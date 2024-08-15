# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountCommonReport(models.TransientModel):
    _name = "account.common.report"
    _description = "Account Common Report"

    company_id = fields.Many2one(
        "res.company",
        string="Company",
        readonly=True,
        default=lambda self: self.env.user.company_id,
    )
    journal_ids = fields.Many2many(
        "account.journal",
        string="Journals",
        required=True,
        default=lambda self: self.env["account.journal"].search([]),
    )
    date_from = fields.Date(string="Start Date")
    date_to = fields.Date(string="End Date")
    target_move = fields.Selection(
        [
            ("posted", "All Posted Entries"),
            ("all", "All Entries"),
        ],
        string="Target Moves",
        required=True,
        default="posted",
    )

    def _build_contexts(self, data):
        result = {}
        result["journal_ids"] = (
            "journal_ids" in data["form"] and data["form"]["journal_ids"] or False
        )
        result["state"] = (
            "target_move" in data["form"] and data["form"]["target_move"] or ""
        )
        result["date_from"] = data["form"]["date_from"] or False
        result["date_to"] = data["form"]["date_to"] or False
        result["strict_range"] = True if result["date_from"] else False
        return result

    def _print_report(self, data):
        raise (_("Error!"), _("Not implemented."))

    def check_report(self):
        self.ensure_one()
        data = {}
        data["ids"] = self.env.context.get("active_ids", [])
        data["model"] = self.env.context.get("active_model", "ir.ui.menu")
        data["form"] = self.read(
            ["date_from", "date_to", "journal_ids", "target_move"]
        )[0]
        used_context = self._build_contexts(data)
        data["form"]["used_context"] = dict(
            used_context, lang=self.env.context.get("lang") or "en_US"
        )
        return self._print_report(data)


class AccountingCommonPartnerReport(models.TransientModel):
    _name = "account.common.partner.report"
    _description = "Account Common Partner Report"
    _inherit = "account.common.report"

    result_selection = fields.Selection(
        [
            ("customer", "Receivable Accounts"),
            ("supplier", "Payable Accounts"),
            ("customer_supplier", "Receivable and Payable Accounts"),
        ],
        string="Partner's",
        required=True,
        default="customer",
    )

    def pre_print_report(self, data):
        data["form"].update(self.read(["result_selection"])[0])
        return data


class AccountPartnerLedger(models.TransientModel):
    _inherit = "account.common.partner.report"
    _name = "account.report.partner.ledger"
    _description = "Account Partner Ledger"

    amount_currency = fields.Boolean(
        "With Currency",
        help="It adds the currency column on report if the currency differs from the company currency.",
    )
    reconciled = fields.Boolean("Reconciled Entries")
    partner_ids = fields.Many2many(
        "res.partner",
        "partner_ledger_partner_rel",
        "id",
        "partner_id",
        string="Partners",
    )
    date_from = fields.Date(string="Start Date", required=True)
    date_to = fields.Date(string="End Date", required=True)
    target_move = fields.Selection(
        [
            ("posted", "All Posted Entries"),
            ("all", "All Entries"),
        ],
        string="Target Moves",
        required=True,
        default="all",
    )
    result_selection = fields.Selection(
        [
            ("customer", "Receivable Accounts"),
            ("supplier", "Payable Accounts"),
            ("customer_supplier", "Receivable and Payable Accounts"),
        ],
        string="Partner's",
        required=True,
        default="customer_supplier",
    )
    reconciled = fields.Boolean("Reconciled Entries", default=True)

    def _print_report(self, data):
        data = self.pre_print_report(data)
        data["form"].update(
            {
                "reconciled": self.reconciled,
                "amount_currency": self.amount_currency,
                "partner_ids": self.partner_ids.ids,
            }
        )
        action = self.env.ref(
            "l10n_ru_act_sverki.account_action_report_partnerledger_ru"
        ).report_action(self, data=data)
        action.update(data)
        return action

    def _print_report_without_stamp(self, data):
        data = self.pre_print_report(data)
        data["form"].update(
            {
                "reconciled": self.reconciled,
                "amount_currency": self.amount_currency,
                "partner_ids": self.partner_ids.ids,
            }
        )
        action = self.env.ref(
            "l10n_ru_act_sverki.account_action_report_partnerledger_ru_without_stamp"
        ).report_action(self, data=data)
        action.update(data)
        return action

    def check_report_without_stamp(self):
        self.ensure_one()
        data = {}
        data["ids"] = self.env.context.get("active_ids", [])
        data["model"] = self.env.context.get("active_model", "ir.ui.menu")
        data["form"] = self.read(
            ["date_from", "date_to", "journal_ids", "target_move"]
        )[0]
        used_context = self._build_contexts(data)
        data["form"]["used_context"] = dict(
            used_context, lang=self.env.context.get("lang") or "en_US"
        )
        return self._print_report_without_stamp(data)

    @api.model
    def default_get(self, default_fields):
        defaults = super(AccountPartnerLedger, self).default_get(default_fields)
        journals = self.env["account.journal"].search(
            [("type", "in", ["sale", "purchase", "bank"])]
        )
        value = [journal.id for journal in journals]
        field = self._fields["journal_ids"]
        value = field.convert_to_cache(value, self, validate=False)
        defaults["journal_ids"] = field.convert_to_write(value, self)
        return defaults
