# -*- encoding: utf-8 -*-
# Copyright ArtLineStudio Ltd, 2019 (<http://artlinespb.ru>)
# Author: George Yanguzov <george@artlinespb.ru>
# License AGPL-3.0 or later (<http://www.gnu.org/licenses/agpl>).

import dateutil.parser
import hashlib
from odoo.tools.translate import _
from odoo import api, models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class AccountBankStatementImport(models.TransientModel):
    _inherit = "account.bank.statement.import"

    @api.model
    def _check_file(self, data_file):
        return data_file.strip().startswith(b'1CClientBankExchange')

    def _parse_file(self, data_file):
        if not self._check_file(data_file):
            return super(AccountBankStatementImport, self)._parse_file(
                data_file)
        try:
            file_data = data_file.decode('cp1251')
        except:
            raise UserError(_('Could not decode file .'))
        data = file_data
        data = data.split('КонецРасчСчет')
        data[0] = data[0].split('\r\n')
        dicvp = dict()
        for l in range(len(data[0])):
            try:
                t = data[0][l].split('=')
                dicvp[t[0]] = t[1]
            except:
                pass
        data[0] = dicvp
        data[1] = data[1].split('КонецДокумента')
        for i in range(len(data[1])):
            data[1][i] = data[1][i].split('\r\n')
            dictran = dict()
            for j in range(len(data[1][i])):
                try:
                    t = data[1][i][j].split('=')
                    dictran[t[0]] = t[1]
                except:
                    pass
            data[1][i] = dictran

        account_number = data[0]['РасчСчет']
        # bank statements data: list of dict containing (optional items marked by o) :

        date_start = dateutil.parser.parse(data[0]['ДатаНачала'],
                                           dayfirst=True).date()  # 'date': date (e.g: 2013-06-26)
        balance_start = float(data[0]['НачальныйОстаток'])  # -o 'balance_start': float (e.g: 8368.56)
        balance_stop = float(data[0]['КонечныйОстаток'])  # -o 'balance_end_real': float (e.g: 8888.88)
        transactions = []  # - 'transactions': list of dict containing :
        vals_line = {}
        vals_bank_statement = {}

        for l in data[1]:
            if len(l) > 0:
                vals_line['name'] = l[
                    'НазначениеПлатежа']  # 'name': string (e.g: 'KBC-INVESTERINGSKREDIET 787-5562831-01')
                vals_line['date'] = dateutil.parser.parse(l['Дата'], dayfirst=True).date()  # - 'date': date
                # - 'amount': float
                if l['ПлательщикРасчСчет'] == account_number:
                    vals_line['amount'] = -float(l['Сумма'])
                    vals_line['account_number'] = l['ПолучательРасчСчет']  # -o 'account_number': string
                    vals_line['partner_name'] = l['Получатель']  # -o 'partner_name': string
                else:
                    vals_line['amount'] = float(l['Сумма'])
                    vals_line['account_number'] = l['ПлательщикРасчСчет']  # -o 'account_number': string
                    vals_line['partner_name'] = l['Плательщик']  # -o 'partner_name': string
                unique_import_id = ''.join(str(e) for e in vals_line.values())
                hash_object = hashlib.md5(unique_import_id.encode('utf-8'))
                vals_line['unique_import_id'] = l['Дата'].replace('.', '') + hash_object.hexdigest()
                _logger.debug('Namber - %s, Hash - %s', l['Номер'], hash_object.hexdigest())
                # -o 'note': string
                vals_line['ref'] = 'п/п №' + l['Номер']  # -o 'ref': string
                transactions.append(vals_line)
                vals_line = {}
        all_data = {
            'name': 'from ' + data[0]['ДатаНачала'] + ' to ' + data[0]['ДатаКонца'],
            # 'name': string (e.g: '000000123')
            'balance_start': balance_start,
            'date': date_start,  # 'date': date (e.g: 2013-06-26)
            'balance_end_real': balance_stop,
            'transactions': transactions
        }
        vals_bank_statement.update(all_data)
        return None, None, [vals_bank_statement]

    def _complete_stmts_vals(self, stmt_vals, journal_id, account_number):
        """Match partner_id if hasn't been deducted yet."""

        res = super(AccountBankStatementImport, self)._complete_stmts_vals(
            stmt_vals, journal_id, account_number,
        )
        # If doesn't find account numbers of partner(normal behaviour is to
        # provide 'account_number', which the generic module uses to find
        # the partner), we have to find res.partner through the name
        test = 5
        partner_obj = self.env['res.partner']
        for statement in res:
            for line_vals in statement['transactions']:
                if not line_vals.get('partner_id') and line_vals.get('name'):
                    partner = partner_obj.search(
                        [('name', 'ilike', line_vals['partner_name'])], limit=1,
                    )
                    line_vals['partner_id'] = partner.id
        return res
