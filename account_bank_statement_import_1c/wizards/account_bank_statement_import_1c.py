# -*- encoding: utf-8 -*-
# Copyright ArtLineStudio Ltd, 2019 (<http://artlinespb.ru>)
# Author: George Yanguzov <george@artlinespb.ru>
# License AGPL-3.0 or later (<http://www.gnu.org/licenses/agpl>).

import logging
from datetime import datetime

from odoo import api, models
from odoo.exceptions import UserError
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class AccountBankStatementImport(models.TransientModel):
    _inherit = "account.bank.statement.import"

    @api.model
    def _check_file(self, data_file):
        return data_file.strip().startswith(b'1CClientBankExchange')

    def _parse_file(self, data_file):
        if not self._check_file(data_file):
            return super(AccountBankStatementImport, self)._parse_file(data_file)
        try:
            file_data = data_file.decode('cp1251')
        except:
            raise UserError(_('Could not decode file.'))
        section_index = file_data.find('Секция')
        common_info_1c = file_data[:section_index]
        common_info_1c = common_info_1c.strip()
        common_info_1c_lines = common_info_1c.split('\r\n')
        common_info_1c = {}
        for line in common_info_1c_lines:
            if line.find('=') > 0:
                line_key_value = line.split('=')
                common_info_1c[line_key_value[0]] = line_key_value[1]
        sections_1c_string = file_data[section_index:]
        sections_1c_lines = sections_1c_string.split('\r\n')
        bank_statements = []
        transactions_1c = []
        # Temporary variables
        section_name = None
        section_dict = {}
        for line_1c in sections_1c_lines:
            if line_1c.startswith('Секция'):
                section_name = line_1c[6:]
                section_dict = {}
                continue
            if section_name and line_1c.find('=') > 0:
                line_1c_key_value = line_1c.split('=')
                section_dict[line_1c_key_value[0]] = line_1c_key_value[1]
            if line_1c.startswith('Конец'):
                if section_name == 'РасчСчет':
                    bank_statements.append(section_dict)  # section_dict.copy()
                elif section_name.startswith('Документ'):
                    transactions_1c.append(section_dict)  # section_dict.copy()
                else:
                    raise UserError(_('Unknown section type: %s.', section_name))
                section_name = None
            if line_1c.startswith('КонецФайла'):
                break

        account_number = common_info_1c['РасчСчет']
        # bank statements data: list of dict containing (optional items marked by o) :
        # 'date': date (e.g: 2013-06-26)
        date_start = datetime.strptime(bank_statements[0]['ДатаНачала'], '%d.%m.%Y').date()
        balance_start = float(bank_statements[0]['НачальныйОстаток'])  # -o 'balance_start': float (e.g: 8368.56)
        balance_stop = float(bank_statements[-1]['КонечныйОстаток'])  # -o 'balance_end_real': float (e.g: 8888.88)
        # 'transactions': list of dict containing :
        transactions = []
        for transaction_1c in transactions_1c:
            if len(transaction_1c) > 0:
                # 'name': string (e.g: 'KBC-INVESTERINGSKREDIET 787-5562831-01')
                # 'date': date
                vals_line = {
                    # 'name': string (e.g: 'KBC-INVESTERINGSKREDIET 787-5562831-01')
                    'name': transaction_1c['НазначениеПлатежа'],
                    # 'date': date
                    'date': datetime.strptime(transaction_1c['Дата'], '%d.%m.%Y').date()
                }
                # 'amount': float
                if transaction_1c['ПлательщикРасчСчет'] == account_number:
                    vals_line['amount'] = -float(transaction_1c['Сумма'])
                    vals_line['account_number'] = transaction_1c['ПолучательРасчСчет']  # -o 'account_number': string
                    vals_line['partner_name'] = transaction_1c['Получатель']  # -o 'partner_name': string
                    # 'unique_import_id': string
                    vals_line['unique_import_id'] = '{}{}{}'.format(transaction_1c['ПолучательРасчСчет'],
                                                                    transaction_1c['Дата'].replace('.', ''),
                                                                    transaction_1c['Номер'])
                else:
                    vals_line['amount'] = float(transaction_1c['Сумма'])
                    vals_line['account_number'] = transaction_1c['ПлательщикРасчСчет']  # -o 'account_number': string
                    vals_line['partner_name'] = transaction_1c['Плательщик']  # -o 'partner_name': string
                    # #- 'unique_import_id': string
                    vals_line['unique_import_id'] = '{}{}{}'.format(transaction_1c['ПлательщикРасчСчет'],
                                                                    transaction_1c['Дата'].replace('.', ''),
                                                                    transaction_1c['Номер'])
                #-o 'note': string
                vals_line['ref'] = 'п/п № {}'.format(transaction_1c['Номер'])  #-o 'ref': string
                transactions.append(vals_line)

        vals_bank_statement = {
            # 'name': string (e.g: '000000123')
            'name': 'from ' + common_info_1c['ДатаНачала'] + ' to ' + common_info_1c['ДатаКонца'],
            'balance_start': balance_start,
            'date': date_start,  # 'date': date (e.g: 2013-06-26)
            'balance_end_real': balance_stop,
            'transactions': transactions
        }
        return None, None, [vals_bank_statement]

    def _complete_stmts_vals(self, stmt_vals, journal_id, account_number):
        """Match partner_id if hasn't been deducted yet."""
        res = super(AccountBankStatementImport, self)._complete_stmts_vals(
            stmt_vals, journal_id, account_number,
        )
        # If doesn't find account numbers of partner(normal behaviour is to
        # provide 'account_number', which the generic module uses to find
        # the partner), we have to find res.partner through the name
        partner_obj = self.env['res.partner']
        for statement in res:
            for line_vals in statement['transactions']:
                if not line_vals.get('partner_id') and line_vals.get('name'):
                    partner = partner_obj.search(
                        [('name', 'ilike', line_vals['partner_name'])], limit=1,
                    )
                    line_vals['partner_id'] = partner.id
        return res
