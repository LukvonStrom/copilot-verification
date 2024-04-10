# config.py
import os


class Config:
    DEBUG = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    BASE_DIR = os.getenv("BASE_DIR", os.getcwd())
    # Add more configuration options here
