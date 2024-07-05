# -*- coding: utf-8 -*-
# Copyright ArtLine Ltd <http://artlinespb.ru>, 2024
# License OPL-1
{
    'name': 'Website editor changes saver.',
    'category': 'Website',
    'version': '10.0.1.1',
    'author': 'ArtLine',
    'website': 'https://artline-erp.ru',
    'depends': [
        'website',
    ],
    'description': """
Модуль сохраняет все изменения внесенные в редакторе сайта.
""",
    'data': [
        'security/ir.model.access.csv',
        'views/website_pages_views.xml',
        'views/website_changes_view.xml',
    ],
    'images': [
        'static/description/icon.png'
    ],
    'installable': True,
    'license': 'LGPL-3',
}