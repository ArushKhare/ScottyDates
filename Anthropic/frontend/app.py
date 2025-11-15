# app.py
from reactpy import component
from frontend.components.profile_form import ProfileForm
from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

# ---------------------------
# Initialize Gemini client
# ---------------------------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment")

client = genai.Client(api_key=api_key)

# ---------------------------
# AI Line Generator
# ---------------------------
def ai_line_generator(profile: dict) -> list[dict]:
    """
    Generate AI-powered dating app opening lines based on a user's profile.
    Uses the global `client` instance.
    """
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

    def clean_gemini_response(response_text: str) -> str:
        if not response_text:
            return ""
        cleaned = response_text.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[len("```json"):].strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned[len("```"):].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
        return cleaned

    response_text = clean_gemini_response(response.text)

    try:
        data = json.loads(response_text)
        return data.get("opening_lines", [])
    except json.JSONDecodeError:
        print("Failed to parse JSON from Gemini response")
        return []

def handle_profile_submit(profile_data):
    """
    Called when the profile form is submitted.
    Prints the profile and generates AI opening lines.
    """
    print("Profile submitted:", profile_data)

    # Generate AI opening lines
    lines = ai_line_generator(profile_data)

    # Print each line and reason
    if lines:
        print("Generated opening lines:")
        for line in lines:
            print(f"{line['line']} - {line['reason']}")
    else:
        print("No opening lines generated.")


@component
def App():
    return ProfileForm(on_submit=handle_profile_submit,ai_line_generator=ai_line_generator)
