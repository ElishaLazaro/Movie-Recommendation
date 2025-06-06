from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(
        __name__,
        static_url_path="/",
        static_folder="./view/",
        template_folder="./view/",
    )
    CORS(app)  # Enable CORS if needed

    with app.app_context():
        from .routes import routes_bp  # Import the Blueprint

        app.register_blueprint(routes_bp)  # Register the Blueprint

    return app
