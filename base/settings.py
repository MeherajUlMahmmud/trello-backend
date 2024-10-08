import datetime
import os
from pathlib import Path

from decouple import config

from base.log_filters import ExcludeStatReloaderFilter, TraceIDFilter

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = os.path.join(BASE_DIR, 'logs')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

SECRET_KEY = config('SECRET_KEY')

ENVIRONMENT = config('ENV', default='development')

DEBUG = config('DEBUG', default=False, cast=bool)

CORS_ORIGIN_ALLOW_ALL = True
SERVER_URL = config('SERVER_URL', default="http://localhost:8000")
MAX_UPLOAD_SIZE = 5242880  # 5MB

ALLOWED_HOSTS = [
    '*'
]


# Application definition
INSTALLED_APPS = [
    'common.apps.CommonConfig',
    'user_control.apps.UserControlConfig',
    'workspace_control.apps.WorkspaceControlConfig',
    'board_control.apps.BoardControlConfig',

    # Third Party
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',
    "django_filters",
    "jazzmin",
    'corsheaders',
    'import_export',
    'rest_framework_swagger',  # Swagger
    'drf_yasg',  # Yet Another Swagger generator
    'django_extensions',

    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    # Third Party
    'corsheaders.middleware.CorsMiddleware',

    # Custom
    'base.middleware.RequestLogMiddleware',
    'base.middleware.TraceIDMiddleware',

    # Django
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Third Party
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

AUTH_USER_MODEL = "user_control.UserModel"

ROOT_URLCONF = 'base.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'base.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Database
DB_ENGINE = config('DB_ENGINE')

DEV_DB_NAME = config('DEV_DB_NAME', default='')
DEV_DB_USER = config('DEV_DB_USER', default='')
DEV_DB_PASSWORD = config('DEV_DB_PASSWORD', default='')
DEV_DB_HOST = config('DEV_DB_HOST', default='')
DEV_DB_PORT = config('DEV_DB_PORT', default='')

TEST_DB_NAME = config('TEST_DB_NAME', default='')
TEST_DB_USER = config('TEST_DB_USER', default='')
TEST_DB_PASSWORD = config('TEST_DB_PASSWORD', default='')
TEST_DB_HOST = config('TEST_DB_HOST', default='')
TEST_DB_PORT = config('TEST_DB_PORT', default='')

PROD_DB_NAME = config('PROD_DB_NAME', default='')
PROD_DB_USER = config('PROD_DB_USER', default='')
PROD_DB_PASSWORD = config('PROD_DB_PASSWORD', default='')
PROD_DB_HOST = config('PROD_DB_HOST', default='')
PROD_DB_PORT = config('PROD_DB_PORT', default='')

DB_NAME = DEV_DB_NAME if ENVIRONMENT == 'development' else TEST_DB_NAME if ENVIRONMENT == 'test' else PROD_DB_NAME
DB_USER = DEV_DB_USER if ENVIRONMENT == 'development' else TEST_DB_USER if ENVIRONMENT == 'test' else PROD_DB_USER
DB_PASSWORD = DEV_DB_PASSWORD if ENVIRONMENT == 'development' else TEST_DB_PASSWORD if ENVIRONMENT == 'test' else PROD_DB_PASSWORD
DB_HOST = DEV_DB_HOST if ENVIRONMENT == 'development' else TEST_DB_HOST if ENVIRONMENT == 'test' else PROD_DB_HOST
DB_PORT = DEV_DB_PORT if ENVIRONMENT == 'development' else TEST_DB_PORT if ENVIRONMENT == 'test' else PROD_DB_PORT

DATABASES = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# LOGGING
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'exclude_state_reloader': {
            '()': ExcludeStatReloaderFilter,
        },
        'trace_id_filter': {
            '()': TraceIDFilter,
        },
    },
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {trace_id} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {trace_id} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'filters': ['exclude_state_reloader', 'trace_id_filter'],
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'verbose',
            'when': 'midnight',  # Rotate logs at midnight
            'interval': 1,  # Rotate daily
            'backupCount': 30,  # Keep logs for 30 days
        },
        'console': {
            'class': 'logging.StreamHandler',
            'filters': ['trace_id_filter'],
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': 'INFO',
    },
}


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configure Django Jazzmin
JAZZMIN_SETTINGS = {
    'site_title': 'Trello',
    'site_header': 'Trello',
    'welcome_sign': 'Welcome to Trello',
    'user_avatar': None,
    # 'topmenu_links': [
    #     {'name': 'Home', 'url': 'admin:index', 'permissions': ['auth.view_user']},
    #     {'name': 'Settings', 'url': 'admin:app_list', 'permissions': ['auth.view_user']},
    # ],
    'show_ui_builder': True,
    'navigation_expanded': True,
    'hide_apps': [],
    'hide_models': [],
    'related_modal_active': False,
    'custom_css': None,
    'custom_js': None,
    'show_drug_title': True,
    'drug_title': 'Trello',
    'site_url': 'https://api.tiger11.pro/',
    'show_full_screen': True,
    # 'changeform_format': 'horizontal_tabs',
    # 'changeform_format_overrides': {
    #     'auth.user': 'vertical_tabs',
    # },
    'theme': 'default',
    'icon_theme': 'default',
    'default_icon_parents': 'fas fa-fw fa-folder',
    'default_icon_children': 'fas fa-fw fa-file',
}

# Configure Django CORS Headers
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_WHITELIST = [
    'http://localhost:8000',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
    'http://127.0.0.1:8000',
]

# Configure Django Import Export
IMPORT_EXPORT_USE_TRANSACTIONS = True
IMPORT_EXPORT_SKIP_ADMIN_LOG = True
IMPORT_EXPORT_IMPORT_PERMISSION_CODE = 'import_export.import_data'
IMPORT_EXPORT_EXPORT_PERMISSION_CODE = 'import_export.export_data'
IMPORT_EXPORT_RESOURCE_CLASS = 'import_export.resources.ModelResource'

# Configure Django Rest Framework
REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY': 'error',
    'COERCE_DECIMAL_TO_STRING': False,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DATETIME_INPUT_FORMATS': ['%Y-%m-%d %H:%M', '%Y-%m-%d'],
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M',  # For Am/Pm: %Y-%m-%d %I:%M %p
}

# Configure Django Rest Framework Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(hours=12),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=1),

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Configure Django Rest Framework Swagger
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

# Configure the Debug Toolbar
if DEBUG:
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

    DEBUG_TOOLBAR_PANELS = [
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.profiling.ProfilingPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
    ]
    INTERNAL_IPS = [
        # Add your IP address(es) for accessing the toolbar
        '127.0.0.1',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }

# Configure the WhiteNoise
WHITENOISE_AUTOREFRESH = True
