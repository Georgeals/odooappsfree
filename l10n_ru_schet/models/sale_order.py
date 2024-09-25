from odoo import models
from odoo.tools import formatLang


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def use_formatlang(self, value, currency):
        env = self.env
        return formatLang(env, value, currency_obj=currency)
