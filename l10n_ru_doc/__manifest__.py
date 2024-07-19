# -*- coding: utf-8 -*-


{
    'name': 'Russia - Documents',
    'version': '3.3',
    'summary': 'Первичные документы',
    'category': 'Localization',
    'sequence': 0,
    'depends': ['sale'],
    'data': [
        'res_company_view.xml',
        'res_users_view.xml',
        'res_partner_view.xml',
        'res_bank_view.xml',
        'account_invoice_view.xml', 
        # 'l10n_ru_doc_data.xml',
        'report/l10n_ru_doc_report.xml',
        'report/report_order.xml',
        'report/report_invoice.xml',
        'report/report_updn.xml',
        'report/report_ordern.xml',
        'report/report_invoicen.xml',
        'report/report_upd.xml',
        'report/report_bill.xml',
        # 'report/report_act.xml',
    ],
    'css': ['static/src/css/l10n_ru_doc.css'],
    'installable': True,
    'application': True,
}
