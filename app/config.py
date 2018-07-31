#!/usr/bin/python

import sys
import argparse
import logging
import os

from app.settings import Settings


class Config(object):
    DEBUG = False
    API_BASE_URL = Settings.get_or_set('API_BASE_URL')
    FRONTEND_BASE_URL = os.environ.get('FRONTEND_BASE_URL')
    ADMIN_CLIENT_ID = Settings.get_or_set('ADMIN_CLIENT_ID')
    ADMIN_CLIENT_SECRET = Settings.get_or_set('ADMIN_CLIENT_SECRET')
    SECRET_KEY = Settings.get_or_set('SECRET_KEY')


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
