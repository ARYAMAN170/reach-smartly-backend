import fitz  # PyMuPDF
import tempfile
import os
import logging
import json
import re
from typing import Dict, Union
from fastapi import UploadFile
from app.services.genaaaipract import generate_content

# Set up logging
logger = logging.getLogger(__name__)


async def extract_user_summary_from_pdf_upload(file: UploadFile) -> Union[Dict, str]:
    """
    Extracts user details and professional summary from the uploaded PDF resume
    using a single comprehensive prompt for better consistency.

    Args:
        file: UploadFile object containing the PDF resume

    Returns:
        Dictionary with extracted user details or error string
    """
    tmp_path = None

    try:
        # Reset file pointer to beginning
        await file.seek(0)

        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            content = await file.read()
            if not content:
                return {"error": "Uploaded file is empty"}

            tmp.write(content)
            tmp_path = tmp.name

        # Extract text from PDF
        resume_text = await _extract_text_from_pdf(tmp_path)
        if isinstance(resume_text, dict) and "error" in resume_text:
            return resume_text

        # Process with AI to extract all fields at once
        results = await _process_resume_with_single_prompt(resume_text)

        logger.info(f"Successfully extracted resume data: {results}")
        return results

    except Exception as e:
        logger.error(f"Error in extract_user_summary_from_pdf_upload: {str(e)}")
        return {"error": f"Failed to process resume: {str(e)}"}

    finally:
        # Clean up temporary file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception as cleanup_error:
                logger.warning(f"Failed to cleanup temp file: {cleanup_error}")


async def _extract_text_from_pdf(pdf_path: str) -> Union[str, Dict]:
    """
    Extract text content from PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text string or error dictionary
    """
    try:
        text_pages = []

        with fitz.open(pdf_path) as doc:
            if len(doc) == 0:
                return {"error": "PDF file appears to be empty"}

            for page_num, page in enumerate(doc):
                try:
                    page_text = page.get_text()

                    # Robust check for valid text
                    if (page_text and
                            isinstance(page_text, str) and
                            page_text.strip()):
                        text_pages.append(page_text.strip())

                except Exception as page_error:
                    logger.warning(f"Error extracting text from page {page_num}: {page_error}")
                    continue

        # Check if we extracted any text
        if not text_pages:
            return {"error": "No readable text found in the PDF. The file might be image-based or corrupted."}

        resume_text = "\n".join(text_pages).strip()

        # Additional validation for meaningful content
        if len(resume_text) < 50:  # Arbitrary minimum length
            return {"error": "PDF contains insufficient text content"}

        return resume_text

    except Exception as e:
        logger.error(f"Error extracting text from PDF: {str(e)}")
        return {"error": f"Failed to read PDF file: {str(e)}"}


async def _process_resume_with_single_prompt(resume_text: str) -> Dict:
    """
    Process resume text with AI using a single comprehensive prompt for better consistency.

    Args:
        resume_text: Raw text extracted from resume

    Returns:
        Dictionary with extracted fields
    """
    try:
        # Single comprehensive prompt that asks for all information at once
        prompt = f"""
You are an AI assistant that extracts information from resumes. Please analyze the following resume text and extract the requested information. Return your response as a valid JSON object with exactly these keys:

{{
  "first_name": "candidate's first name only (string or null if not found)",
  "last_name": "candidate's last name only (string or null if not found)", 
  "email_id": "candidate's email address (string or null if not found)",
  "professional_title": "candidate's current role/job title/status like 'Software Engineer', '3rd Year Student', 'Recent Graduate', 'Marketing Intern' (string or null if not found)",
  "professional_summary": "a concise 1-2 sentence professional summary highlighting key skills, experience level, academic status, and achievements (string or null if insufficient information)"
}}

Rules:
1. Extract only factual information present in the resume
2. If any field cannot be determined, use null (not empty string)
3. For professional_title, look for current role, job title, or academic status
4. For professional_summary, create a brief summary based on the resume content
5. Return ONLY the JSON object, no additional text or formatting
6. Ensure the JSON is valid and properly formatted

Resume Text:
{resume_text}
"""

        # Call AI service
        response = generate_content(prompt)

        if response is None:
            logger.error("AI service returned None")
            return _get_fallback_extraction(resume_text)

        # Clean the response to extract JSON
        cleaned_response = _clean_json_response(response)

        try:
            # Parse the JSON response
            extracted_data = json.loads(cleaned_response)

            # Validate the response has all required keys
            required_keys = ['first_name', 'last_name', 'email_id', 'professional_title', 'professional_summary']
            for key in required_keys:
                if key not in extracted_data:
                    extracted_data[key] = None

            # Clean up any empty strings to null
            for key, value in extracted_data.items():
                if isinstance(value, str):
                    cleaned_value = value.strip()
                    if not cleaned_value or cleaned_value.lower() in ['null', 'none', 'n/a', 'not found',
                                                                      'not available']:
                        extracted_data[key] = None
                    else:
                        extracted_data[key] = cleaned_value

            logger.info(f"Successfully parsed AI response: {extracted_data}")
            return extracted_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON response: {e}")
            logger.error(f"Raw response: {response}")
            logger.error(f"Cleaned response: {cleaned_response}")

            # Fallback to regex extraction
            return _get_fallback_extraction(resume_text)

    except Exception as e:
        logger.error(f"Error in single prompt processing: {str(e)}")
        return _get_fallback_extraction(resume_text)


