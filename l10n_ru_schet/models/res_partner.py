# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2018 ArtLine (<https://artline-erp.ru/>).
#
##############################################################################

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    vat = fields.Char(string="Tax ID", translate=True)
    kpp = fields.Char("KPP", size=9)
    okpo = fields.Char("OKPO", size=14)

    def get_address_for_schet(self):
        self.ensure_one()
        name = self.with_context({"lang": self.env.lang})._get_complete_name()
        if vat := self.vat:
            name += f", ИНН {vat}"
        if kpp := self.kpp:
            name += f", КПП {kpp}"
        if address := self._display_address(without_company=True):
            name += f", {address}"
        return name
