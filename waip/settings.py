import os
import dj_database_url
from decouple import config as config_env


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config_env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config_env('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = [
    'localhost',
    'waip.herokuapp.com',
    'whatamiplaying.rafaelgarciadoblas.com',
    'waip.rafaelgarciadoblas.com',
    'www.waip.rafaelgarciadoblas.com',
    'waip.site',
    'www.waip.site',
]


# Application definition

INSTALLED_APPS = [
    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Extra pip installed apps
    'debug_toolbar',

    # Project specific apps
    'games.apps.GamesConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Extra pip installed app
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Serve Static Files
]

ROOT_URLCONF = 'waip.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Points relatively to the templates directory
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'waip.context_processors.google_analytics_key',
            ],
        },
    },
]

WSGI_APPLICATION = 'waip.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases
# For dj_database_url.config check https://github.com/kennethreitz/dj-database-url
DATABASES = {
    # example mysql://database_user:database_user_passord.siteground.eu/database_name')
    'default': dj_database_url.config(default=config_env('DATABASE_URL'))
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

# Overriding Python for getting DebugBar to work
INTERNAL_IPS = ['127.0.0.1', '0.0.0.0']


# Setup for users uploading files
MEDIA_ROOT = 'media'

MEDIA_URL = '/media/'

# Setup for logins
LOGIN_REDIRECT_URL = 'home'  # Url to redirect after succesful log in

LOGIN_URL = 'login'  # Url to redirect when you are not authenticated and try to access a view that requires it


# Old Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'ERROR',
#             'class': 'logging.FileHandler',
#             'filename': os.path.join(BASE_DIR, 'logs/errors.log'),
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#     },
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}

GOOGLE_ANALYTICS_KEY = config_env('GOOGLE_ANALYTICS_KEY', default='google_analytics_key_placeholder')


SHOWCASE_USER_ID = config_env('SHOWCASE_USER_ID', cast=int)
ADMIN_USER_ID = config_env('ADMIN_USER_ID', cast=int)
