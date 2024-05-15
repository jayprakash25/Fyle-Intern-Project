import os
import sys

print(f"Current working directory: {os.getcwd()}")
print(f"System path: {sys.path}")

try:
    import core
    from core import app
    print("Flask application imported successfully!")
except ImportError as e:
    print(f"Failed to import Flask application: {e}")