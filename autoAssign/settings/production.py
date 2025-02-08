# flake8: noqa

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

import autoAssign
from .base import *
import dj_database_url
import os

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
# SECURITY SETTINGS
# ==============================================================================

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

SECURE_HSTS_SECONDS = 60 * 60 * 24 * 7 * 52  # one year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SESSION_COOKIE_SECURE = True


# Enable WhiteNoise to serve static files directly
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ==============================================================================
# EMAIL SETTINGS
# ==============================================================================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='contact.johnjlawal@gmail.com')

# ==============================================================================
# THIRD-PARTY APPS SETTINGS
# ==============================================================================

# sentry_sdk.init(
#     dsn=config("SENTRY_DSN", default=""),
#     environment=SPS_ENVIRONMENT,
#     release="sps@%s" % sps_project.__version__,
#     integrations=[DjangoIntegration()],
# )