import logging

from boogie.configurations import DjangoConf, env
from .apps import InstalledAppsConf
from .celery import CeleryConf
from .constance import ConstanceConf
from .middleware import MiddlewareConf
from .options import EjOptions
from .paths import PathsConf
from .security import SecurityConf
from .themes import ThemesConf
from .. import fixes

log = logging.getLogger('ej')


class Conf(ThemesConf,
           ConstanceConf,
           MiddlewareConf,
           CeleryConf,
           SecurityConf,
           PathsConf,
           InstalledAppsConf,
           DjangoConf,
           EjOptions):
    """
    Configuration class for the EJ platform.

    Settings are created as attributes of a Conf instance and injected in
    the global namespace.
    """

    def get_using_sqlite(self):
        return 'sqlite3' in self.DATABASE_DEFAULT['ENGINE']

    def get_using_postgres(self):
        return 'postgresql' in self.DATABASE_DEFAULT['ENGINE']

    USING_DOCKER = env(False, name='USING_DOCKER')

    #
    # Accounts
    #
    AUTH_USER_MODEL = 'ej_users.User'
    ACCOUNT_AUTHENTICATION_METHOD = 'email'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_UNIQUE_EMAIL = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_USER_MODEL_USERNAME_FIELD = None
    LOGIN_REDIRECT_URL = '/'
    SOCIALACCOUNT_PROVIDERS = {
        'facebook': {
            'SCOPE': ['email'],
            'METHOD': 'js_sdk'  # instead of 'oauth2'
        }
    }

    # MANAGER CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
    MANAGERS = ADMINS = [
        ('Bruno Martin, Luan Guimarães, Ricardo Poppi, Henrique Parra', 'bruno@hacklab.com.br'),
        ('Laury Bueno', 'laury@hacklab.com.br'),
    ]

    #
    # Third party modules
    #
    MIGRATION_MODULES = {
        'sites': 'ej.contrib.sites.migrations'
    }

    AUTHENTICATION_BACKENDS = [
        'rules.permissions.ObjectPermissionBackend',
        'django.contrib.auth.backends.ModelBackend',
        'allauth.account.auth_backends.AuthenticationBackend',
    ]

    EJ_CONVERSATIONS_URLMAP = {
        'conversation-detail': '/conversations/{conversation.slug}/',
        'conversation-list': '/conversations/',
    }

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.TokenAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
        'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ),
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 50,
        'DEFAULT_VERSION': 'v1',
    }

    DEBUG = True
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {
                'min_length': 4,
            }
        },
    ]
    BOOGIE_REST_API_SCHEMA = 'https'

    # REST_AUTH_REGISTER_SERIALIZERS = {
    #     'REGISTER_SERIALIZER': 'ej_users.serializers.RegistrationSerializer'
    # }
    PUSH_NOTIFICATIONS_SETTINGS = {'FCM_API_KEY': ''}

    # TODO: Fix this later in boogie configuration stack
    # Required for making django debug toolbar work
    ENVIRONMENT = 'local'
    if ENVIRONMENT == 'local':

        INTERNAL_IPS = [*globals().get('INTERNAL_IPS', ()), '127.0.0.1']

        # Django CORS
        CORS_ORIGIN_ALLOW_ALL = True
        CORS_ALLOW_CREDENTIALS = True
        CORS_ORIGIN_REGEX_WHITELIST = (r'^(http://)?localhost:\d{4,5}$',)

        CSRF_TRUSTED_ORIGINS = [
            'localhost:8000',
            'localhost:3000',
            'localhost:8081',
        ]

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'besouro-local',
                'USER': 'besouro',
                'PASSWORD': '',
                'HOST': 'localhost',
                'PORT': '5432'
            }
        }

        X_FRAME_OPTIONS = 'ALLOW-FROM http://localhost:3000'

        ACCOUNT_EMAIL_VERIFICATION = 'optional'
        EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    if ENVIRONMENT == 'dev':
        # TODO: check if this header fix the http issue.
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

        INTERNAL_IPS = [*globals().get('INTERNAL_IPS', ()), '127.0.0.1']

        # Django CORS
        CORS_ORIGIN_ALLOW_ALL = False
        CORS_ALLOW_CREDENTIALS = True
        CORS_ORIGIN_WHITELIST = (
            'dev.besouro.ejplatform.org',
            'admin.dev.besouro.ejplatform.org',
        )

        CSRF_TRUSTED_ORIGINS = [
            'dev.besouro.ejplatform.org',
            'admin.dev.besouro.ejplatform.org',
        ]

        X_FRAME_OPTIONS = 'DENY'

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'besouro-local',
                'USER': 'besouro',
                'PASSWORD': '',
                'HOST': 'besouro_dev_db',
                'PORT': '5432'
            }
        }

        ALLOWED_HOSTS = ['dev.besouro.ejplatform.org',
                         'admin.dev.besouro.ejplatform.org',
                         '18.222.20.172']

        ACCOUNT_EMAIL_VERIFICATION = 'none'
        EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
        #ANYMAIL = {'MAILGUN_API_KEY': ''}
        DEFAULT_FROM_EMAIL = "Unidos Contra a Corrupção <noreply@unidoscontraacorrupcao.org.br>"

    if ENVIRONMENT == 'prod':
        INTERNAL_IPS = [*globals().get('INTERNAL_IPS', ()), '127.0.0.1']

        # Django CORS
        CORS_ORIGIN_ALLOW_ALL = False
        CORS_ALLOW_CREDENTIALS = True
        CORS_ORIGIN_WHITELIST = (
            'app.unidoscontraacorrupcao.org.br',
            'admin.besouro.ejplatform.org',
        )

        CSRF_TRUSTED_ORIGINS = [
            'app.unidoscontraacorrupcao.org.br',
            'admin.besouro.ejplatform.org',
        ]

        X_FRAME_OPTIONS = 'DENY'

        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'besouro-local',
                'USER': 'besouro',
                'PASSWORD': '',
                'HOST': 'besouro_prod_db',
                'PORT': '5432'
            }
        }

        ALLOWED_HOSTS = ['app.unidoscontraacorrupcao.org.br',
                         'admin.besouro.ejplatform.org',
                         '18.222.20.172']

        DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000
        ACCOUNT_EMAIL_VERIFICATION = 'optional'
        EMAIL_BACKEND = 'anymail.backends.mailgun.EmailBackend'
        #ANYMAIL = {'MAILGUN_API_KEY': ''}
        DEFAULT_FROM_EMAIL = "Unidos Contra a Corrupção <noreply@unidoscontraacorrupcao.org.br>"

Conf.save_settings(globals())
#
# Apply fixes and wait for services to start
#
fixes.apply_all()
