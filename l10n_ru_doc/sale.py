# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def print_quotation(self):
        for record in self:
            record.filtered(lambda s: s.state == 'draft').write({'state': 'sent'})
            return self.env['report'].get_action(record, 'l10n_ru_doc.report_order')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: