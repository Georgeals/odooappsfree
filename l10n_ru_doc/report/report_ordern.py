# -*- coding: utf-8 -*-
##############################################################################
#
#    flectra
#    Copyright (C) 2015-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, models
from odoo.addons.l10n_ru_doc.report_helper import QWebHelper

class RuSaleOrderNReport(models.AbstractModel):
    _name = 'report.l10n_ru_doc.report_ordern'

    def get_report_values(self, docids, data=None):
        for record in self:
            docs = self.env['sale.order'].browse(docids)
            return {
                'helper': QWebHelper(),
                'doc_ids': docs.ids,
                'doc_model': 'sale.order',
                'docs': docs
            }
