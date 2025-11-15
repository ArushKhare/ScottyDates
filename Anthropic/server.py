from flask import Flask
from reactpy.backend.flask import configure
from backend.api import api
from frontend.app import App

app = Flask(__name__)

# Register API endpoints
app.register_blueprint(api, url_prefix="/api")

# Mount ReactPy root component at "/"
configure(app, App)

if __name__ == "__main__":
    app.run(debug=True)