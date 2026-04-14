# backend/config/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS for both development and production
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# Add Railway backend domain from environment variable
RAILWAY_DOMAIN = os.getenv('RAILWAY_DOMAIN')
if RAILWAY_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_DOMAIN)

# Add any custom backend domain
BACKEND_DOMAIN = os.getenv('BACKEND_DOMAIN')
if BACKEND_DOMAIN:
    ALLOWED_HOSTS.append(BACKEND_DOMAIN)

# ─── Installed Apps ───────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party packages
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',

    # Our apps — note the apps/ folder prefix
    'apps.users',
    'apps.products',
    'apps.cart',
    'apps.orders',
]

# In INSTALLED_APPS, add whitenoise storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS must be near the top
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# ─── Database ─────────────────────────────────────────────────────────────────
import dj_database_url

DATABASE_URL = os.getenv('DATABASE_URL')

if DATABASE_URL:
    # Production: Use DATABASE_URL from Railway
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
            ssl_require=False,
        )
    }
else:
    # Development: Use individual environment variables
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME', 'techzone_db'),
            'USER': os.getenv('DB_USER', 'postgres'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '5432'),
        }
    }

# ─── Custom User Model ────────────────────────────────────────────────────────
# This MUST be set before the first migration
AUTH_USER_MODEL = 'users.CustomUser'

# ─── Django REST Framework ────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

# ─── JWT Settings ─────────────────────────────────────────────────────────────
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES' : ('rest_framework_simplejwt.tokens.AccessToken',),
}

# Tell simplejwt to use email as the login field
SIMPLE_JWT_USER_ID_FIELD = 'email'

# ─── CORS Settings ────────────────────────────────────────────────────────────
# Allows frontend (React) to call this Django backend from different domains
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]

# Add production frontend URL from environment variable if it exists
FRONTEND_URL = os.getenv('FRONTEND_URL')
if FRONTEND_URL:
    # Clean up URL (remove trailing slash if any)
    frontend_url = FRONTEND_URL.rstrip('/')
    CORS_ALLOWED_ORIGINS.append(frontend_url)
    # Also add with https prefix if it's not already there (for Railway compatibility)
    if not frontend_url.startswith('https://') and not frontend_url.startswith('http://'):
        CORS_ALLOWED_ORIGINS.append(f'https://{frontend_url}')

# Enable credentials for JWT authentication
CORS_ALLOW_CREDENTIALS = True

# Expose headers that frontend might need
CORS_EXPOSE_HEADERS = [
    'Content-Type',
    'X-CSRFToken',
]

# ─── Password Validation ──────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# This tells simplejwt's TokenObtainPairView to accept 'email' not 'username'
SIMPLE_JWT['USER_ID_FIELD'] = 'id'

# backend/config/settings.py  (add at the bottom)
RAZORPAY_KEY_ID     = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')


# backend/config/settings.py
# Add at the bottom

import os

# ── Production security settings ──────────────────────────────────────────────
# These only apply when DEBUG=False (production)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER       = True
    SECURE_CONTENT_TYPE_NOSNIFF     = True
    X_FRAME_OPTIONS                 = 'DENY'
    SESSION_COOKIE_SECURE           = True
    CSRF_COOKIE_SECURE              = True

STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Include frontend dist folder so React assets are served
STATICFILES_DIRS = [
    os.path.join(os.path.dirname(BASE_DIR), 'frontend', 'dist'),
]