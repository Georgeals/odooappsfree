# -*- coding: utf-8 -*-
# Copyright 2019 ArtLine Ltd <http://artlinespb.ru>, 2019
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Russia - Schet',
    'version': '11.0.1.3',
    'summary': 'Счет на оплату',
    'description': """
The module for print documents of Russia an invoice for payment.
============================================================
Модуль добавляет печатные формы в оферту/заказ:
    * Счет на оплату. 
    * Счет на оплату с выводом подписей и печати
Выставление счета на сотрудника компании, при этом в счете отображается наименование компании
Поддержка мультикомпаний
    """,
    'author': 
        'ArtLine, '
        'CodUP',
    'website': 'http://artlinespb.ru',
    'license': 'AGPL-3',
    'category': 'Localization',
    'sequence': 0,
    'depends': ['sale_management'],
    'demo': ['l10n_ru_doc_demo.xml'],
    'data': [
        'res_partner_view.xml',
        'res_company_view.xml',
        'res_users_view.xml',
        'res_bank_view.xml',
        'l10n_ru_doc_data.xml',
        'report/l10n_ru_doc_report.xml',
        'report/report_order.xml',
        'report/report_order_ws.xml',        
    ],
    'css': ['static/src/css/l10n_ru_doc.css'],
    'installable': True,
}
