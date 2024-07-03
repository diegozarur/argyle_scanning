import os
from typing import Optional, Union

from dotenv import load_dotenv

load_dotenv()


class Config:
    # General Flask Config
    SECRET_KEY: Optional[str] = os.getenv("SECRET_KEY")
    FLASK_ENV: Optional[str] = os.getenv('FLASK_ENV')
    DEBUG: Optional[Union[str, bool]] = os.getenv('DEBUG')

    # Celery Config
    CELERY_BROKER_URL: Optional[str] = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND: Optional[str] = os.getenv('CELERY_RESULT_BACKEND')

    # Session and Cookie Config
    SESSION_COOKIE_HTTPONLY: bool = True
    REMEMBER_COOKIE_HTTPONLY: bool = True
    REMEMBER_COOKIE_DURATION: int = 3600

    # Logging
    LOG_TO_STDOUT: Optional[str] = os.getenv('LOG_TO_STDOUT')

    # Path to credentials JSON file
    SCANNER_SETTINGS: Optional[str] = os.getenv('SCANNER_SETTINGS')
    STORAGE_TYPE: Optional[str] = os.getenv('STORAGE_TYPE')
    FLASK_PORT: Optional[str] = os.getenv('FLASK_PORT')
    SELENIUM_HUB_URL: Optional[str] = os.getenv('SELENIUM_HUB_URL')


class ProductionConfig(Config):
    DEBUG: bool = False
    TESTING: bool = False
    FLASK_ENV: str = 'production'
    SESSION_COOKIE_SECURE: bool = True
    REMEMBER_COOKIE_DURATION: int = 86400  # 1 day


class DebugConfig(Config):
    DEBUG: bool = True
    TESTING: bool = True
    FLASK_ENV: str = 'development'
    TEMPLATES_AUTO_RELOAD: bool = True

    # Hot-reloading
    USE_RELOADER: bool = True


# Load all possible configurations
config_dict = {
    'production': ProductionConfig(),
    'debug': DebugConfig()
}
