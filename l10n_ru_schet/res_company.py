# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models

class Company(models.Model):
    _inherit = 'res.company'

    inn = fields.Char(related='partner_id.inn')
    kpp = fields.Char(related='partner_id.kpp')
    okpo = fields.Char(related='partner_id.okpo')
    chief_id = fields.Many2one('res.users', 'Chief')
    accountant_id = fields.Many2one('res.users', 'General Accountant')
    print_facsimile = fields.Boolean('Print Facsimile', help="Check this for adding Facsimiles of responsible persons to documents.")
    print_stamp = fields.Boolean('Print Stamp', help="Check this for adding Stamp of company to documents.")
    stamp = fields.Binary("Stamp")
    print_anywhere = fields.Boolean('Print Anywhere', help="Uncheck this, if you want add Facsimile and Stamp only in email.", default=True)
    is_ip = fields.Boolean('Индивидуальный предприниматель', default=False)
    is_self_employed = fields.Boolean('Самозанятый', default=False)
    bank_id = fields.Many2one('res.partner.bank', 'Bank account for orders.')

    @api.onchange('is_ip')
    def _onchange_is_ip(self):
        if self.is_ip:
            self.is_self_employed = False

    @api.onchange('is_self_employed')
    def _onchange_is_self_employed(self):
        if self.is_self_employed:
            self.is_ip = False
