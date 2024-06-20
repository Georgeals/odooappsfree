from odoo import models, fields, _


class WebsiteChangesSaver(models.Model):
    _name = 'website.changes.saver'
    _rec_name = 'page_id'

    page_id = fields.Many2one(
        'website.page', require=True, null=False, readonly=True,
    )
    view_id = fields.Many2one(
        'ir.ui.view', require=True, null=False, readonly=True,
    )
    saved_data = fields.Text(require=True, null=False, readonly=True,)
    page_update_date = fields.Datetime(readonly=True,)
    page_update_uid = fields.Many2one(
        'res.users', require=True, mull=False, readonly=True,
    )
