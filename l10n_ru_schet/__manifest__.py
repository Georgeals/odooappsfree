# -*- coding: utf-8 -*-
# Copyright 2019 ArtLine Ltd <https://artline-erp.ru>, 2019
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Russia - Schet",
    "version": "17.0.0.1.0",
    "summary": "Счет на оплату",
    "description": """
The module for print documents of Russia an invoice for payment.
============================================================
Модуль добавляет печатные формы в оферту/заказ:
    * Счет на оплату. 
    * Счет на оплату с выводом подписей и печати
Выставление счета на сотрудника компании, при этом в счете отображается наименование компании
Поддержка мультикомпаний
    """,
    "author": "ArtLine",
    "website": "https://artline-erp.ru",
    "license": "AGPL-3",
    "category": "Localization",
    "sequence": 0,
    "depends": ["sale_management"],
    "demo": ["data/l10n_ru_doc_demo.xml"],
    "data": [
        "views/res_partner_view.xml",
        "views/res_company_view.xml",
        "views/res_users_view.xml",
        "views/res_bank_view.xml",
        "report/l10n_ru_doc_report.xml",
        "report/templates/report_order.xml",
        "report/templates/report_order_ws.xml",
        "report/templates/basic_templates.xml",
    ],
    "images": ["static/description/banner.png"],
    "css": ["static/src/css/l10n_ru_doc.css"],
    "installable": True,
}
