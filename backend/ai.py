# backend/ai.py
import os
import json
from typing import Dict, List

from google import genai

# Client will read GEMINI_API_KEY or GOOGLE_API_KEY from env if not passed explicitly
#   export GEMINI_API_KEY="your-key"
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")  # good default as of late 2025


def profile_to_text(profile: Dict) -> str:
    """Turn a profile dict into a readable text block for the model."""
    interests_str = ", ".join(profile.get("interests", []))
    return (
        f"Name: {profile.get('full_name')}\n"
        f"Age: {profile.get('age')}\n"
        f"Major: {profile.get('major')}\n"
        f"Class year: {profile.get('class_year')}\n"
        f"Campus: {profile.get('campus')}\n"
        f"Interests: {interests_str}\n"
        f"Bio: {profile.get('bio')}\n"
    )


def get_match_score(user_profile: Dict, other_profile: Dict) -> float:
    """
    Ask Gemini for a compatibility score between 0 and 100.
    We prompt it to return ONLY a number and then parse.
    """
    user_text = profile_to_text(user_profile)
    other_text = profile_to_text(other_profile)

    prompt = (
        "You are a compatibility rater for a college-only dating app.\n"
        "Given two student profiles, return ONLY a numeric compatibility score between 0 and 100.\n"
        "Higher scores mean more shared interests, similar vibe, and likely good conversation.\n\n"
        "Profile A:\n"
        f"{user_text}\n"
        "Profile B:\n"
        f"{other_text}\n\n"
        "Score (number only):"
    )

    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )  # response.text contains model text output :contentReference[oaicite:2]{index=2}

    text = (resp.text or "").strip()
    try:
        score = float(text)
    except ValueError:
        score = 50.0

    return max(0.0, min(100.0, score))


def chat_helper(
    current_user_profile: Dict,
    other_profile: Dict,
    recent_messages: List[Dict[str, str]],
) -> Dict[str, List[str] | str]:
    """
    Summarize the other person's profile & suggest 3 non-cringe openers.
    recent_messages: list of {"from": "me" | "them", "text": "..."}
    """
    other_text = profile_to_text(other_profile)

    convo_str = ""
    for msg in recent_messages[-10:]:
        who = "You" if msg["from"] == "me" else other_profile.get("full_name", "Them")
        convo_str += f"{who}: {msg['text']}\n"

    # We'll ask for JSON and parse it ourselves
    json_schema_hint = {
        "summary": "string",
        "openers": ["string", "string", "string"],
    }

    prompt = (
        "You are a socially aware assistant helping a student talk to a match "
        "on an in-college dating app.\n\n"
        "Other person's profile:\n"
        f"{other_text}\n\n"
        "Recent chat messages (if any):\n"
        f"{convo_str or '(no messages yet)'}\n\n"
        "1) Write a 2–3 sentence summary of the other person's vibe and interests, "
        "addressing the user (e.g., 'They seem like...').\n"
        "2) Suggest exactly 3 friendly, specific, non-cringe lines the user could send next.\n\n"
        "Respond ONLY as valid JSON with this structure:\n"
        f"{json.dumps(json_schema_hint, indent=2)}\n"
    )

    resp = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )

    raw = (resp.text or "").strip()
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        # fallback: treat full text as summary, no openers
        data = {"summary": raw, "openers": []}

    summary = data.get("summary", "")
    openers = data.get("openers", [])
    # enforce exactly 3 lines if possible
    if not isinstance(openers, list):
        openers = [str(openers)]
    openers = [str(o) for o in openers][:3]

    return {"summary": summary, "openers": openers}
