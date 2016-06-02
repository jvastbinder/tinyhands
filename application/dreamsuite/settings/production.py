from .base import *

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '139.162.52.72', # this needs to be changed to the ip address of the new linode box when we get it
    'tinyhandsdreamsuite.org',
]

ADMINS = (('Ben Duggan', 'benaduggan@gmail.com'))
SITE_DOMAIN = 'tinyhandsdreamsuite.org'

SPREADSHEET_NAME = 'Dream Suite - THN Data'
IRF_WORKSHEET_NAME = 'IRF Entry'
VIF_WORKSHEET_NAME = 'VIF Entry'

IMPORT_ACCOUNT_EMAIL = 'ashishm@tinyhands.org'
IMPORT_SPREADSHEET_NAME = 'Dream Suite - THN Data'
IRF_IMPORT_WORKSHEET_NAME = 'IRF Import'