# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2018 ArtLine (<https://artline-erp.ru>).
#
##############################################################################

from odoo import api, models
from odoo.exceptions import ValidationError


class RuSaleOrderReport(models.AbstractModel):
    _name = "report.l10n_ru_schet.report_order_ws"

    def _get_report_values(self, docids, data=None):
        docs = self.env["sale.order"].browse(docids)
        if not self.env.company.bank_id:
            raise ValidationError(
                "Необходимо заполнить банковский счет в карточке компании."
            )
        return {
            "doc_ids": docs.ids,
            "doc_model": "sale.order",
            "docs": docs,
        }
