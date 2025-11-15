import google.generativeai as genai
import json
import os
import time

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

profile_a = {
    "name": "Alice",
    "age": 29,
    "interests": ["fitness", "cooking"],
    "active": True
}

profile_b = {
    "name": "Bob",
    "age": 31,
    "interests": ["cooking", "travel"],
    "active": False
}

prompt = f"""
You are an expert data analyst. Compare the following two JSON user profiles. Provide score from 1-10.

OUTPUT STRICTLY IN JSON. DO NOT USE ``` in the text.

Profile A:
json
{json.dumps(profile_a, indent=2)}
{json.dumps(profile_b, indent=2)}
{{
"similarities": [],
"differences": [],
"insights": [],
"score": 0
}}
"""

response = model.generate_content(prompt)

t = response.text

print(t)

try:
    j = json.loads(t.rstrip())
except Exception as e:
    print(e)

print(j["similarities"])
