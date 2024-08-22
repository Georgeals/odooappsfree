from odoo import models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    def get_move_lines_for_reconciliation(self, partner_id=None, excluded_ids=None, str=False, offset=0, limit=None, additional_domain=None, overlook_partner=False):
        # If not partner_id, do not return any invoices for reconcile
        if partner_id is False:
            return self.env['account.move.line']
        return super(AccountBankStatementLine, self).get_move_lines_for_reconciliation(partner_id, excluded_ids, str, offset, limit, additional_domain, overlook_partner)
