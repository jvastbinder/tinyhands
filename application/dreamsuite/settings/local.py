from .base import *

DEBUG = True

INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE_CLASSES += [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
INSTALLED_APPS.append('debug_toolbar')


SPREADSHEET_NAME = 'Tinyhands'
IRF_WORKSHEET_NAME = 'IRF Entry'
VIF_WORKSHEET_NAME = 'VIF Entry'
ADDRESS2_WORKSHEET_NAME = 'Address2 Export'

IMPORT_ACCOUNT_EMAIL = 'test_sup@example.com'
IMPORT_SPREADSHEET_NAME = 'Tinyhands'
IRF_IMPORT_WORKSHEET_NAME = 'IRF Import'
VIF_IMPORT_WORKSHEET_NAME = 'VIF Import'
