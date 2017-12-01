from .base import *

DEBUG = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS += [
    'corsheaders',
]

MIDDLEWARE_CLASSES += [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

SPREADSHEET_CONFIG = {
    'IRF': {
        'key_column' : 'IRF Number',
        'export': {
            'spreadsheet': 'Tinyhands',
            'sheet':'IRF Entry',
            'export_function': 'export_import.irf_io.get_irf_export_rows',
            },
        'import': {
            'spreadsheet':'Tinyhands',
            'sheet':'IRF Import',
            'import_function': 'export_import.irf_io.import_irf_row',
            'status_column': 'Import Status',
            'issue_column': 'Import Issues',
            },
        },
    'IRF_STORY': {
        'key_column' : 'IRF Number',
        'export': {
            'spreadsheet': 'Tinyhands Story',
            'sheet':'IRFs',
            'export_function': 'export_import.irf_io.get_irf_export_rows',
            },
        },               
    'STORY': {
        'read': {
            'spreadsheet': 'Tinyhands Story',
            'sheet':'Stories',
            },
        },
    'VIF': {
        'key_column': 'VIF Number',
        'export': {
            'spreadsheet':'Tinyhands VIFs',
            'sheet':'VIF Entry',
            'export_function': 'export_import.vif_io.get_vif_export_rows',
            },
        'import': {
            'spreadsheet':'Tinyhands VIFs',
            'sheet':'VIF Import',
            'import_function': 'export_import.vif_io.import_vif_row',
            'status_column': 'Import Status',
            'issue_column': 'Import Issues',
            },
        },
    'ADDRESS2': {
        'replace': {
            'spreadsheet':'Tinyhands',
            'sheet':'Address2 Export',
            }
        },
    'TEST_GoogleSheetExportBase': {
        'edit': {
            'spreadsheet': 'TestSpreadsheet',
            'sheet':'TestExportBase',
            }
        },
    'TEST_GoogleSheetImportBase': {
        'edit': {
            'spreadsheet': 'TestSpreadsheet',
            'sheet':'TestImportBase',
            }
        },
    'TEST_GoogleSheetBasic': {
        'edit': {
            'spreadsheet': 'TestSpreadsheet',
            'sheet':'TestExport',
            }
        },
    'TEST_GoogleSheet': {
        'key_column': 'The Key',
        'export': {
            'spreadsheet':'TestSpreadsheet',
            'sheet':'TestExport',
            'export_function': 'export_import.test.test_google_sheet_basic.export_row',
            },
        'import': {
            'spreadsheet':'TestSpreadsheet',
            'sheet':'TestImport',
            'import_function': 'export_import.vtest.test_google_sheet.import_row',
            'status_column': 'Import Status',
            'issue_column': 'Import Issues',
            }
        },
    }
