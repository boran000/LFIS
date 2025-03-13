
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "default-dev-key")
    UPLOAD_FOLDER = 'static/uploads'
    
    # MySQL Configuration
    DB_USERNAME = os.environ.get('DB_USERNAME', 'schoolhub_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', '123456')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'schoolhub')
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
