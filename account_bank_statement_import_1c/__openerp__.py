# Copyright 2019 ArtLine Ltd <http://artlinespb.ru>, 2019
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).               
{
    'name': 'Bank Statement Import 1C',
    'category': 'Accounting',
    'version': '8.0.1.3',
    'author': 'ArtLine',
    'website': 'https://artlinespb.ru/import-bank-statements-1c-format/',
    'summary': "Импорт выписки из 1C",
    'depends': [
        'account',
        'account_bank_statement_import',
    ],
    'description': """
    Импорт выписки из 1С
    """,                     
    'data': [
        'wizards/account_bank_statement_import_1c_view.xml',
    ],
    "images": [
        'static/description/banner.png'
    ],
    "contributors": [
        "ArtLine <george@artlinespb.ru>",
    ],
    'auto_install': False,
    'installable': True
    'license': 'AGPL-3',
    'support': 'george@artlinespb.ru',

}