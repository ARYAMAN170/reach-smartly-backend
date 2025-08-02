import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
from google.genai import types

def generate_content(
    prompt: str,
    model: str = "gemini-2.5-flash-lite",
) -> str:
    """
    Stream the full generated text from Gemini.
    Requires either:
      - api_key passed in, or
      - environment var GEMINI_API_KEY set.
    """
    # 1. Resolve API key
    key = os.getenv('GEMINI_API_KEY')
    if not key:
        raise RuntimeError("GEMINI_API_KEY not set and no api_key argument provided.")

    # 2. Initialize client
    client = genai.Client(api_key=key)

    # 3. Build the single-content request
    contents = [
        types.Content(
            role="user",
            parts=[types.Part.from_text(text=prompt)]
        )
    ]

    # 4. (Optional) Tools & thinking config
    #    Remove these if you don’t actually need search tools
    tools = [ types.Tool(googleSearch=types.GoogleSearch()) ]
    config = types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=0),
        tools=tools
    )

    # 5. Stream and collect
    full_response = []
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=config
    ):
        full_response.append(chunk.text)

    return "".join(full_response)


if __name__ == "__main__":
    prompt = "hello"
    try:
        out = generate_content(prompt)
        print(out)
    except Exception as e:
        print("Error during generation:", e)
