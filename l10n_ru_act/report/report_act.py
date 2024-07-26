# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2016 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, models

class RuActReport(models.AbstractModel):
    _name = 'report.l10n_ru_act.report_act'

    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('l10n_ru_act.report_act')
        obj = self.env[report.model].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': obj,
            # 'get_label': self.get_label,
            # 'get_date': self.get_date,
        }

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        report = Report._get_report_from_name('l10n_ru_doc.report_act')
        selected_modules = self.env[report.model].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': selected_modules,
        }
        return Report.render('l10n_ru_doc.report_act', docargs)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: