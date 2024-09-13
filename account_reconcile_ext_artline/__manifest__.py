# -*- coding: utf-8 -*-
# Copyright 2024 ArtLine Ltd <https://artline-erp.ru>, 2024
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Block reconcile without partner",
    "version": "11.0.0.1",
    "summary": "Запрет сверки без указания партнера",
    "description": """
    """,
    "author": "ArtLine",
    "website": "https://artline-erp.ru",
    "license": "AGPL-3",
    "category": "Localization",  # todo: Категория неправильная. В задачах "добавления функций в других модулях" категорию можно подсмотреть в расширяемом модуле т.е. в account
    "sequence": 0,
    "depends": ["base", "account", "account_invoicing"],
    "data": [
    ],
    "installable": True,
}
