from odoo import models
from odoo.tools import formatLang


class AccountMove(models.Model):
    _inherit = "account.move"

    def use_formatlang(self, value, currency):
        env = self.env
        return formatLang(env, value, currency_obj=currency)
