# -*- coding: utf-8 -*-
from odoo import models, fields


class ResCountryState(models.Model):
    _inherit = 'res.country.state'

    tax_regional_code = fields.Char(string='Tax Code')
