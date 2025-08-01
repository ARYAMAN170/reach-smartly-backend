import os
import google.generativeai as genai

def generate_content(
    prompt: str,
    model: str = "gemini-1.5-flash",  # Update model name to valid one
) -> str:
    """
    Stream the full generated text from Gemini.
    Requires either:
      - api_key passed in, or
      - environment var GEMINI_API_KEY set.
    """
    # 1. Resolve API key
    key = os.getenv("GEMINI_API_KEY", "AIzaSyCVs4PWrKnunpTfEPobwAd7pFAWkPXQZEo")
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set and no api_key argument provided.")

    # 2. Configure the API
    genai.configure(api_key=key)

    # 3. Select the model
    model = genai.GenerativeModel(model)

    # 4. Generate content
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    prompt = "hello"
    out = generate_content(prompt)
    print(out)
