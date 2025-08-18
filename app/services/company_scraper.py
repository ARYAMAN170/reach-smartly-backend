
import os
import requests
from bs4 import BeautifulSoup
from app.core.config import settings


def get_company_website(company_name: str) -> str:
    """
    Search for a company's official website using Serper API.
    
    Args:
        company_name: Name of the company to search for
        
    Returns:
        Company website URL or None if not found
    """
    # Get API key from settings/environment
    api_key = settings.SERPER_API_KEY or os.getenv("SERPER_API_KEY")
    if not api_key:
        raise ValueError(
            "SERPER_API_KEY not found in environment variables. "
            "Please set SERPER_API_KEY in your environment or .env file."
        )
    
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "q": f"{company_name} official website"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Look for the company's official website, avoiding social media links
        for result in data.get("organic", []):
            link = result.get("link", "")
            if (link and 
                "linkedin" not in link.lower() and 
                "facebook" not in link.lower() and 
                "twitter" not in link.lower() and
                "instagram" not in link.lower() and
                ".com" in link):
                return link
        return None
        
    except requests.RequestException as e:
        print(f"⚠️ Error searching for company website: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Unexpected error: {e}")
        return None

def get_company_overview(website_url: str) -> str:
    """
    Scrape company overview from their website.
    
    Args:
        website_url: URL of the company website
        
    Returns:
        Company overview text or None if not found
    """
    if not website_url:
        return None
        
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(website_url, headers=headers, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Try multiple strategies to get company description
        summary_parts = []

        # 1. Try meta description first
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            content = meta_desc["content"].strip()
            if len(content) > 20:  # Only add if meaningful
                summary_parts.append(content)

        # 2. Try Open Graph description
        og_desc = soup.find("meta", property="og:description")
        if og_desc and og_desc.get("content"):
            content = og_desc["content"].strip()
            if content not in str(summary_parts) and len(content) > 20:
                summary_parts.append(content)

        # 3. Look for common "about" sections
        about_selectors = [
            'section[class*="about"]',
            'div[class*="about"]',
            'section[class*="overview"]',
            'div[class*="overview"]',
            'section[class*="company"]',
            'div[class*="company"]'
        ]
        
        for selector in about_selectors:
            about_section = soup.select_one(selector)
            if about_section:
                text = about_section.get_text().strip()
                if 50 < len(text) < 500:  # Reasonable length
                    summary_parts.append(text[:400] + "..." if len(text) > 400 else text)
                    break

        # 4. Grab meaningful paragraphs as fallback
        if len(summary_parts) < 2:
            paragraph_texts = []
            for p in soup.find_all("p"):
                text = p.get_text().strip()
                # Filter out navigation, footer, and other non-content paragraphs
                if (30 < len(text) < 300 and 
                    not any(word in text.lower() for word in ['cookie', 'privacy', 'terms', 'navigation', 'menu', 'footer'])):
                    paragraph_texts.append(text)
                if len(paragraph_texts) >= 2:
                    break

            summary_parts.extend(paragraph_texts)

        # Combine all parts
        final_summary = "\n\n".join(summary_parts[:3])  # Limit to first 3 parts
        return final_summary.strip() if final_summary and len(final_summary) > 30 else None

    except requests.RequestException as e:
        print(f"⚠️ Error fetching company overview: {e}")
        return None
    except Exception as e:
        print(f"⚠️ Error parsing company overview: {e}")
        return None

def get_company_info(company_name: str) -> dict:
    """
    Get comprehensive company information including website and overview.
    
    Args:
        company_name: Name of the company to research
        
    Returns:
        Dictionary containing company information
    """
    result = {
        "company_name": company_name,
        "website": None,
        "overview": None,
        "success": False,
        "error": None
    }
    
    try:
        # Get company website
        website = get_company_website(company_name)
        if not website:
            result["error"] = "Could not find company website"
            return result
            
        result["website"] = website
        
        # Get company overview
        overview = get_company_overview(website)
        if overview:
            result["overview"] = overview
            result["success"] = True
        else:
            result["error"] = "Could not extract company overview from website"
            
        return result
        
    except Exception as e:
        result["error"] = f"Error getting company information: {str(e)}"
        return result


# === MAIN ===
if __name__ == "__main__":
    company = input("Enter company name: ").strip()
    
    if not company:
        print("❌ Please enter a valid company name.")
        exit(1)
        
    print(f"🔍 Searching for information about: {company}")
    
    info = get_company_info(company)
    
    if info["success"]:
        print(f"\n🌐 Website: {info['website']}")
        print(f"\n📄 Company Overview:\n{info['overview']}")
    else:
        print(f"\n❌ {info['error']}")
        if info["website"]:
            print(f"🌐 Website found: {info['website']}")
