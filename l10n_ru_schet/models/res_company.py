# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2024 ArtLine (<https://artline-erp.ru/>).
#
##############################################################################
from email.policy import default

from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    inn = fields.Char(related="partner_id.vat")
    kpp = fields.Char(related="partner_id.kpp")
    okpo = fields.Char(related="partner_id.okpo")
    chief_id = fields.Many2one("res.users", "Chief")
    accountant_id = fields.Many2one("res.users", "General Accountant")
    print_facsimile = fields.Boolean(
        "Print Facsimile",
        help="Check this for adding Facsimiles of responsible persons to documents.",
    )
    print_stamp = fields.Boolean(
        "Print Stamp", help="Check this for adding Stamp of company to documents."
    )
    stamp = fields.Binary("Stamp")
    print_anywhere = fields.Boolean(
        "Print Anywhere",
        help="Uncheck this, if you want add Facsimile and Stamp only in email.",
        default=True,
    )
    company_type_ru = fields.Selection(
        [("ip", "IP"), ("self_employed", "Self-Employed")],
        default="ip",
        string="Company Type",
        help="if not a company you can choose IP or Self-Employed",
        required=True,
    )
    partner_is_company = fields.Boolean(related="partner_id.is_company", readonly=False)
    partner_id_for_bank = fields.Many2one(related="partner_id")
    bank_id = fields.Many2one(
        "res.partner.bank",
        "Bank account for orders.",
        domain="[('partner_id', '=', partner_id_for_bank)]",
    )
