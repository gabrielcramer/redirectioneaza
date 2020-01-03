# -*- coding: utf-8 -*-
"""
This file contains configurations settings for the application
"""

# enviroment vars to set:
# ENVIRONMENT   [DEV|PROD]

# On prod, AWS SSM Parameter Store to set:
# /PROD/ACCESS_KEY
# /PROD/SECRET_KEY
# /PROD/CAPTCHA_PUBLIC_KEY
# /PROD/CAPTCHA_PRIVATE_KEY
# /PROD/DB_USERNAME
# /PROD/DB_PASSWORD
# /PROD/DB_DBSERVER
# /PROD/DB_DBPORT
# /PROD/DB_DBCATALOG


from os import environ, path
from datetime import datetime, date
import boto3

from .handlers.ssm_parameter_store import SSMParameterStore

ENVIRONMENT = environ.get('ENVIRONMENT', 'DEV')
BASEDIR = path.abspath(path.dirname(__file__))

# placeholder for the client that we'll use in prod to read params
ssm_store = {}

class AppBaseConfig:
    # TODO Rethink this once migrated to another object store
    UPLOAD_FOLDER = 'storage'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEMPLATES_AUTO_RELOAD = True

    SERVER_HOST, SERVER_PORT = 'localhost', 5000


class AppDevelopmentConfig(AppBaseConfig):

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + path.join(BASEDIR, 'database.db')

    SECRET_KEY = environ.get('APP_SECRET_KEY', b'-~s\xd9\x95\xab\x0b\x85w\xfcDT')
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT', b'\x07\xa5\xd2#\xb7\xaf\xca^\x0bH\tN')

    USER_FORMS = '/storage/'

    CAPTCHA_PUBLIC_KEY = "6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI"
    CAPTCHA_PRIVATE_KEY = "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe"
    CAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
    CAPTCHA_POST_PARAM = "g-recaptcha-response"

class ProdDevelopmentConfig(AppBaseConfig):

    AWS_ACCESS_KEY_ID = environ.get('AWS_ACCESS_KEY_ID', '')
    AWS_SECRET_ACCESS_KEY = environ.get('AWS_SECRET_ACCESS_KEY', '')
    AWS_REGION = environ.get('AWS_REGION', 'eu-central-1')

    client = boto3.client(
        'ssm',
        region_name=AWS_REGION,
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
    )
    ssm_store = SSMParameterStore(ttl=10, ssm_client=client)

    CAPTCHA_PUBLIC_KEY = ssm_store.get('/PROD/CAPTCHA_PUBLIC_KEY')
    CAPTCHA_PRIVATE_KEY = ssm_store.get('/PROD/CAPTCHA_PRIVATE_KEY')

    BUCKET_NAME = 'redirectioneaza.code4.ro'
    USER_FORMS = '/documents'
    BUCKET_OBJECT_ACL = "public-read"

    CAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"
    CAPTCHA_POST_PARAM = "g-recaptcha-response"

    DB_USERNAME = ssm_store.get('/PROD/DB_USERNAME')
    DB_PASSWORD = ssm_store.get('/PROD/DB_PASSWORD')
    DB_DBSERVER = ssm_store.get('/PROD/DB_DBSERVER')
    DB_DBPORT = ssm_store.get('/PROD/DB_DBPORT')
    DB_DBCATALOG = ssm_store.get('/PROD/DB_DBCATALOG')

    # Set up app configuration
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_DBSERVER}:{DB_DBPORT}/{DB_DBCATALOG}'


CONFIG_BY_NAME = dict(
    DEV=AppDevelopmentConfig,
    PROD=ProdDevelopmentConfig
)

# if we are currently in production
DEV = ENVIRONMENT == 'DEV'

# use this to simulate production
DEV = False

# the year when the site started
# used to create an array up to the current year
START_YEAR = 2016

now = datetime.now()
DONATION_LIMIT = date(now.year, 7, 31)
MONTH_NAMES = ['', 'Ianuarie', 'Februarie', 'Martie', 'Aprilie', 'Mai', 'Iunie', 'Iulie', 'August', 'Septembrie', 'Octombrie', 'Noiembrie', 'Decembrie']

DEV_DEPENDECIES_LOCATION = "/bower_components"

TITLE = "redirectioneaza.ro"

DEFAULT_NGO_LOGO = "/images/logo_bw.png"
