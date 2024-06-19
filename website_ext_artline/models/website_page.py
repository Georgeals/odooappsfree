from odoo import models, fields, api, _


class Page(models.Model):
    _inherit = 'website.page'

    changes_ids = fields.One2many(
        comodel_name='website.changes.saver',
        inverse_name='page_id',
    )
    changes_count = fields.Integer(
        string='Changes Count',
        compute='_compute_changes_count',
    )

    def action_changes_view(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "website.changes.saver",
            "views": [[False, "tree"]],
            'domain': [['id', 'in', self.changes_ids.ids]],
        }

    @api.depends('changes_ids')
    def _compute_changes_count(self):
        for page in self:
            page.changes_count = len(page.changes_ids)
