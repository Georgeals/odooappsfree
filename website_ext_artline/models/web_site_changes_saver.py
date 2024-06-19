from odoo import models, fields


class WebsiteChangesSaver(models.Model):
    _name = 'website.changes.saver'

    page_id = fields.Many2one(
        'website.page', require=True, null=False,
    )
    view_id = fields.Many2one(
        'ir.ui.view', require=True, null=False,
    )
    saved_data = fields.Text(require=True, null=False)
    page_update_date = fields.Datetime()
    page_update_uid = fields.Many2one(
        'res.users', require=True, mull=False,
    )
