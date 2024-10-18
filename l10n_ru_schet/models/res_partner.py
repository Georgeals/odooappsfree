# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2018 ArtLine (<https://artline-erp.ru/>).
#
##############################################################################

from odoo import api, fields, models

DOC_ADDRESS_FORMAT = '%(street)s\n%(street2)s\n%(city)s %(state_code)s %(zip)s\n%(country_name)s'


class ResPartner(models.Model):
    _inherit = "res.partner"

    vat = fields.Char(string="Tax ID")
    kpp = fields.Char("KPP", size=9)

    def get_full_name_for_schet(self):
        self.ensure_one()
        commercial_partner = self.commercial_partner_id
        full_name = commercial_partner.with_context({"lang": commercial_partner.lang})._get_complete_name() # todo self.env.lang ??????????        
        if commercial_partner.vat:
            full_name += f", ИНН {commercial_partner.vat}"
        if commercial_partner.kpp:
            full_name += f", КПП {commercial_partner.kpp}"
        post_address_format, args = commercial_partner._prepare_display_address(without_company=True)
        address = DOC_ADDRESS_FORMAT % args
        splitted_address = address.split("\n")
        address = ", ".join([n for n in splitted_address if n.strip()])  
        full_name += f", {address}"
        return full_name
