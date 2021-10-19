import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SETTINGS_PATH = os.path.abspath(os.path.join(BASE_DIR, "dproject"))

UPLOADED_PROJECTS_DIR = BASE_DIR + '/uploads/projects/'

UPLOADED_OUTPUT_DIR = BASE_DIR + '/uploads/uploaded/output/'
CONFIG_TEMP = BASE_DIR + '/uploads/uploaded/config_temp/'
RESULT_DIR = BASE_DIR + '/result/'
load_dotenv(os.path.join(SETTINGS_PATH, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY')
BASE_URL = os.getenv('BASE_URL')
ENVIRONMENT = os.getenv('ENVIRONMENT', 'Unknown')
DEBUG = bool(int(os.getenv('DEBUG', 0)))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',') if os.getenv('ALLOWED_HOSTS') else []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'NAME': os.getenv('DATABASE_NAME'),
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

STATIC_ROOT = os.getenv('STATIC_ROOT')
