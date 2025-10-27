"""
Main Flask application factory.
Creates and configures the Flask application.
"""
from flask import Flask, render_template
import logging
import atexit

from config import Config
from routes import api_bp, db_routes
from utils import LoggingUtils


def create_app() -> Flask:
    """
    Application factory pattern.
    Creates and configures Flask application.
    
    Returns:
        Configured Flask application
    """
    # Validate configuration
    Config.validate_config()
    
    # Setup logging
    LoggingUtils.setup_logging()
    logger = logging.getLogger(__name__)
    
    # Create Flask app
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['DEBUG'] = Config.DEBUG
    # Ensure templates/static reload so UI changes appear immediately
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    try:
        app.jinja_env.cache = {}
    except Exception:
        pass
    
    # Register blueprints
    app.register_blueprint(api_bp)
    
    
    # Register main route
    @app.route("/")
    def index():
        """Serve main application page."""
        return render_template("index.html")
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return {"error": "Endpoint not found"}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        logger.error(f"Internal server error: {error}")
        return {"error": "Internal server error"}, 500
    
    logger.info("Flask application created successfully")
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
