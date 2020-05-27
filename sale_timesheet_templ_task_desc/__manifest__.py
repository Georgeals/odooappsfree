# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Sales Timesheet template task',
    'category': 'Hidden',
    'summary': 'Modul add templeat task description',
    'description': """
Allows create use template description of task
=============================================

This module auto add description for internal of product to the service task description.
""",
    'website': 'http://artlinespb.ru/',
    'depends': ['sale_timesheet'],
    'installable': True,
    'uninstall_hook': 'uninstall_hook',
}
