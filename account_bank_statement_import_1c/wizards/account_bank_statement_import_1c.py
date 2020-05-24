# -*- coding: utf-8 -*-

import StringIO
import dateutil.parser

from openerp.tools.translate import _
from openerp import api, models
from openerp.exceptions import UserError

import logging
_logger = logging.getLogger(__name__)


try:
    import chardet
except (ImportError, IOError) as err:
    chardet = False
    _logger.debug(err)

		
class AccountBankStatementImport(models.TransientModel):
    _inherit = "account.bank.statement.import"

    @api.model
    def _check_1c(self, data_file):
            return data_file.strip().startswith('1CClientBankExchange')

    def _parse_mod_date(self, date_str):
            return dateutil.parser.parse(date_str, fuzzy=True).date()
            
    def _parse_file(self, data_file):
        if not self._check_1c(data_file):
                return super(AccountBankStatementImport, self)._parse_file(data_file)
        
        
        if(chardet == False):
                encoding = 'utf-8'
        else:
                encoding = chardet.detect(data_file)['encoding']

        data_file = data_file.decode(encoding)

        data=data_file
        data=data.split('КонецРасчСчет'.decode('utf-8'))
        
        for k in range(len(data)-1):
        
            data[k]=data[k].split('\r\n')
            dicvp=dict()
            for l in range(len(data[k])):
                try: 
                    t=data[k][l].split('=')
                    dicvp[t[0]] = t[1]
                except:
                    pass
            data[k]=dicvp
        
        data[-1]=data[-1].split('КонецДокумента'.decode('utf-8'))
        for i in range(len(data[-1])):    
            data[-1][i]=data[-1][i].split('\r\n')
            dictran=dict()
            for j in range(len(data[-1][i])):    
                try: 
                    t=data[-1][i][j].split('=')
                    dictran[t[0]] = t[1]
                except:
                    pass
            data[-1][i]=dictran
        
        account_number=data[0]['РасчСчет'.decode('utf-8')]
        #bank statements data: list of dict containing (optional items marked by o) :
        date_start = dateutil.parser.parse(data[0]['ДатаНачала'.decode('utf-8')], dayfirst=True).date() 
        #'date': date (e.g: 2013-06-26)
        balance_start = float(data[0]['НачальныйОстаток'.decode('utf-8')])#-o 'balance_start': float (e.g: 8368.56)
        balance_stop = float(data[-2]['КонечныйОстаток'.decode('utf-8')])#-o 'balance_end_real': float (e.g: 8888.88)
        transactions = [] 
        #- 'transactions': list of dict containing :
        vals_line = {}
        vals_bank_statement = {}

        for l in data[-1]:
            if len(l)>0:
                vals_line['name'] = l['НазначениеПлатежа'.decode('utf-8')] 
                # 'name': string (e.g: 'KBC-INVESTERINGSKREDIET 787-5562831-01')
                vals_line['date'] = dateutil.parser.parse(l['Дата'.decode('utf-8')], dayfirst=True).date() #- 'date': date
                #- 'amount': float
                if l['ПлательщикРасчСчет'.decode('utf-8')] == account_number:
                    vals_line['amount'] = -float(l['Сумма'.decode('utf-8')])
                    vals_line['account_number']=l['ПолучательРасчСчет'.decode('utf-8')]     #-o 'account_number': string
                    vals_line['partner_name']=l['Получатель'.decode('utf-8')]  #-o 'partner_name': string
                    vals_line['unique_import_id']=l['ПолучательРасчСчет'.decode('utf-8')]+l['Дата'.decode('utf-8')].replace('.','')+l['Номер'.decode('utf-8')]   #- 'unique_import_id': string
                else:
                    vals_line['amount'] = float(l['Сумма'.decode('utf-8')])
                    vals_line['account_number']=l['ПлательщикРасчСчет'.decode('utf-8')]     #-o 'account_number': string
                    vals_line['partner_name']=l['Плательщик'.decode('utf-8')]  #-o 'partner_name': string
                    vals_line['unique_import_id']=l['ПлательщикРасчСчет'.decode('utf-8')]+l['Дата'.decode('utf-8')].replace('.','')+l['Номер'.decode('utf-8')]   #- 'unique_import_id': string
                #-o 'note': string
                vals_line['ref'] = 'п/п №'.decode('utf-8')+l['Номер'.decode('utf-8')] 
                #-o 'ref': string
                transactions.append(vals_line)
                vals_line = {}

        all_data = {
                'name': 'from '+data[0]['ДатаНачала'.decode('utf-8')]+' to '+data[-2]['ДатаКонца'.decode('utf-8')], # 'name': string (e.g: '000000123')
                'balance_start': balance_start,
                'date': date_start,#'date': date (e.g: 2013-06-26)
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
        partner_obj = self.env['res.partner']
        for statement in res:
            for line_vals in statement['transactions']:
                if not line_vals.get('partner_id') and line_vals.get('name'):
                    partner = partner_obj.search(
                        [('name', 'ilike', line_vals['partner_name'])], limit=1,
                    )
                    line_vals['partner_id'] = partner.id
        return res
