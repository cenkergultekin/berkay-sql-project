"""
Main Flask application factory.
Creates and configures the Flask application.
"""
import sys
import os
from flask import Flask, render_template
import logging
import atexit

# PyInstaller için path düzeltmesi
if getattr(sys, 'frozen', False):
    # PyInstaller bundle içindeyiz
    bundle_dir = sys._MEIPASS
    template_folder = os.path.join(bundle_dir, 'frontend', 'templates')
    static_folder = os.path.join(bundle_dir, 'frontend', 'static')
else:
    # Normal Python çalıştırması
    template_folder = 'frontend/templates'
    static_folder = 'frontend/static'

from backend.config.config import Config
from backend.routes.routes import api_bp, db_routes
from backend.core.utils import LoggingUtils


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
    
    # Create Flask app with dynamic template and static folders
    app = Flask(__name__, 
                template_folder=template_folder,
                static_folder=static_folder)
    
    # Configure app
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    app.config['DEBUG'] = False  # Desktop sürümde debug kapalı
    app.config['TEMPLATES_AUTO_RELOAD'] = False
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    
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
    app.run(debug=False, host='127.0.0.1', port=5000)
