import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///task_manager.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
    RESTX_MASK_SWAGGER = False
    PROPAGATE_EXCEPTIONS = True
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=4)
