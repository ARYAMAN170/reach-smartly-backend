import os
import google.generativeai as genai
from app.core.config import settings


def generate_content(
        prompt: str,
        model: str = "gemini-2.0-flash-exp",
        api_key: str = None
) -> str:
    """
    Generate text content using Google's Gemini AI model.

    Args:
        prompt: The input text prompt
        model: The Gemini model to use (default: gemini-2.0-flash-exp)
        api_key: Optional API key (if not provided, uses GEMINI_API_KEY env var)

    Returns:
        Generated text response or error message
    """

    # 1. Resolve API key
    key = api_key or settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError(
            "GEMINI_API_KEY not set in environment variables and no api_key argument provided. "
            "Please set GEMINI_API_KEY environment variable or pass api_key parameter."
        )

    try:
        # 2. Configure the API
        genai.configure(api_key=key)

        # 3. Create the model instance
        model_instance = genai.GenerativeModel(model)

        # 4. Generate content
        response = model_instance.generate_content(prompt)

        # Check if response has text
        if hasattr(response, 'text') and response.text:
            return response.text
        else:
            return "No text response generated"

    except Exception as e:
        return f"Error generating content: {str(e)}"

def generate_content_with_config(
        prompt: str,
        model: str = "gemini-2.0-flash-exp",
        temperature: float = 0.7,
        max_output_tokens: int = 1024,
        api_key: str = None
) -> str:
    """
    Generate content with additional configuration options.

    Args:
        prompt: The input text prompt
        model: The Gemini model to use
        temperature: Controls randomness (0.0 - 1.0)
        max_output_tokens: Maximum tokens in response
        api_key: Optional API key

    Returns:
        Generated text response or error message
    """

    # 1. Resolve API key
    key = api_key or settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set and no api_key argument provided.")

    try:
        # 2. Configure the API
        genai.configure(api_key=key)

        # 3. Create generation config
        generation_config = genai.types.GenerationConfig(
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )

        # 4. Create the model instance with config
        model_instance = genai.GenerativeModel(
            model_name=model,
            generation_config=generation_config
        )

        # 5. Generate content
        response = model_instance.generate_content(prompt)

        if hasattr(response, 'text') and response.text:
            return response.text
        else:
            return "No text response generated"

    except Exception as e:
        return f"Error generating content: {str(e)}"


if __name__ == "__main__":
    # Test the function
    test_prompt = "tell me about apple"

    # Test basic function
    print("Testing basic generate_content:")
    result = generate_content(test_prompt)
    print(f"Result: {result}\n")


