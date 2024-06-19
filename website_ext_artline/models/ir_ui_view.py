from odoo import models, fields, api


class ViewExtended(models.Model):
    _inherit = 'ir.ui.view'

    changes_ids = fields.One2many(
        comodel_name='website.changes.saver',
        inverse_name='view_id',
    )

    def save(self, value, xpath=None):
        self.ensure_one()
        current_website = self.env['website'].get_current_website()
        website_specific_view = self.env['ir.ui.view'].search([
            ('key', '=', self.key),
            ('website_id', '=', current_website.id)
        ], limit=1)

        if website_specific_view:
            self = website_specific_view

        data = {
            'view_id': self.id,
        }

        super(ViewExtended, self).save(value, xpath=xpath)

        data.update({
            'saved_data': self.arch_base,
            'page_update_date': self.write_date,
            'page_update_uid': self.write_uid.id,
            'page_id': self.first_page_id.id,
        })

        self.env['website.changes.saver'].sudo().create(data)
