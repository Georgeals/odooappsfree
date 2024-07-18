# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2015-2018 ArtLine (<https://artline-erp.ru/>).
#
##############################################################################

from odoo import api, models


class RuSaleOrderReport(models.AbstractModel):
    _name = "report.l10n_ru_schet.report_order"

    def _get_report_values(self, docids, data=None):
        docs = self.env["sale.order"].browse(docids)
        return {
            "doc_ids": docs.ids,
            "doc_model": "sale.order",
            "docs": docs,
        }
