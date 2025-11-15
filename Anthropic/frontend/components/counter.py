from reactpy import component, html, hooks
import httpx
from flask import request

@component
def Counter():
    count, set_count = hooks.use_state(0)
    message, set_message = hooks.use_state("")

    async def increment(event):
        set_count(count + 1)

    async def call_backend(event):
        # Build full URL dynamically from the current request
        host = request.host_url.rstrip("/")  # e.g. http://127.0.0.1:5000
        url = f"{host}/api/hello"           # relative path becomes full URL

        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            data = resp.json()
            set_message(data.get("message", "No message"))

    return html.div(
        html.h3(f"Count: {count}"),
        html.button({"on_click": increment}, "Increment"),
        html.hr(),
        html.button({"on_click": call_backend}, "Call Backend"),
        html.p(f"Backend says: {message}")
    )