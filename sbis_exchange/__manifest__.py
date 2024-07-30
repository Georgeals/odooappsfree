# -*- coding: utf-8 -*-
{
    'name': "Sbis exchange",
    'summary': """Sbis exchange""",
    'description': """Sbis exchange""",
    'author': "George Yanguzov",
    'company': 'ArtLineStudio LTD',
    'website': "https://artlinespb.ru/",
    'category': 'Uncategorized',
    'version': '17.0.0.1.0',
    'depends': ['base', 'account', 'l10n_ru_doc', 'l10n_ru_utd',
                'l10n_ru_schet_factura', 'l10n_ru_act'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_config_setting_views.xml',
        'views/account_invoice_views.xml',
        'wizard/sbis_exchange_view.xml'
    ],
}
