# Copyright 2019 - ArtLine, LTD
# License OPL-1

import dateutil.parser

from odoo.tools.translate import _
from odoo import api, models
from odoo.exceptions import UserError


class AccountBankStatementImport(models.TransientModel):
    _inherit = "account.bank.statement.import"

    @api.model
    def _check_file(self, data_file):
        return data_file.strip().startswith(b'$OPERS')

    def _parse_file(self, data_file):
        if not self._check_file(data_file):
            return super(AccountBankStatementImport, self)._parse_file(
                data_file)
        try:
            file_data = data_file.decode('cp1251')
            if '\r\n' in file_data:
                data_list = file_data.split('\r\n')
            elif '\r' in file_data:
                data_list = file_data.split('\r')
            else:
                data_list = file_data.split('\n')
            header = data_list[0].strip()
            header = header.split("_")[1]
        except:
            raise UserError(_('Could not decipher the ibank2 file.'))
        transactions = []
        vals_line = {}
        doc_name = ''
        date_start = ''
        kor = ''
        balance_start = 0.0
        balance_stop = 0.0
        date_end = ''
        vals_bank_statement = {}
        for line in data_list:
                line = line.strip()
                line = line.split("=")
                if not line:
                        continue
                if line[0] == 'OPER_DATE':
                        vals_line['date'] = dateutil.parser.parse(line[1], dayfirst=True).date()
                elif line[0] == 'AMOUNT':
                        vals_line['amount'] = float(line[1].replace(',', ''))
                elif line[0] == 'BEGIN_DATE':
                        date_start = dateutil.parser.parse(line[1], dayfirst=True).date()
                elif line[0] == 'END_DATE':
                        date_end = dateutil.parser.parse(line[1], dayfirst=True).date()
                elif line[0] == 'DOC_NUM':
                        vals_line['ref'] = "п.п. № " + line[1]
                elif line[0] == 'IN_REST':
                        balance_start = float(line[1])
                elif line[0] == 'OUT_REST':	
                        balance_stop = float(line[1])
                elif line[0] == 'OPER_DETAILS':
                        vals_line['name'] = line[1]
                elif line[0] == 'CORR_NAME':
                        vals_line['partner_name'] = line[1]
                elif line[0] == 'CORR_ACCOUNT':
                        vals_line['account_number'] = line[1]
                elif line[0] == 'OPER_ID':
                        vals_line['unique_import_id'] = line[1]
                elif line[0] == '$OPERATION_END':
                        transactions.append(vals_line)
                        vals_line = {}
                else:
                        pass
        name='to '+str(date_end)
        all_data = {
                'name': name,
                'balance_start': balance_start,
                'date': date_start,
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
        test = 1
        partner_obj = self.env['res.partner']
        for statement in res:
            for line_vals in statement['transactions']:
                if not line_vals.get('partner_id') and line_vals.get('name'):
                    partner = partner_obj.search(
                        [('name', 'ilike', line_vals['partner_name'])], limit=1,
                    )
                    line_vals['partner_id'] = partner.id
        return res
