"""
Legacy main.py file - DEPRECATED
Use app.py instead for the new clean architecture.

This file is kept for backward compatibility but should not be used.
All functionality has been moved to the new modular structure.
"""

import warnings
from app import app

warnings.warn(
    "main.py is deprecated. Please use 'python app.py' instead.",
    DeprecationWarning,
    stacklevel=2
)

if __name__ == "__main__":
    print("⚠️  WARNING: main.py is deprecated!")
    print("📁 Please use 'python app.py' instead for the new clean architecture.")
    print("🚀 Starting application with legacy compatibility...")
    app.run(debug=True)
