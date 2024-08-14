# -*- coding: utf-8 -*-
##############################################################################
#
#    ArtLineStudio Ltd.
#    Copyright (C) 2020-TODAY ArtLineStudio(<https://artlinespb.ru/>).
#    Author: George Yanguzov(<george@artlinespb.ru>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': "Russian document - Partner act reconciliation",
    'summary': """Russian document - Partner act reconciliation""",
    'description': """Russian document - Partner act reconciliation""",
    'author': "George Yanguzov",
    'company': 'ArtLineStudio LTD',
    'website': "https://artlinespb.ru/",
    'category': 'Accounting',
    'version': '17.0.1.0',
    'depends': ['base', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/account_report_general_ledger_view.xml',
        'views/views.xml',
        'views/res_users_view.xml',
        'views/res_company_view.xml',
        'views/res_partner_view.xml',
        'report/templates.xml',
        'report/templates_without_stamp.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False
}