from odoo import api, fields, models


class Company(models.Model):
    _inherit = "res.company"

    is_ip = fields.Boolean("Индивидуальный предприниматель", default=False)
    is_self_employed = fields.Boolean("Самозанятый", default=False)

    @api.onchange("is_ip")
    def _onchange_is_ip(self):
        if self.is_ip:
            self.is_self_employed = False

    @api.onchange("is_self_employed")
    def _onchange_is_self_employed(self):
        if self.is_self_employed:
            self.is_ip = False
