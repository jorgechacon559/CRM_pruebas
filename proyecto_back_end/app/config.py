import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-muy-secreta')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-clave-muy-secreta')
    JWT_ACCESS_TOKEN_EXPIRES = 900  # 15 minutos
    JWT_REFRESH_TOKEN_EXPIRES = 86400  # 1 día
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
