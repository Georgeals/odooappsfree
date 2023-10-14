# -*- coding: utf-8 -*-
##############################################################################
#
#    ArtLineStudio Ltd.
#    Copyright (C) 2021-TODAY ArtLineStudio <https://artlinespb.ru/>.
#    Author: George Yanguzov <george@artlinespb.ru>
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
    'name': 'Mail Server Smtp Yandex',
    'version': '11.0.0.1',
    'category': 'Social Network',
    'description': """
Send email from Yandex SMTP server and others.

Fixed error:

SMTPSenderRefused: 553

5.7.1 Sender address rejected: not owned by auth user.

Module search smtp server whit user name matches sender address mail header "From" 
If smtp server not found, then replace address mail header "From" with smtp auth user.

""",
    'author': "ArtLine",
    'company': 'ArtLineStudio LTD',
    'website': "https://artlinespb.ru/",
    'depends': ['base'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
