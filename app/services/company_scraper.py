
import requests
from bs4 import BeautifulSoup

SERPER_API_KEY = "e3c277dde2ee2ca8144d4a1b701b588b3b1ba433"

def get_company_website(company_name):
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "q": f"{company_name} official website"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    for result in data.get("organic", []):
        link = result.get("link", "")
        if "linkedin" not in link and "facebook" not in link and ".com" in link:
            return link
    return None

def get_company_overview(website_url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(website_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Try meta description first
        meta = soup.find("meta", attrs={"name": "description"})
        if meta and meta.get("content"):
            summary = meta["content"].strip()
        else:
            summary = ""

        # Add og:description if available
        og = soup.find("meta", property="og:description")
        if og and og.get("content") and og["content"] not in summary:
            summary += "\n" + og["content"].strip()

        # Grab first few meaningful <p> tags
        paragraph_texts = []
        for p in soup.find_all("p"):
            text = p.get_text().strip()
            if 30 < len(text) < 300:
                paragraph_texts.append(text)
            if len(paragraph_texts) >= 3:
                break

        if paragraph_texts:
            summary += "\n\n" + "\n".join(paragraph_texts)

        return summary.strip() if summary else None

    except Exception as e:
        print("⚠️ Error fetching overview:", e)
        return None

# === MAIN ===
if __name__ == "__main__":
    company = input("Enter company name: ").strip()
    website = get_company_website(company)

    if website:
        print(f"\n🌐 Website: {website}")
        overview = get_company_overview(website)
        if overview:
            print(f"\n📄 Company Overview:\n{overview}")
        else:
            print("\n⚠️ No overview found.")
    else:
        print("❌ Couldn't find the company website.")
