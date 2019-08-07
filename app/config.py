#!/usr/bin/python
from app.settings import Settings


def get_setting(name):
    return Settings.get_or_set(name)


class Config(object):
    DEBUG = False
    API_BASE_URL = get_setting('API_BASE_URL')
    IMAGES_URL = get_setting('IMAGES_URL')
    FRONTEND_BASE_URL = get_setting('FRONTEND_BASE_URL')
    ADMIN_CLIENT_ID = get_setting('ADMIN_CLIENT_ID')
    ADMIN_CLIENT_SECRET = get_setting('ADMIN_CLIENT_SECRET')
    SECRET_KEY = get_setting('SECRET_KEY')
    AUTH_USERNAME = get_setting('AUTH_USERNAME')
    AUTH_PASSWORD = get_setting('AUTH_PASSWORD')
    GOOGLE_OAUTH2_CLIENT_ID = get_setting('GOOGLE_OAUTH2_CLIENT_ID')
    GOOGLE_OAUTH2_CLIENT_SECRET = get_setting('GOOGLE_OAUTH2_CLIENT_SECRET')
    GOOGLE_OAUTH2_REDIRECT_URI = get_setting('GOOGLE_OAUTH2_REDIRECT_URI')
    OAUTHLIB_INSECURE_TRANSPORT = False
    PAYPAL_ACCOUNT = get_setting('PAYPAL_ACCOUNT')
    ACCESS_AREAS = ['admin', 'event', 'email', 'magazine', 'report', 'shop', 'announcement', 'article']
    SUMMARY_LIMIT = 300

    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None


class Development(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SESSION_PROTECTION = None
    OAUTHLIB_INSECURE_TRANSPORT = True


class Preview(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SESSION_PROTECTION = None
    OAUTHLIB_INSECURE_TRANSPORT = True


class Live(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SESSION_PROTECTION = None


configs = {
    'development': Development,
    # 'test': Test,
    'preview': Preview,
    # 'staging': Staging,
    'live': Live,
    # 'production': Live
}