def _clean_json_response(response: str) -> str:
    """
    Clean the AI response to extract valid JSON.

    Args:
        response: Raw AI response

    Returns:
        Cleaned JSON string
    """
    if not response:
        return "{}"

    # Remove any text before the first {
    start_idx = response.find('{')
    if start_idx == -1:
        return "{}"

    # Remove any text after the last }
    end_idx = response.rfind('}')
    if end_idx == -1:
        return "{}"

    # Extract the JSON part
    json_part = response[start_idx:end_idx + 1]

    # Remove any markdown formatting
    json_part = json_part.replace('```json', '').replace('```', '').strip()

    return json_part


def _get_fallback_extraction(resume_text: str) -> Dict:
    """
    Fallback extraction using regex patterns when AI parsing fails.

    Args:
        resume_text: Raw resume text

    Returns:
        Dictionary with extracted fields
    """
    logger.info("Using fallback regex extraction")

    result = {
        'first_name': None,
        'last_name': None,
        'email_id': None,
        'professional_title': None,
        'professional_summary': None
    }

    try:
        # Email extraction (most reliable)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.findall(email_pattern, resume_text)
        if email_matches:
            result['email_id'] = email_matches[0]

        # Name extraction (look for patterns at the beginning)
        lines = resume_text.split('\n')
        for i, line in enumerate(lines[:5]):  # Check first 5 lines
            line = line.strip()
            if line and len(line) < 50:  # Likely a name if short and near top
                # Remove common prefixes/suffixes
                clean_line = re.sub(r'^(mr\.?|ms\.?|mrs\.?|dr\.?)\s*', '', line, flags=re.IGNORECASE)
                clean_line = re.sub(r'\s*(resume|cv|curriculum vitae)$', '', clean_line, flags=re.IGNORECASE)

                # Check if it looks like a name (2-4 words, mostly letters)
                words = clean_line.split()
                if 2 <= len(words) <= 4 and all(re.match(r'^[A-Za-z\s\'-]+$', word) for word in words):
                    result['first_name'] = words[0]
                    if len(words) > 1:
                        result['last_name'] = words[-1]
                    break

        # Professional title extraction (look for common job titles or student status)
        title_patterns = [
            r'\b(?:software|web|mobile|frontend|backend|full[\s-]?stack|senior|junior|lead|principal)\s+(?:engineer|developer|programmer)\b',
            r'\b(?:data|machine learning|ai|ml)\s+(?:scientist|engineer|analyst)\b',
            r'\b(?:product|project|program)\s+manager\b',
            r'\b(?:ux|ui|product)\s+designer\b',
            r'\b(?:marketing|sales|business)\s+(?:manager|executive|analyst)\b',
            r'\b(?:intern|internship)\b.*?\b(?:at|in)\s+\w+',
            r'\b(?:student|graduate|undergraduate)\b.*?\b(?:year|final|3rd|third|4th|fourth)\b',
            r'\b(?:recent|fresh)\s+graduate\b',
            r'\b(?:btech|b\.tech|bachelor|master|mca|mba)\s+(?:student|graduate)\b'
        ]

        for pattern in title_patterns:
            matches = re.findall(pattern, resume_text, re.IGNORECASE)
            if matches:
                result['professional_title'] = matches[0].strip()
                break

        # Create a basic professional summary
        if result['professional_title'] or result['first_name']:
            name_part = result['first_name'] or "Candidate"
            title_part = result['professional_title'] or "professional"
            result['professional_summary'] = f"{name_part} is a {title_part} with demonstrated experience and skills."

    except Exception as e:
        logger.error(f"Error in fallback extraction: {str(e)}")

    return result


def _validate_extracted_data(data: Dict) -> Dict:
    """
    Validate and clean extracted data.

    Args:
        data: Raw extracted data dictionary

    Returns:
        Validated and cleaned data dictionary
    """
    if data.get('email_id'):
        email = data['email_id']
        # Basic email validation
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$', email):
            data['email_id'] = None

    # Ensure names don't contain numbers or special characters
    for name_field in ['first_name', 'last_name']:
        if data.get(name_field):
            name = data[name_field]
            if not re.match(r'^[A-Za-z\s\'-]+$', name):
                data[name_field] = None

    return data
