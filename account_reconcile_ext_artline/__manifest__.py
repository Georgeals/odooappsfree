# -*- coding: utf-8 -*-
# Copyright 2024 ArtLine Ltd <http://artlinespb.ru>, 2024
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Block reconcile without partner",
    "version": "11.0.0.1",
    "summary": "Запрет сверки без указания партнера",
    "description": """
    """,
    "author": "ArtLine",
    "website": "http://artlinespb.ru",
    "license": "AGPL-3",
    "category": "Accounting",
    "sequence": 0,
    "depends": ["base", "account", "account_invoicing"],
    "data": [
        "views/account.xml",
    ],
    "installable": True,
}
