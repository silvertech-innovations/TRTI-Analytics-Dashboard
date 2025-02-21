import os
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY: Load secret key from environment variable
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure--ch56#y1ir*0km4e6l236o_hzazm@pk(#%mn)=z4jb)qs$_+^b')

# SECURITY: Debug should be False in production
DEBUG = os.getenv("DEBUG", "True") == "True"

# Allowed Hosts
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dashboard',
    'channels',
]

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Login & Logout URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'trti_dashboard.urls'

AUTH_USER_MODEL = 'dashboard.CustomUser' 

# Templates configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'trti_dashboard.wsgi.application'

# Databases Configuration
DATABASES = {
    'default': {  
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DB_NAME'),
        'USER': os.getenv('MYSQL_DB_USER'),
        'PASSWORD': os.getenv('MYSQL_DB_PASSWORD'),
        'HOST': os.getenv('MYSQL_DB_HOST'),
        'PORT': int(os.getenv('MYSQL_DB_PORT', 3306)),  
    }
}

MONGO_DB_SETTINGS = {
    "DB_NAME": os.getenv("MONGO_DB_NAME"),
    "HOST": os.getenv("MONGO_DB_HOST"),
    "USER": os.getenv("MONGO_DB_USER"),
    "PASSWORD": os.getenv("MONGO_DB_PASSWORD"),
    "PORT": int(os.getenv("MONGO_DB_PORT")),
}

# Power BI Embed URL
POWER_BI_EMBED_URL = os.getenv("POWER_BI_EMBED_URL")

# Session Security
SESSION_ENGINE = "django.contrib.sessions.backends.file"  # Store sessions in file
SESSION_COOKIE_AGE = 3600  # Session expires in 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # Expire session when browser closes
SESSION_COOKIE_SECURE = not DEBUG  # Secure cookies in production
CSRF_COOKIE_SECURE = not DEBUG  # Secure CSRF cookie in production
SESSION_FILE_PATH = os.path.join(BASE_DIR, "django_sessions")  


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static & Media Files
STATIC_URL = '/static/'
STATICFILES_DIRS = [
os.path.join(BASE_DIR, "dashboard/static")
if os.path.exists(os.path.join(BASE_DIR, "dashboard/static"))
    else os.path.join(BASE_DIR, "static")
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Load credentials from .env
USERNAME = os.getenv("LOGIN_USERNAME")
PASSWORD = os.getenv("LOGIN_PASSWORD")

class ReadOnlyMigrations:
    def __contains__(self, item):
        return True  # Tell Django that all apps are in this dictionary

    def __getitem__(self, item):
        return None  # Tell Django that no migrations exist

MIGRATION_MODULES = ReadOnlyMigrations()

DATABASE_ROUTERS = ['database_router.ReadOnlyRouter']

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
