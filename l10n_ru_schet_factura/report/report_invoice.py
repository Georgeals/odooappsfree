from odoo import api, models


class RuInvoiceReport(models.AbstractModel):
    _name = 'report.l10n_ru_schet_factura.report_invoice'

    def _get_report_values(self, docids, data=None):
        report = self.env['ir.actions.report']._get_report_from_name('l10n_ru_schet_factura.report_invoice')
        obj = self.env[report.model].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': obj,
        }

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        report = Report._get_report_from_name('l10n_ru_schet_factura.report_invoice')
        selected_modules = self.env[report.model].browse(docids)
        docargs = {
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': selected_modules,
        }
        return Report.render('l10n_ru_schet_factura.report_invoice', docargs)
