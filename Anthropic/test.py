from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

# Get API key from environment
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

# Initialize the client
client = genai.Client(api_key=api_key)

profile = {
    "name": "Alice",
    "age": 27,
    "bio": "Adventurous, loves hiking and reading mystery novels.",
    "interests": ["hiking", "reading", "photography"],
    "favorite_books": ["Gone Girl", "Sherlock Holmes"],
    "personality_traits": ["adventurous", "funny"]
}

prompt = f"""
You are a helpful assistant that generates dating app opening lines.

Given the following user profile in JSON format:

{profile}

Please generate 3 creative, friendly, and personalized opening lines that someone could use to start a conversation with this person. 

Output **must** be valid JSON with this structure:

{{
    "opening_lines": [
        {{
            "line": "string with the opening line",
            "reason": "why this line matches the profile"
        }}
    ]
}}

Follow the JSON structure exactly.
Output only a valid JSON object that contains no extra text, explanation, or Markdown formatting before or after.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

sample_response_text = """{
    "opening_lines": [
        {
            "line": "Hey Alice! Love that you're into hiking ...",
            "reason": "..."
        }
    ]
}"""

def clean_gemini_response(response_text: str) -> str:
    """
    Remove Markdown code fences like ```json and ``` from Gemini's response.
    """
    if not response_text:
        return ""
    
    cleaned = response_text.strip()
    
    # Remove opening ```json or ``` 
    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json"):].strip()
    elif cleaned.startswith("```"):
        cleaned = cleaned[len("```"):].strip()
    
    # Remove closing ```
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()
    
    return cleaned
# Parse the JSON output safely
response_text = clean_gemini_response(response.text)
print(response_text)
print("\n")
data = json.loads(response_text.strip())
for item in data["opening_lines"]:
    print(item["line"], "-", item["reason"])
