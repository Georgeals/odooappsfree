from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def action_account_partner_ledger_filter_ru(self):

        view = self.env.ref('l10n_ru_act_sverki.account_report_partner_ledger_view')
        return {
            'type': 'ir.actions.act_window',
            'name': 'Partner Ledger Ru',
            'res_model': 'account.report.partner.ledger',
            'view_mode': 'form',
            'views': [(view.id, 'form'), (False, 'tree')],
            'target': 'new',
            "context": {'default_partner_ids': self.ids}
        }