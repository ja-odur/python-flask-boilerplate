"""Module for application configuration"""

# Third-Party libraries
from pathlib import Path
from decouple import config as env_config
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path, verbose=True)

class Config:
    """Base Application configurations"""

    SQLALCHEMY_DATABASE_URI = env_config(
        'DATABASE_URI', default='postgresql://localhost/default_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    """Application production configurations"""

    pass


class DevelopmentConfig(Config):
    """Application development configurations"""

    DEBUG = True

class TestingConfig(Config):
    """Applications testing configuration"""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = env_config(
        'TEST_DATABASE_URI', default='postgresql://localhost/test_default_db'
    )


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}



