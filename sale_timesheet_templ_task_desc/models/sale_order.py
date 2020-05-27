# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval
from odoo.tools import float_is_zero, plaintext2html


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    def _timesheet_create_task_prepare_values(self):
        self.ensure_one()
        project = self._timesheet_find_project()
        planned_hours = self._convert_qty_company_hours()
        description_so = plaintext2html(self.name) if self.name else False
        description_pr = self.product_id.description if self.product_id.description else ""
        description = description_so + description_pr
        return {
            'name': '%s:%s' % (self.order_id.name or '', self.name.split('\n')[0] or self.product_id.name),
            'planned_hours': planned_hours,
            'remaining_hours': planned_hours,
            'partner_id': self.order_id.partner_id.id,
            'description': description,
            'project_id': project.id,
            'sale_line_id': self.id,
            'company_id': self.company_id.id,
            'email_from': self.order_id.partner_id.email,
            'user_id': False, # force non assigned task, as created as sudo()
        }
