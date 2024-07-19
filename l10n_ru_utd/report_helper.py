# -*- encoding: utf-8 -*-
# Copyright ArtLineStudio Ltd., 2021 (<https://artlinespb.ru/>)
# Author: George Yanguzov <george@artlinespb.ru>
# License AGPL-3.0 or later (<http://www.gnu.org/licenses/agpl>).

from datetime import datetime
import re
from pytils import numeral,dt
from odoo.addons.l10n_ru_doc.report_helper import QWebHelper


class QWebHelper(QWebHelper):

    def ru_date3(self, date):
        if date:
            date = datetime.strftime(date, '%Y-%m-%d')
            # date = '.'.join(date.split('-')[::-1])
        return date

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
