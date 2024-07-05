# Copyright 2019 ArtLine Ltd <http://artlinespb.ru>, 2019
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Bank Statement Import 1C',
    'category': 'Accounting',
    'version': '10.0.1.3',
    'author': 'ArtLine',
    'website': 'https://artline-erp.ru/modul-import-vypisok-1c',
    'depends': [
        'account_bank_statement_import',
    ],
    'description': """
Импорт выписки из 1C
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
    'installable': True,
    'license': 'AGPL-3',
    'support': 'george@artlinespb.ru',
}