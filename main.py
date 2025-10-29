"""
SQL Agent Desktop Application
Main entry point for the desktop version.
"""
import sys
import os
import threading
import time
import webbrowser
import logging
from app import app
from backend.config.config import Config

def start_flask_app():
    """Start Flask application in a separate thread."""
    try:
        app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
    except Exception as e:
        print(f"Flask app error: {e}")

def check_flask_ready(max_attempts=10):
    """Check if Flask app is ready to serve requests."""
    import requests
    for attempt in range(max_attempts):
        try:
            response = requests.get('http://127.0.0.1:5000/api/health', timeout=1)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(0.5)
    return False

def main():
    """Main function for desktop application."""
    print("=" * 50)
    print("SQL Agent Desktop Application")
    print("=" * 50)
    print("Starting Flask server...")
    
    # Start Flask app in background thread
    flask_thread = threading.Thread(target=start_flask_app, daemon=True)
    flask_thread.start()
    
    # Wait for Flask to be ready
    print("Waiting for server to start...")
    if check_flask_ready():
        print("Server started successfully!")
        print("Opening browser...")
        
        # Open browser
        webbrowser.open('http://127.0.0.1:5000')
        
        print("\n" + "=" * 50)
        print("SQL Agent is running at: http://127.0.0.1:5000")
        print("=" * 50)
        print("Instructions:")
        print("   - The application will open in your default browser")
        print("   - Connect to your SQL Server database")
        print("   - Start asking questions in natural language")
        print("   - Press Ctrl+C to exit")
        print("=" * 50)
        
        try:
            # Keep main thread alive
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down SQL Agent...")
            sys.exit(0)
    else:
        print("Failed to start server!")
        print("Please check if port 5000 is available.")
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
