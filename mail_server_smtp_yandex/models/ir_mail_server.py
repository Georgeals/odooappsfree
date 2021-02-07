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

from odoo import api, models, tools
import re


class IrMailServer(models.Model):
    _inherit = "ir.mail_server"

    @api.model
    def send_email(self, message, mail_server_id=None, smtp_server=None, smtp_port=None,
                   smtp_user=None, smtp_password=None, smtp_encryption=None, smtp_debug=False, smtp_session=None):
                          # Get SMTP Server Details from Mail Server
        # todo начать с проверки сессии

        # search smtp owned by message
        header_from = message.get('From')
        owned_by_mail = re.search('<.*>', header_from).group(0)[1:-1]
        mail_server = self.sudo().search([('smtp_user', '=', owned_by_mail)], limit=1)
        if mail_server.id:
            mail_server_id = mail_server.id
            smtp_session = None
        else:
            # Replace Header
            if smtp_session.user:
                smtp_user = smtp_session.user
            else:
                mail_server = self.sudo().search([], order='sequence', limit=1)
                smtp_user = mail_server.smtp_user
            header_from = re.sub('<.*>', '<%s>' % smtp_user, header_from)
            message.replace_header('From', header_from)

        return super(IrMailServer, self).send_email(message, mail_server_id, smtp_server, smtp_port,
                                                    smtp_user, smtp_password, smtp_encryption, smtp_debug, smtp_session)
