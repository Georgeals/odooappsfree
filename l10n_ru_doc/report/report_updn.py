# -*- coding: utf-8 -*-
##############################################################################
#
#    flectra
#    Copyright (C) 2015-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, models
from odoo.addons.l10n_ru_doc.report_helper import QWebHelper


class RuUpdNReport(models.AbstractModel):
    _name = 'report.l10n_ru_doc.report_updn'

    def get_report_values(self, docids, data=None):
        for record in self:
            docs = self.env['account.invoice'].browse(docids)
            return {
                'helper': QWebHelper(),
                'doc_ids': docs.ids,
                'doc_model': 'account.invoice',
                'docs': docs
            }
