# Defualt
from pathlib import Path
# Custom
import django_heroku
import json
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

if os.path.exists('production/config.json'):
    with open('production/config.json') as json_file:
        data = json.load(json_file)
        #Core
        SECRET_KEY = data['SECRET_KEY']
        # Email
        EMAIL_HOST_USER = data['EMAIL_HOST_USER']
        EMAIL_HOST_PASSWORD = data['EMAIL_HOST_PASSWORD']
        DEFAULT_FROM_EMAIL = data['DEFAULT_FROM_EMAIL']
        EMAIL_HOST = data['EMAIL_HOST']
        # Database

else:
    # Core
    SECRET_KEY = os.environ.get('SECRET_KEY')
    # Email
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
    EMAIL_HOST = os.environ.get('EMAIL_HOST')




debug = os.environ.get('DEBUG')
if debug == 'True':
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = []

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # "Sites" framework
    "django.contrib.sites",


    #project apps   
    'events_registry',
    'users',

    #Third party
    'django_extensions',
    'widget_tweaks',
]

AUTH_USER_MODEL = 'users.Member'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'moske.urls'
MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'events_registry/templates'),
                os.path.join(BASE_DIR, 'users/templates')],
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

WSGI_APPLICATION = 'moske.wsgi.application'


#Login
LOGIN_URL = '/users/login'

# Static 
STATIC_URL = '/static/'

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')



# Database
DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mvwqwifm',
        'USER':'mvwqwifm',
        'PASSWORD':'M-W5bKCHzw3TNQ6f622VURJbS43ci-PN',
        'HOST':'hattie.db.elephantsql.com',
        'port':'5432'
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Email configration
EMAIL_PORT = 465
EMAIL_USE_SSL = True
EMAIL_USE_TLS = False


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Oslo'

USE_I18N = True

TIME_FORMAT = 'H:i'

USE_L10N = False

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

django_heroku.settings(locals())

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'