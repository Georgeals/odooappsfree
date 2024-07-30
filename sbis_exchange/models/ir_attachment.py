# -*- coding: utf-8 -*-
##############################################################################
#
#    ArtLineStudio Ltd.
#    Copyright (C) 2021-TODAY ArtLineStudio(<https://artlinespb.ru/>).
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

# from odoo import models, fields, _
from odoo import models, _
from odoo.exceptions import UserError


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def unlink(self):
        # OVERRIDE
        linked_edi_documents = self.env['account.edi.document'].search([('attachment_id', 'in', self.ids)])
        if linked_edi_documents:
            raise UserError(_("You can't unlink an attachment being an EDI document."))
        return super(IrAttachment, self).unlink()
