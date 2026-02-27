import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../database/osint.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change')
    # API Keys (get from respective services)
    HIBP_API_KEY = os.getenv('HIBP_API_KEY', '')  # HaveIBeenPwned
    EMAILREP_API_KEY = os.getenv('EMAILREP_API_KEY', '')  # EmailRep.io
    ABSTRACT_API_KEY = os.getenv('ABSTRACT_API_KEY', '')  # Phone validation
