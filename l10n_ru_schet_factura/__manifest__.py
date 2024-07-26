# -*- coding: utf-8 -*-
# Copyright 2019 ArtLine Ltd <http://artlinespb.ru>, 2019
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Russia - Schet-Factura",
    "version": "17.0.1.1",
    "summary": "Счет-фактура",
    "description": """
Модуль добавляет печатную форму 'Счет-фактура'.
    """,
    "author": "ArtLine",
    "website": "http://artlinespb.ru",
    "license": "AGPL-3",
    "category": "Localization",
    "sequence": 0,
    "depends": ["sale_management"],
    "data": [
        "report/report_invoice.xml",
        "report/report.xml",
    ],
    "installable": True,
}
