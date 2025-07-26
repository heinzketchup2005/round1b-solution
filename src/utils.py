import logging
import os

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler()
        ]
    )

def ensure_directories():
    """Ensure required directories exist"""
    directories = ['/app/input', '/app/output', '/app/models']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)