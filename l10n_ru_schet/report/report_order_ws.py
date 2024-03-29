# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, models
from odoo.addons.l10n_ru_schet.report_helper import QWebHelper

class RuSaleOrderReport(models.AbstractModel):
    _name = 'report.l10n_ru_schet.report_order_ws'

    @api.multi
    def get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        return {
            'helper': QWebHelper(),
            'doc_ids': docs.ids,
            'doc_model': 'sale.order',
            'docs': docs
        }