# -*- coding: utf-8 -*-
# Copyright 2019 ArtLine Ltd <http://artlinespb.ru>, 2019
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Russia - Act",
    "version": "17.0.1.1",
    "summary": "Акт выполненных работ",
    "description": """
Модуль добавляет печатную форму 'Акт выполненных работ'.
    """,
    "author": "ArtLine",
    "website": "http://artlinespb.ru",
    "license": "AGPL-3",
    "category": "Localization",
    "sequence": 0,
    "depends": ["sale_management", "l10n_ru_schet"],
    "data": [
        "report/report.xml",
        "report/report_act.xml",
    ],
    "installable": True,
}
