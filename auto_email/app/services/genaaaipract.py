import google.generativeai as genai
from google.genai import types

def generate_content(
    prompt: str,
    model: str = "gemini-2.0-flash-exp",
) -> str:
    """
    Generate content using Gemini AI with hardcoded API key.
    """
    # Hardcoded API key as requested
    api_key = "AIzaSyCVs4PWrKnunpTfEPobwAd7pFAWkPXQZEo"
    
    if not api_key:
        raise RuntimeError("API key not available.")

    # Initialize client
    client = genai.Client(api_key=api_key)

    # Build the content request
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]

    # Configuration
    tools = [types.Tool(googleSearch=types.GoogleSearch())]
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0),
        tools=tools
    )

    # Stream and collect response
    full_response = []
    try:
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=config
        ):
            if chunk.text:
                full_response.append(chunk.text)
    except Exception as e:
        print(f"Error during generation: {e}")
        return "Error generating content"

    return "".join(full_response)


if __name__ == "__main__":
    prompt = "hello"
    try:
        out = generate_content(prompt)
        print(out)
    except Exception as e:
        print("Error during generation:", e)