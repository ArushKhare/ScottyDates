from reactpy import component, html, hooks
import json

@component
def ProfileForm(on_submit, ai_line_generator):
    # Form state
    name, set_name = hooks.use_state("")
    age, set_age = hooks.use_state("")
    bio, set_bio = hooks.use_state("")
    interests, set_interests = hooks.use_state("")
    favorite_books, set_favorite_books = hooks.use_state("")
    personality_traits, set_personality_traits = hooks.use_state("")

    # JSON preview state
    profile_json, set_profile_json = hooks.use_state("{}")

    # Generated lines state
    ai_lines, set_ai_lines = hooks.use_state([])

    # Build profile object
    def make_profile():
        return {
            "name": name.strip(),
            "age": int(age) if age.isdigit() else None,
            "bio": bio.strip(),
            "interests": [i.strip() for i in interests.split(",") if i.strip()],
            "favorite_books": [b.strip() for b in favorite_books.split(",") if b.strip()],
            "personality_traits": [p.strip() for p in personality_traits.split(",") if p.strip()]
        }

    # Live update JSON
    def handle_live_update(_event=None):
        profile_obj = make_profile()
        set_profile_json(json.dumps(profile_obj, indent=4))

    # Form submit handler
    def handle_submit(event):
        profile_obj = make_profile()
        set_profile_json(json.dumps(profile_obj, indent=4))
        on_submit(profile_obj)
        return False  # prevent default form submit

    # AI lines handler
    def handle_generate_lines(event):
        profile_obj = make_profile()
        lines = ai_line_generator(profile_obj)
        set_ai_lines(lines)
        return False  # prevent default submit

    return html.form(
        {
            "onsubmit": handle_submit,
            "style": {"display": "flex", "flexDirection": "column", "gap": "10px", "maxWidth": "600px"}
        },

        html.label("Name:"),
        html.input({"type": "text", "value": name, "onchange": lambda e: (set_name(e["target"]["value"]), handle_live_update())}),

        html.label("Age:"),
        html.input({"type": "number", "value": age, "onchange": lambda e: (set_age(e["target"]["value"]), handle_live_update())}),

        html.label("Bio:"),
        html.textarea({"value": bio, "onchange": lambda e: (set_bio(e["target"]["value"]), handle_live_update())}),

        html.label("Interests (comma separated):"),
        html.input({"type": "text", "value": interests, "onchange": lambda e: (set_interests(e["target"]["value"]), handle_live_update())}),

        html.label("Favorite Books (comma separated):"),
        html.input({"type": "text", "value": favorite_books, "onchange": lambda e: (set_favorite_books(e["target"]["value"]), handle_live_update())}),

        html.label("Personality Traits (comma separated):"),
        html.input({"type": "text", "value": personality_traits, "onchange": lambda e: (set_personality_traits(e["target"]["value"]), handle_live_update())}),

        html.div(
            {"style": {"display": "flex", "gap": "10px"}},
            html.button({"type": "submit"}, "Submit Profile"),
            html.button({"type": "button", "onclick": handle_generate_lines}, "Generate Lines")
        ),

        html.h3("Preview JSON:"),
        html.pre({"style": {"backgroundColor": "#f0f0f0", "padding": "10px"}}, profile_json),

        html.h3("Generated Lines:"),
        html.div([html.p(line) for line in ai_lines])
    )
