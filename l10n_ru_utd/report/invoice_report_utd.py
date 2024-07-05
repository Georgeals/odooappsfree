# -*- coding: utf-8 -*-
##############################################################################
#
#    ArtLineStudio Ltd.
#    Copyright (C) 2020-TODAY ArtLineStudio(<https://artline-erp.ru/>).
#    Author: George Yanguzov(<george@artlinespb.ru>)
#
##############################################################################

from datetime import datetime

from odoo import api, models

from odoo.addons.l10n_ru_utd.report_helper import QWebHelper


class InvoiceReportUTD(models.AbstractModel):
    _name = 'report.l10n_ru_utd.invoice_report_utd'

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        report = Report._get_report_from_name('l10n_ru_utd.invoice_report_utd')
        selected_modules = self.env[report.model].browse(docids)
        docargs = {
            'helper': QWebHelper(),
            'get_label':self.get_label,
            'get_date':self.get_date,
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': selected_modules,
        }
        # print ('===============',docargs)
        return Report.render('l10n_ru_utd.invoice_report_utd', docargs)

    @api.multi
    def get_label(self, invoice):
        #_logger.info("SIMBA%s"%(invoice.partner_id.parent_name))

        if invoice.partner_id.parent_name == False:
            name = invoice.partner_id.name
        else:
            name = invoice.partner_id.parent_name
        bank_statement = self.env['account.bank.statement'].search([('company_id','=',invoice.company_id.id)])
        result = ''
        #_logger.info("SIMBASIMBA%s"%(invoice.payment_move_line_ids[0].name))
        #_logger.info("SIMBASIMBA%s"%(invoice.payment_move_line_ids[1].name))

        for payment in invoice.payment_move_line_ids:
            move_line = payment.move_id.line_ids[0]
            
            result = result + str(move_line.name) + ' от ' + str(datetime.strptime(move_line.date,'%Y-%m-%d').strftime('%d.%m.%Y')) + ','
     
 
        #for payment in invoice.payment_ids:
            #for move_line in payment.move_line_ids:
            #move_line = payment.move_line_ids[0]
            #result = result + '№ '+str(move_line.name) + ' от ' + str(datetime.strptime(move_line.date,'%Y-%m-%d').strftime('%d.%m.%Y')) + ','

        #for payment in invoice.payment_ids:
            #for line in bank_statement:
                #if line.all_lines_reconciled:
                    #for item in line.line_ids:
                        #if (item.partner_id.name == name):
                            #_logger.info("SIMBA%s,%s"%(payment.amount,item.amount))
                            #if (payment.amount == item.amount):
                                #result = result + '№ '+str(item.name) + ' от ' + str(datetime.strptime(item.date,'%Y-%m-%d').strftime('%d.%m.%Y')) + ','
        if result == '':
            return ''
        else:
            return result[0:len(result)-1]
    @api.multi
    def get_date(self,invoice):
        bank_statement = self.env['account.bank.statement'].search([('company_id','=',invoice.company_id.id)])
        for line in bank_statement:
            if line.all_lines_reconciled:
                for item in line.line_ids:
                    if item.partner_id.name == invoice.partner_id.parent_name:
                        return datetime.strptime(item.date,'%Y-%m-%d').strftime('%d.%m.%Y')
        return ' '


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: