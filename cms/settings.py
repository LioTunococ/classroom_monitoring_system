from pathlib import Path
import os
from django.core.exceptions import ImproperlyConfigured

# Optional error monitoring via Sentry
SENTRY_DSN = os.environ.get('SENTRY_DSN')
SENTRY_TRACES_SAMPLE_RATE = float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '0.0'))
SENTRY_PROFILES_SAMPLE_RATE = float(os.environ.get('SENTRY_PROFILES_SAMPLE_RATE', '0.0'))
if SENTRY_DSN:
    try:
        import sentry_sdk
        from sentry_sdk.integrations.django import DjangoIntegration
        sentry_sdk.init(
            dsn=SENTRY_DSN,
            integrations=[DjangoIntegration()],
            traces_sample_rate=SENTRY_TRACES_SAMPLE_RATE,
            profiles_sample_rate=SENTRY_PROFILES_SAMPLE_RATE,
            send_default_pii=False,
        )
    except Exception:
        # Sentry is optional; do not crash if unavailable
        pass

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = os.environ.get('DJANGO_DEBUG', 'True').lower() == 'true'

# Secret key: require in production
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-secret-key-change-me')
if not DEBUG and not os.environ.get('DJANGO_SECRET_KEY'):
    raise ImproperlyConfigured('DJANGO_SECRET_KEY is required when DEBUG=False')

# Allowed hosts from env (comma-separated). In production, you must set this.
_hosts = os.environ.get('DJANGO_ALLOWED_HOSTS')
if _hosts is not None:
    ALLOWED_HOSTS = [h.strip() for h in _hosts.split(',') if h.strip()]
else:
    ALLOWED_HOSTS = ["*"] if DEBUG else []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'attendance',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cms.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'cms.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Optional: environment-based database (e.g., Postgres) without extra deps
DB_ENGINE = os.environ.get('DJANGO_DB_ENGINE')
if DB_ENGINE:
    DATABASES['default'] = {
        'ENGINE': DB_ENGINE,  # e.g., 'django.db.backends.postgresql'
        'NAME': os.environ.get('DJANGO_DB_NAME', ''),
        'USER': os.environ.get('DJANGO_DB_USER', ''),
        'PASSWORD': os.environ.get('DJANGO_DB_PASSWORD', ''),
        'HOST': os.environ.get('DJANGO_DB_HOST', 'localhost'),
        'PORT': os.environ.get('DJANGO_DB_PORT', ''),
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 5},
    },
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Manila'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'

# Security settings for production
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get('DJANGO_SECURE_SSL_REDIRECT', 'true').lower() == 'true'
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = int(os.environ.get('DJANGO_HSTS_SECONDS', '31536000'))  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = os.environ.get('DJANGO_HSTS_INCLUDE_SUBDOMAINS', 'true').lower() == 'true'
    SECURE_HSTS_PRELOAD = os.environ.get('DJANGO_HSTS_PRELOAD', 'false').lower() == 'true'
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = os.environ.get('DJANGO_REFERRER_POLICY', 'strict-origin-when-cross-origin')
    X_FRAME_OPTIONS = 'DENY'

    # Optional: trust proxy SSL header if behind a reverse-proxy/Load Balancer
    if os.environ.get('DJANGO_SECURE_PROXY_SSL_HEADER', 'false').lower() == 'true':
        SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

    # Optional: CSRF trusted origins (comma-separated URLs)
    _csrf = os.environ.get('DJANGO_CSRF_TRUSTED_ORIGINS')
    if _csrf:
        CSRF_TRUSTED_ORIGINS = [o.strip() for o in _csrf.split(',') if o.strip()]

# Admins for error emails (optional)
_admins = os.environ.get('DJANGO_ADMINS', '')  # comma-separated emails or name<email>
ADMINS = []
if _admins:
    for part in _admins.split(','):
        email = part.strip()
        if not email:
            continue
        # Accept both 'Name <email>' and 'email' formats
        if '<' in email and '>' in email:
            name = email.split('<', 1)[0].strip()
            addr = email[email.find('<')+1:email.find('>')].strip()
            ADMINS.append((name or addr, addr))
        else:
            ADMINS.append((email, email))

# Email backend configuration (optional)
EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST', '')
EMAIL_PORT = int(os.environ.get('DJANGO_EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.environ.get('DJANGO_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.environ.get('DJANGO_EMAIL_USE_TLS', 'true').lower() == 'true'
SERVER_EMAIL = os.environ.get('DJANGO_SERVER_EMAIL', 'cms@localhost')

# Logging: file logs in production, console logs in dev, optional email on errors
LOG_DIR = BASE_DIR / 'logs'
try:
    os.makedirs(LOG_DIR, exist_ok=True)
except Exception:
    # If directory can't be created, keep going; file handler may fail if enabled
    pass

# Compute log file path (avoid duplicating 'logs/logs')
LOG_FILE = LOG_DIR / 'app.log'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] %(levelname)s %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_FILE),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 3,
            'formatter': 'standard',
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': True,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'] if DEBUG else ['file', 'console'],
            'level': 'INFO',
        },
        '': {  # root logger
            'handlers': ['console'] if DEBUG else ['file', 'console'],
            'level': 'INFO',
        },
    },
}

# Enable email on errors only if SMTP and ADMINS configured
if EMAIL_HOST and ADMINS:
    LOGGING['loggers']['django']['handlers'].append('mail_admins')
    LOGGING['loggers']['']['handlers'].append('mail_admins')
