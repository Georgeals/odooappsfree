# -*- coding: utf-8 -*-
# Copyright ArtLineStudio LTD <https://artline-erp.ru>, 2025
# License LGPL-3 (see https://www.odoo.com/documentation/18.0/legal/licenses.html#lgpl-3)
{
    "name": "Печатная форма счета.",
    "version": "16.0.1.0.0",
    "category": "Sale",
    "summary": "",
    "description": """
    """,
    "author": "ArtLineStudio LTD",
    "website": "https://artline-erp.ru",
    "depends": ["sale_management", "sale"],
    "external_dependencies": {
        "python": ["pytils"],
    },
    "data": [
        "report/ir_actions_report.xml",
        "report/report_order.xml",
        "views/res_bank_view.xml",
        "views/res_company_view.xml",
        "views/res_partner_view.xml",
        "views/res_users_view.xml",
        "data/mail_template_data.xml",
        "data/sale_order_data.xml",
    ],
    "installable": True,
    "license": "LGPL-3",
}
