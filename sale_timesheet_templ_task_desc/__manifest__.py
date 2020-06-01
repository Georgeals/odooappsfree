# -*- coding: utf-8 -*-
# Copyright 2019 ArtLine Ltd <http://artlinespb.ru>, 2019
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Timesheet template task',
    'category': 'Hidden',
    'version': '11.0.1.0.1',  
    'author': 'ArtLine',    
    'summary': 'Module add templeat of task description',
    'description': """
Allows create and use template description of task
=============================================
This module auto add description for internal of product to the service task description.
""",
    'website': 'http://artlinespb.ru/',
    'images': ['static/description/banner.png'],    
    'depends': ['sale_timesheet'],
    'installable': True,
    'license': 'AGPL-3',
    'support': 'george@artlinespb.ru',
    "contributors": ["ArtLine <george@artlinespb.ru>"],
}