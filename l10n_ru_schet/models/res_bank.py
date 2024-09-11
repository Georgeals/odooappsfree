# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2018 Artline (<https://artline-erp.ru/>).
#
##############################################################################

from odoo import api, fields, models


class Bank(models.Model):
    _inherit = "res.bank"

    corr_acc = fields.Char("Corresponding account", size=64)


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    bank_corr_acc = fields.Char(related="bank_id.corr_acc", readonly=True)
