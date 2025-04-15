"""
Django settings for teste2 project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
from tasks.validators import MaximumLengthValidator


load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tasks",
]

MIDDLEWARE = [     
    "tasks.middleware.aaaamiddleware.RedirectOldLoginMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "tasks.middleware.aaaamiddleware.RequireLoginMiddleware" 
]

LOGIN_URL = "/authenticate/"  


ROOT_URLCONF = "teste2.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        
        },
    },
]

WSGI_APPLICATION = "teste2.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# # settings.py

# # --- Gmail Email Settings (FOR LOCAL DEVELOPMENT ONLY - DO NOT USE IN PRODUCTION!) ---
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587  # Use 587 for TLS
# EMAIL_USE_TLS = True  # Use TLS (required by Gmail)
# EMAIL_HOST_USER = 'planne.auth@gmail.com'  # Your full Gmail address
# EMAIL_HOST_PASSWORD = 'Uniesp123' # <<< IMPORTANT: Use an APP PASSWORD, NOT your regular Gmail password!

# # Optional: Set a default 'From' address
# DEFAULT_FROM_EMAIL = 'My Django App <your_gmail_address@gmail.com>'

# settings.py

# --- Production Email Settings ---
# Uses environment variables for security. Set these variables on PythonAnywhere.

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = os.getenv('EMAIL_HOST')  # e.g., 'smtp.sendgrid.net' or 'smtp.gmail.com'
# EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587)) # Use 587 for TLS, 465 for SSL, default to 587
# EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true' # Default to True if var missing
# EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL', 'False').lower() == 'true' # Default to False
# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER') # Your SMTP username or API key name
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # Your SMTP password or API key (KEEP SECRET)

# # Optional: Set a default 'From' address
# DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
# # You might want a better default, e.g., using your domain name if available
# # SERVER_EMAIL = DEFAULT_FROM_EMAIL # Often used for error emails from Django itself

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length" : 6,
        }
    },
    # {
    #     'NAME': 'tasks.validators.MaximumLengthValidator', # Update with the correct path to your validator
    #     'OPTIONS': {
    #         'max_length': 8,
    #     }
    # },
    {
        "NAME": "tasks.validators.MaximumLengthValidator",
        "OPTIONS": {
            "max_length": 8,
        }
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

AUTH_USER_MODEL = "tasks.User"


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'tasks', 'static', 'tasks'),
    os.path.join(BASE_DIR, 'tasks', 'static', 'tasks', 'imagens'),
]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# STATIC_URL = "static/"
# STATICFILES_DIR = [
#     os.path.join(BASE_DIR,'tasks','static'),
# ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
