# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, models
from odoo.addons.l10n_ru_doc.report_helper import QWebHelper

class RuInvoiceReports(models.AbstractModel):
    _name = 'report.l10n_ru_doc.invoice_report'

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        report = Report._get_report_from_name('l10n_ru_doc.invoice_report')
        selected_modules = self.env[report.model].browse(docids)
        docargs = {
            'helper': QWebHelper(),
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': selected_modules,
        }
        print ('===============',docargs)
        return Report.render('l10n_ru_doc.invoice_report', docargs)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: