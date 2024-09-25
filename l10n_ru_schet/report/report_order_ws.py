# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2018 ArtLine (<https://artline-erp.ru>).
#
##############################################################################

from odoo import api, models


class RuSaleOrderReport(models.AbstractModel):
    _name = "report.l10n_ru_schet.report_order_ws"

    def _get_report_values(self, docids, data=None):
        sale_orders = self.env["sale.order"].browse(docids)
        for order in sale_orders:
            order.company_id.check_bank_id_is_not_empty()
        return {
            "doc_ids": sale_orders.ids,
            "doc_model": "sale.order",
            "docs": sale_orders,
        }
