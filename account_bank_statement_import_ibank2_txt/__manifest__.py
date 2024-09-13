# Copyright 2019 ArtLine Ltd <https://artline-erp.ru>, 2019
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Bank Statement Import iBank2',
    'category': 'Accounting',
    'version': '11.0.1.0.1',
    'author': 'ArtLine',
    'website': 'https://artline-erp.ru/modul-import-vypisok-ibank2',
    'depends': [
        'account_bank_statement_import',
    ],
    'data': [
        'wizards/account_bank_statement_import_ibank2_view.xml',
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
