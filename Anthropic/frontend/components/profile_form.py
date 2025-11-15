# frontend/components/profile_form.py
from reactpy import component, html, hooks
import json

@component
def ProfileForm(on_submit):
    # State for each input
    name, set_name = hooks.use_state("")
    age, set_age = hooks.use_state("")
    bio, set_bio = hooks.use_state("")
    interests, set_interests = hooks.use_state("")
    favorite_books, set_favorite_books = hooks.use_state("")
    personality_traits, set_personality_traits = hooks.use_state("")

    # State for JSON preview
    profile_json, set_profile_json = hooks.use_state("{}")

    def handle_submit(event):
        event.prevent_default()
        # Construct the profile object
        profile_obj = {
            "name": name.strip(),
            "age": int(age) if age.isdigit() else None,
            "bio": bio.strip(),
            "interests": [i.strip() for i in interests.split(",") if i.strip()],
            "favorite_books": [b.strip() for b in favorite_books.split(",") if b.strip()],
            "personality_traits": [p.strip() for p in personality_traits.split(",") if p.strip()]
        }
        # Update JSON preview
        set_profile_json(json.dumps(profile_obj, indent=4))
        # Call callback (e.g., to pass to Gemini)
        on_submit(profile_obj)

    return html.form(
        {
            "on_submit": handle_submit,
            "style": {"display": "flex", "flexDirection": "column", "gap": "10px", "maxWidth": "600px"}
        },
        html.label("Name:"),
        html.input({"type": "text", "value": name, "on_change": lambda e: set_name(e["target"]["value"])}),

        html.label("Age:"),
        html.input({"type": "number", "value": age, "on_change": lambda e: set_age(e["target"]["value"])}),

        html.label("Bio:"),
        html.textarea({"value": bio, "on_change": lambda e: set_bio(e["target"]["value"])}),

        html.label("Interests (comma separated):"),
        html.input({"type": "text", "value": interests, "on_change": lambda e: set_interests(e["target"]["value"])}),

        html.label("Favorite Books (comma separated):"),
        html.input({"type": "text", "value": favorite_books, "on_change": lambda e: set_favorite_books(e["target"]["value"])}),

        html.label("Personality Traits (comma separated):"),
        html.input({"type": "text", "value": personality_traits, "on_change": lambda e: set_personality_traits(e["target"]["value"])}),

        html.button({"type": "submit"}, "Generate JSON"),

        html.h3("Preview JSON:"),
        html.pre(profile_json, {"style": {"backgroundColor": "#f0f0f0", "padding": "10px"}})
    )