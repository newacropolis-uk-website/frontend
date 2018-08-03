#!/usr/bin/python

import sys
import argparse
import logging
import os

from app.settings import Settings


def get_setting(name):
    return Settings.get_or_set(name)


class Config(object):
    DEBUG = False
    API_BASE_URL = get_setting('API_BASE_URL')
    FRONTEND_BASE_URL = os.environ.get('FRONTEND_BASE_URL')
    ADMIN_CLIENT_ID = get_setting('ADMIN_CLIENT_ID')
    ADMIN_CLIENT_SECRET = get_setting('ADMIN_CLIENT_SECRET')
    SECRET_KEY = get_setting('SECRET_KEY')
    AUTH_USERNAME = get_setting('AUTH_USERNAME')
    AUTH_PASSWORD = get_setting('AUTH_PASSWORD')


class Development(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SESSION_PROTECTION = None
    PORT = 5100


class Preview(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SESSION_PROTECTION = None
    PORT = 4100


class Live(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SESSION_PROTECTION = None
    PORT = 8100


configs = {
    'development': Development,
    # 'test': Test,
    'preview': Preview,
    # 'staging': Staging,
    'live': Live,
    # 'production': Live
}
