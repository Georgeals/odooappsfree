from odoo import api, models, _
import time
from odoo.addons.l10n_ru_doc.report_helper import QWebHelper


class RuReportPartnerLedger(models.AbstractModel):
    _inherit = "report.account.report_partnerledger"
    _name = "report.l10n_ru_act_sverki.report_partnerledger_ru"

    def _balance(self, data, partner, field, balance):
        if field not in ["debit - credit"]:
            return
        result = 0.0
        query_get_data = (
            self.env["account.move.line"]
            .with_context(data["form"].get("used_context", {}))
            ._query_get()
        )
        reconcile_clause = (
            ""
            if data["form"]["reconciled"]
            else ' AND "account_move_line".full_reconcile_id IS NULL '
        )

        params = [
            partner.id,
            tuple(data["computed"]["move_state"]),
            tuple(data["computed"]["account_ids"]),
        ] + query_get_data[2]
        query = (
            """SELECT sum("""
            + field
            + """)
                FROM """
            + query_get_data[0]
            + """, account_move AS m
                WHERE "account_move_line".partner_id = %s
                    AND m.id = "account_move_line".move_id
                    AND m.state IN %s
                    AND account_id IN %s
                    AND """
            + query_get_data[1]
            + reconcile_clause
        )
        if balance == "initial":
            params[3] = params[4]
        # for both balance (initial and final)
        params[4] = "1990-01-01"

        self.env.cr.execute(query, tuple(params))

        contemp = self.env.cr.fetchone()
        if contemp is not None:
            result = contemp[0] or 0.0
        return result

    def _negate(self, balans):
        if balans > 0:
            return
        balans = -balans
        return balans

    def _format(self, result):
        return "{:.2f}".format(result)

    @api.model
    def _get_report_values(self, docids, data=None):
        data["computed"] = {}

        obj_partner = self.env["res.partner"]
        query_get_data = (
            self.env["account.move.line"]
            .with_context(data["form"].get("used_context", {}))
            ._query_get()
        )
        data["computed"]["move_state"] = ["draft", "posted"]
        if data["form"].get("target_move", "all") == "posted":
            data["computed"]["move_state"] = ["posted"]
        result_selection = data["form"].get("result_selection", "customer")
        if result_selection == "supplier":
            data["computed"]["ACCOUNT_TYPE"] = ["liability_payable"]
        elif result_selection == "customer":
            data["computed"]["ACCOUNT_TYPE"] = ["asset_receivable"]
        else:
            data["computed"]["ACCOUNT_TYPE"] = ["liability_payable", "asset_receivable"]

        self.env.cr.execute(
            """
                    SELECT a.id
                    FROM account_account a
                    WHERE a.account_type IN %s
                    AND NOT a.deprecated""",
            (tuple(data["computed"]["ACCOUNT_TYPE"]),),
        )
        data["computed"]["account_ids"] = [a for (a,) in self.env.cr.fetchall()]
        params = [
            tuple(data["computed"]["move_state"]),
            tuple(data["computed"]["account_ids"]),
        ] + query_get_data[2]
        reconcile_clause = (
            ""
            if data["form"]["reconciled"]
            else ' AND "account_move_line".reconciled = false '
        )
        query = (
            """
                    SELECT DISTINCT "account_move_line".partner_id
                    FROM """
            + query_get_data[0]
            + """, account_account AS account, account_move AS am
                    WHERE "account_move_line".partner_id IS NOT NULL
                        AND "account_move_line".account_id = account.id
                        AND am.id = "account_move_line".move_id
                        AND am.state IN %s
                        AND "account_move_line".account_id IN %s
                        AND NOT account.deprecated
                        AND """
            + query_get_data[1]
            + reconcile_clause
        )
        self.env.cr.execute(query, tuple(params))
        # ---------------------Taking only selected partners---------------------------
        if data["form"]["partner_ids"]:
            partner_ids = data["form"]["partner_ids"]
        else:
            partner_ids = [res["partner_id"] for res in self.env.cr.dictfetchall()]
        # -----------------------------------------------------------------------------

        partners = obj_partner.browse(partner_ids)
        partners = sorted(partners, key=lambda x: (x.ref, x.name))

        data["form"]["date_from"] = ".".join(data["form"]["date_from"].split("-")[::-1])
        data["form"]["date_to"] = ".".join(data["form"]["date_to"].split("-")[::-1])
        docargs = {
            "doc_ids": partner_ids,
            "doc_model": self.env["res.partner"],
            "data": data,
            "docs": partners,
            "time": time,
            "lines": self._lines,
            "sum_partner": self._sum_partner,
            "negate": self._negate,
            "balance": self._balance,
            "format": self._format,
            "helper": QWebHelper(),
        }
        return docargs

    @api.model
    def render_html(self, docids, data=None):
        self.model = self.env.context.get("active_model")
        docs = self.env[self.model].browse(self.env.context.get("active_ids", [])).id

        data["computed"] = {}

        obj_partner = self.env["res.partner"]
        query_get_data = (
            self.env["account.move.line"]
            .with_context(data["form"].get("used_context", {}))
            ._query_get()
        )
        data["computed"]["move_state"] = ["draft", "posted"]
        if data["form"].get("target_move", "all") == "posted":
            data["computed"]["move_state"] = ["posted"]
        result_selection = data["form"].get("result_selection", "customer")
        if result_selection == "supplier":
            data["computed"]["ACCOUNT_TYPE"] = ["payable"]
        elif result_selection == "customer":
            data["computed"]["ACCOUNT_TYPE"] = ["receivable"]
        else:
            data["computed"]["ACCOUNT_TYPE"] = ["payable", "receivable"]

        self.env.cr.execute(
            """
            SELECT a.id
            FROM account_account a
            WHERE a.internal_type IN %s
            AND NOT a.deprecated""",
            (tuple(data["computed"]["ACCOUNT_TYPE"]),),
        )
        data["computed"]["account_ids"] = [a for (a,) in self.env.cr.fetchall()]
        params = [
            tuple(data["computed"]["move_state"]),
            tuple(data["computed"]["account_ids"]),
        ] + query_get_data[2]
        reconcile_clause = (
            ""
            if data["form"]["reconciled"]
            else ' AND "account_move_line".reconciled = false '
        )
        query = (
            """
            SELECT DISTINCT "account_move_line".partner_id
            FROM """
            + query_get_data[0]
            + """, account_account AS account, account_move AS am
            WHERE "account_move_line".partner_id IS NOT NULL
                AND "account_move_line".account_id = account.id
                AND am.id = "account_move_line".move_id
                AND am.state IN %s
                AND "account_move_line".account_id IN %s
                AND NOT account.deprecated
                AND """
            + query_get_data[1]
            + reconcile_clause
        )
        self.env.cr.execute(query, tuple(params))
        # ---------------------Taking only selected partners---------------------------
        if data["form"]["partner_ids"]:
            partner_ids = data["form"]["partner_ids"]
        else:
            partner_ids = [res["partner_id"] for res in self.env.cr.dictfetchall()]
        # -----------------------------------------------------------------------------

        partners = obj_partner.browse(partner_ids)
        partners = sorted(partners, key=lambda x: (x.ref, x.name))

        report_obj = self.env["report"]

        data["form"]["date_from"] = ".".join(data["form"]["date_from"].split("-")[::-1])
        data["form"]["date_to"] = ".".join(data["form"]["date_to"].split("-")[::-1])
        docargs = {
            "doc_ids": partner_ids,
            "doc_model": self.env["res.partner"],
            "data": data,
            "docs": partners,
            "time": time,
            "lines": self._lines,
            "sum_partner": self._sum_partner,
            "negate": self._negate,
            "balance": self._balance,
            "format": self._format,
            "helper": QWebHelper(),
        }
        return report_obj.render("l10n_ru_act.report_partnerledger_ru", docargs)