# -*- coding: utf-8 -*-
##############################################################################
#
#    ArtLineStudio Ltd.
#    Copyright (C) 2021-TODAY ArtLineStudio(<https://artlinespb.ru/>).
#    Author: George Yanguzov(<george@artlinespb.ru>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
# from odoo import api, fields, models, _
from odoo import fields, models, _
# import odoo.addons.decimal_precision as dp
# from odoo.tools import float_compare, float_round, float_is_zero, config
from odoo.exceptions import UserError
from .sbis_request import SbisExchange
# from lxml import etree

# from datetime import datetime
# import mimetypes

logger = logging.getLogger(__name__)


# class FakeSbisExchange(object):
#
#     def __init__(self):
#         pass
#
#     def counterparty_information(self, partner_id, cp_type='organization'):
#         fake_result = {
#             u'Идентификатор': 'FKE1d49fa3c4e8011e2b170005056b7304c',
#         }
#         return fake_result


class InvoicesToSbis(models.TransientModel):
    _name = 'account.invoice.sbis'
    _description = 'Wizard to upload customer invoices to SBIS'

    edi_document_type = fields.Selection([
        ('updschf', 'Universal Transfer Document'),
        # УпдСчфДоп	Счет-фактура и передаточный документ от 01.04.2016 или 02.02.2019
        ('updschf_xml', _('Universal Transfer Document, xml')),
        # УпдСчфДоп	Счет-фактура и передаточный документ от 01.04.2016 или 02.02.2019
        ('aktnaklschf', ' Act/Consignment Note and Invoice'),
        # АктВР	Акт выполненных работ
    ], string='Type document for send', default="updschf")
    # note = fields.Text('Note')
    mode_type = fields.Selection([
        ('send', 'Send document'),
        ('update', 'Update state'),
        ('auto', 'Auto'),
    ], string='Mode', default="auto", help="""
    Send document - Send document to the SBIS.
    Update state - Update document state from the SBIS.
    Auto - auto compute mode, send for new document and Update state for sended document.
    Note: Invoices with draft status are skipped!
    """, readonly=True)

    def upload_document_to_sbis(self):
        """Exchange the document to the SBIS"""
        try:
            sbis_exchange = SbisExchange(self.env.user.company_id.sbis_login,
                                         self.env.user.company_id.sbis_password)
            # sbis_exchange = FakeSbisExchange()
            #         todo: define (ConnectionError, Timeout)
            invoices = self.env['account.invoice'].browse(self.env.context.get('active_ids'))
            for invoice in invoices:
                # pdf
                if invoice.state != 'draft':
                    if self.mode_type in ['send', 'auto'] and invoice.sbis_guid is False:
                        invoice.create_edi_documents(self.edi_document_type, sbis_exchange)
                        result = sbis_exchange.write_document(invoice)
                        invoice.sbis_guid = result[u'Идентификатор']
                        invoice.sbis_url = result[u'СсылкаДляНашаОрганизация']
                        invoice.sbis_state = result[u'Состояние'][u'Описание']
                    elif self.mode_type in ['update', 'auto'] and invoice.sbis_guid is not False:
                        pass
                        result = sbis_exchange.read_document(invoice)
                        invoice.sbis_url = result[u'СсылкаДляНашаОрганизация']
                        invoice.sbis_state = result[u'Состояние'][u'Описание']
                    # todo add for attachment этап result[u'Этап'][-1][u'Название']
            sbis_exchange.authexit()
        except Exception as e:
            raise UserError(e.message)
        return {'type': 'ir.actions.act_window_close'}

# todo: Q Add note примечани?
# todo: add check    Для передаваемых данных также есть ограничения по размеру. HTTP-запрос вместе с заголовками должен
#  быть не больше 100 МБ. Записываемое вложение не должно превышать 73 МБ. При кодировании двоичных данных в Base64
#  размер вложения увеличивается на 25%.
