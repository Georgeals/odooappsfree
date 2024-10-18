# -*- encoding: utf-8 -*-
# Copyright ArtLineStudio Ltd, 2019 (<https://artline-erp.ru>)
# Author: George Yanguzov <info@artline-erp.ru>
# License AGPL-3.0 or later (<http://www.gnu.org/licenses/agpl>).

{
    'name': 'Bank Statement Import 1C',
    'category': 'Accounting',
    'version': '11.0.1.1.2',
    'author': 'ArtLine',
    'website': 'https://artline-erp.ru/modul-import-vypisok-1c',
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
        "ArtLine <info@artline-erp.ru>",
    ],
    'installable': True,
    'license': 'AGPL-3',
    'support': 'info@artline-erp.ru',
}
