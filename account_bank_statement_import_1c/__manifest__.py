# Copyright 2019 ArtLine Ltd <http://artlinespb.ru>, 2019
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Bank Statement Import 1C',
    'category': 'Accounting',
    'version': '11.0.1.0.2',
    'author': 'ArtLine',
    'website': 'https://artlinespb.ru/import-bank-statements-1c-format/',
    'depends': [
        'account_bank_statement_import',
        'account_invoicing',
    ],
    'data': [
        'wizards/account_bank_statement_import_1c_view.xml',
    ],
    "images": [
        'static/description/banner.png'
    ],
    "contributors": [
        "ArtLine <george@artlinespb.ru>",
    ],
    'installable': True,
    'license': 'AGPL-3',
    'support': 'george@artlinespb.ru',
}
