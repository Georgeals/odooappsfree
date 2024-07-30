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

# import base64
# from lxml import etree
# from io import BytesIO
import uuid
import xml.etree.ElementTree as ET
# import os
import re
from datetime import datetime

from odoo import models, fields, api, _
# from odoo.exceptions import UserError
# from odoo.release import version_info
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

from odoo.addons.l10n_ru_doc.report_helper import QWebHelper

SVOEDOTPR_ATTR = {u'ИННЮЛ': u"7605016030",
                  u'ИдЭДО': u"2BE",
                  u'НаимОрг': u"ООО \"Компания \"Тензор\""}
RUSSIA_CODE = "643"


class AccountInvoice(models.Model):
    _inherit = "account.move"

    edi_document_ids = fields.One2many(
        comodel_name='account.edi.document',
        inverse_name='invoice_id',
        string='Electronic Document for an Invoice'
    )
    edi_state = fields.Selection(
        selection=[('to_send', 'To Send'), ('sent', 'Sent'), ('to_cancel', 'To Cancel'), ('cancelled', 'Cancelled')],
        string="Electronic invoicing",
        store=True,
        compute='_compute_edi_state',
        help='The aggregated state of all the EDIs of this invoice')
    sbis_guid = fields.Char(string='GUID', readonly=True, copy=False)
    sbis_url = fields.Char(string='SBIS url', readonly=True, copy=False)
    sbis_state = fields.Char(string='SBIS state', readonly=True, copy=False)
    root = None

    # sbis_upload = fields.Boolean()
    # todo: cron sbis_state https://sbis.ru/help/integration/api/all_methods/read_doc/?

    @api.depends('edi_document_ids.state')
    def _compute_edi_state(self):
        for move in self:
            all_states = set(
                move.edi_document_ids.mapped('state'))
            if all_states == {'sent'}:
                move.edi_state = 'sent'
            elif all_states == {'cancelled'}:
                move.edi_state = 'cancelled'
            elif 'to_send' in all_states:
                move.edi_state = 'to_send'
            elif 'to_cancel' in all_states:
                move.edi_state = 'to_cancel'
            else:
                move.edi_state = False

    def upload_document_to_sbis(self):
        """Upload the document to the SBIS"""
        context = dict(self._context or {})
        context['active_ids'] = self.ids
        return {
            'name': _('Sbis Exchange'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.invoice.sbis',
            'views': [[False, 'form']],
            'context': context,
            'target': 'new',
        }

    def update_state_sbis(self):
        """Update the state of the SBIS document"""
        context = dict(self._context or {})
        context['active_ids'] = self.ids
        sbis = self.env['account.invoice.sbis'].with_context(context).create({'mode_type': 'update'})
        # sbis = self.env['account.invoice.sbis'].with_context({'active_ids': self.ids}).create({'mode_type': 'update'})
        sbis.upload_document_to_sbis()

    def create_edi_documents(self, edi_document_type, sbis_exchange):
        self.ensure_one()
        if edi_document_type == 'updschf':
            self.create_edi_document('l10n_ru_utd.invoice_report_utd')
        elif edi_document_type == 'updschf_xml':
            self.create_edi_document('l10n_ru_utd.invoice_report_utd', sbis_exchange)
        elif edi_document_type == 'aktnaklschf':
            types = self.mapped('invoice_line_ids.product_id.type')
            if u'service' in types:
                self.create_edi_document('l10n_ru_act.report_act')
            if u'consu' in types:
                self.create_edi_document('l10n_ru_doc.report_bill')
            self.create_edi_document('l10n_ru_schet_factura.report_invoice')

    def document_number(self):
        numb = "----"
        numeration = re.findall(r'\d+$', self.number)
        if numeration:
            numb = numeration[0]
        return numb

    def partner_type(self, partner):
        p_type = "unknown"
        if not partner.is_company:
            p_type = 'individual'
        elif len(partner.inn) == 12:
            p_type = 'individual_entrepreneur'
        elif len(partner.inn) == 10:
            p_type = 'organization'
        return p_type

    def set_xml_caption(self, company_info, partner_info):
        self.root.attrib[u'ВерсПрог'] = u'СБиС3'
        self.root.attrib[u'ВерсФорм'] = '5.01'
        ident_otprav = company_info.get(u'Идентификатор')
        ident_poluch = partner_info.get(u'Идентификатор')

        datepart = datetime.strptime(fields.Date.context_today(self), "%Y-%m-%d").strftime("%Y%m%d")
        self.sbis_guid = str(uuid.uuid4())
        idfile = "ON_NSCHFDOPPR_" + ident_poluch + "_" + ident_otprav + "_" + datepart + "_" + self.sbis_guid

        self.root.attrib[u'ИдФайл'] = idfile
        l1_element = ET.SubElement(self.root, u"СвУчДокОбор")
        l1_element.attrib[u'ИдОтпр'] = ident_otprav
        l1_element.attrib[u'ИдПол'] = ident_poluch
        l2_element = ET.SubElement(l1_element, u"СвОЭДОтпр")
        l2_element.attrib[u'ИдЭДО'] = SVOEDOTPR_ATTR[u'ИдЭДО']
        l2_element.attrib[u'ИННЮЛ'] = self.company_id.inn
        l2_element.attrib[u'НаимОрг'] = self.company_id.name

    def set_xml_doc_and_invoice_attribs(self):
        l1_element = ET.SubElement(self.root, u"Документ")
        l1_element.attrib[u'ВремИнфПр'] = datetime.now().strftime("%H.%M.%S")
        l1_element.attrib[u'ДатаИнфПр'] = datetime.now().strftime("%d.%m.%Y")
        # l1_element.attrib[u'ДатаИнфПр'] = datetime.strptime(
        #     self.create_date, "%Y-%m-%d %H:%M:%S").strftime("%d.%m.%Y")
        l1_element.attrib[u'КНД'] = "1115131"
        # l1_element.attrib[u'Функция'] = u"ДОП"
        l1_element.attrib[u'Функция'] = u"СЧФДОП"
        l1_element.attrib[u'ПоФактХЖ'] = (
            u"Документ об отгрузке товаров (выполнении работ), передаче имущественных прав (документ об оказании услуг)"
        )
        l1_element.attrib[u'НаимДокОпр'] = (
            u"Документ об отгрузке товаров (выполнении работ), передаче имущественных прав (документ об оказании услуг)"
        )
        l1_element.attrib[u'НаимЭконСубСост'] = self.company_id.name
        l2_element = ET.SubElement(l1_element, u"СвСчФакт")
        l2_element.attrib[u'ДатаСчФ'] = datetime.strptime(
            self.date_invoice, "%Y-%m-%d").strftime("%d.%m.%Y")
        l2_element.attrib[u'НомерСчФ'] = self.document_number()
        l2_element.attrib[u'КодОКВ'] = '643'

    def set_xml_svprod(self):
        l2_element = self.root.find(u'Документ').find(u'СвСчФакт')
        l3_element = ET.SubElement(l2_element, u"СвПрод")
        l4_element = ET.SubElement(l3_element, u"ИдСв")
        l5_element = ET.SubElement(l4_element, u"СвЮЛУч")
        l5_element.attrib[u'ИННЮЛ'] = self.company_id.inn
        l5_element.attrib[u'КПП'] = self.company_id.kpp
        l5_element.attrib[u'НаимОрг'] = self.company_id.name
        l4_element = ET.SubElement(l3_element, u"Адрес")
        # l5_element = ET.SubElement(l4_element, u"АдрРФ")
        helper = QWebHelper()
        l5_element = ET.SubElement(l4_element, u"АдрИнф")
        # l5_element.attrib[u'КодРегион'] = self.company_id.state_id.tax_regional_code
        # l5_element.attrib[u'КодСтр'] = str(self.company_id.state_id.country_id.id)
        l5_element.attrib[u'КодСтр'] = RUSSIA_CODE
        l5_element.attrib[u'АдрТекст'] = helper.address(self.company_id)
        l3_element = ET.SubElement(l2_element, u"ГрузОт")
        l4_element = ET.SubElement(l3_element, u"ОнЖе")
        l4_element.text = u'он же'

    def set_sub_xml(self, cp_type, partner, l3_element):
        l4_element = ET.SubElement(l3_element, u"ИдСв")
        if cp_type == 'organization':
            l5_element = ET.SubElement(l4_element, u"СвЮЛУч")
            l5_element.attrib[u'ИННЮЛ'] = partner.inn
            l5_element.attrib[u'КПП'] = partner.kpp
            l5_element.attrib[u'НаимОрг'] = partner.name
        else:
            if cp_type == 'individual_entrepreneur':
                l5_element = ET.SubElement(l4_element, u"СвИП")
                l5_element.attrib[u'ИННФЛ'] = partner.inn
                fio = ET.SubElement(l5_element, u"ФИО")
                name_parts = partner.name.split()
                if name_parts[0].lower() == u'ип':
                    name_parts = name_parts[1:]
                last_name, first_name, fathers_name = (name_parts + [' '] * 3)[:3]
                fio.attrib[u'Фамилия'] = last_name
                fio.attrib[u'Имя'] = first_name
                if fathers_name != ' ':
                    fio.attrib[u'Отчество'] = fathers_name
            elif cp_type == 'individual':
                l5_element = ET.SubElement(l4_element, u"СвФЛУчастФХЖ")
                fio = ET.SubElement(l5_element, u"ФИО")
                fio.attrib[u'Фамилия'] = partner.lastname
                fio.attrib[u'Имя'] = partner.firstname
        l4_element = ET.SubElement(l3_element, u"Адрес")
        helper = QWebHelper()
        l5_element = ET.SubElement(l4_element, u"АдрИнф")
        l5_element.attrib[u'КодСтр'] = RUSSIA_CODE
        if partner.egrul:
            l5_element.attrib[u'АдрТекст'] = partner.egrul
        else:
            l5_element.attrib[u'АдрТекст'] = helper.address(partner)

    def set_xml_gruzopoluch(self, partner):
        partner_shipping = partner
        if self.partner_shipping_id and self.partner_shipping_id.name:
            partner_shipping = self.partner_shipping_id
            if self.partner_shipping_id.parent_id and self.partner_shipping_id.parent_id.name:
                partner_shipping = self.partner_shipping_id.parent_id
        l2_element = self.root.find(u'Документ').find(u'СвСчФакт')
        l3_element = ET.SubElement(l2_element, u"ГрузПолуч")
        cp_type = self.partner_type(partner_shipping)
        self.set_sub_xml(cp_type, partner_shipping, l3_element)

    def set_xml_svpokup(self, cp_type, partner):
        l2_element = self.root.find(u'Документ').find(u'СвСчФакт')
        l3_element = ET.SubElement(l2_element, u"СвПокуп")
        self.set_sub_xml(cp_type, partner, l3_element)
        l3_element = ET.SubElement(l2_element, u"ДокПодтвОтгр")
        l3_element.attrib[u'НаимДокОтгр'] = u"УПД"
        l3_element.attrib[u'НомДокОтгр'] = self.document_number()
        l3_element.attrib[u'ДатаДокОтгр'] = l2_element.attrib[u'ДатаСчФ']

    def set_xml_tabl_sch_fact(self):
        l1_element = self.root.find(u'Документ')
        l2_element = ET.SubElement(l1_element, u"ТаблСчФакт")
        ind_num = 1
        for line in self.invoice_line_ids:
            svedtov = ET.Element(u"СведТов")
            svedtov.attrib[u'КолТов'] = str(line.quantity)
            svedtov.attrib[u'НаимТов'] = line.name
            svedtov.attrib[u'НалСт'] = "20%"
            svedtov.attrib[u'НомСтр'] = str(ind_num)
            svedtov.attrib[u'ОКЕИ_Тов'] = "796"
            # svedtov.attrib[u'ЦенаТов'] = str(line.price_unit)
            svedtov.attrib[u'ЦенаТов'] = '{:.2f}'.format(line.price_subtotal / line.quantity)
            svedtov.attrib[u'СтТовБезНДС'] = '{:.2f}'.format(line.price_subtotal)
            acciz = ET.SubElement(svedtov, u"Акциз")
            bacciz = ET.SubElement(acciz, u"БезАкциз")
            bacciz.text = u'без акциза'

            sumnal = ET.SubElement(svedtov, u"СумНал")
            rsumnal = ET.SubElement(sumnal, u"СумНал")
            rsumnal.text = '{:.2f}'.format(line.price_unit * line.quantity - line.price_subtotal)
            svedtov.attrib[u'СтТовУчНал'] = '{:.2f}'.format(line.price_unit*line.quantity)

            #  ДопСведТов
            dopsvedtov = ET.Element(u'ДопСведТов')
            dopsvedtov.attrib[u'НаимЕдИзм'] = line.uom_id.name or ''
            if line.product_id.default_code:
                dopsvedtov.attrib[u'КодТов'] = line.product_id.default_code
            svedtov.append(dopsvedtov)

            l2_element.append(svedtov)
            ind_num += 1

        vsegoopl = ET.SubElement(l2_element, u"ВсегоОпл")
        vsegoopl.attrib[u'СтТовБезНДСВсего'] = '{:.2f}'.format(self.amount_untaxed)
        vsegoopl.attrib[u'СтТовУчНалВсего'] = '{:.2f}'.format(self.amount_total)
        summnalvsego = ET.SubElement(vsegoopl, u"СумНалВсего")
        sumnal = ET.SubElement(summnalvsego, u"СумНал")
        sumnal.text = '{:.2f}'.format(self.amount_tax)

    def set_xml_sved_per(self):
        l1_element = self.root.find(u'Документ')
        l2_element = ET.SubElement(l1_element, u"СвПродПер")
        l3_element = ET.SubElement(l2_element, u"СвПер")
        types = self.mapped('invoice_line_ids.product_id.type')
        transferred = u"Услуги оказаны"
        if u'consu' in types:
            transferred = u"Товары переданы, услуги оказаны"
        if u'service' not in types:
            transferred = u"Товары переданы"
        l3_element.attrib[u'СодОпер'] = transferred
        l4_element = ET.SubElement(l3_element, u"ОснПер")
        l4_element.attrib[u'НаимОсн'] = u"Без документа-основания"

    def set_xml_podpisant(self):
        l1_element = self.root.find(u'Документ')
        # todo  делать ли разных подписантов? пока все взял по примеру отсюда https://www.diadoc.ru/docs/forms/upd
        l2_element = ET.SubElement(l1_element, u"Подписант")
        l3_element = ET.SubElement(l2_element, u"ЮЛ")
        fio = ET.SubElement(l3_element, u"ФИО")
        l2_element.attrib[u'ОснПолн'] = u"Должностные обязанности"
        l2_element.attrib[u'ОблПолн'] = "1"
        l2_element.attrib[u'Статус'] = "1"
        l3_element.attrib[u'ИННЮЛ'] = self.company_id.inn
        l3_element.attrib[u'Должн'] = self.company_id.chief_id.partner_id.function
        fio.attrib[u'Фамилия'] = self.company_id.chief_id.partner_id.lastname
        fio.attrib[u'Имя'] = self.company_id.chief_id.partner_id.firstname

    def get_xml_content(self, sbis_exchange):
        self.root = ET.Element(u"Файл")
        partner = self.partner_id.parent_id if self.partner_id.parent_id else self.partner_id
        cp_type = self.partner_type(partner)
        company_info = sbis_exchange.counterparty_information(self.company_id, 'organization')
        partner_info = sbis_exchange.counterparty_information(partner, cp_type)
        self.set_xml_caption(company_info, partner_info)
        self.set_xml_doc_and_invoice_attribs()
        self.set_xml_svprod()
        self.set_xml_gruzopoluch(partner)
        self.set_xml_svpokup(cp_type, partner)
        self.set_xml_tabl_sch_fact()
        self.set_xml_sved_per()
        self.set_xml_podpisant()
        # module_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        # xml_res_path = os.path.join(module_path, 'UPD_sbis_res.xml')
        # tree = ET.ElementTree(self.root)
        # tree.write(xml_res_path, encoding='WINDOWS-1251')
        xml_string = ET.tostring(self.root, encoding='WINDOWS-1251', method='xml')
        return xml_string

    def create_edi_document(self, report_xml_id, sbis_exchange=None):
        helper = QWebHelper()
        if sbis_exchange:
            content = self.get_xml_content(sbis_exchange).encode('base64')
            file_ext = u'.xml'
        else:
            content = self.env['report'].get_pdf([self.id], report_xml_id).encode('base64')
            file_ext = u'.pdf'
        edi_data = {
            'invoice_id': self.id,
            'state': 'to_send',
        }
        if self.sbis_guid:
            edi_data['guid'] = self.sbis_guid
            self.sbis_guid = False
        edi_utd_id = self.env['account.edi.document'].create(edi_data)
        if report_xml_id == 'l10n_ru_utd.invoice_report_utd':
            doc_type = u'УПД'
        elif report_xml_id == 'l10n_ru_act.report_act':
            doc_type = u'Акт'
        elif report_xml_id == 'l10n_ru_doc.report_bill':
            doc_type = u'Товарная накладная'
        elif report_xml_id == 'l10n_ru_schet_factura.report_invoice':
            doc_type = u'Счет-фактура'
        else:
            raise Exception('Unknown EDI document type. Name: %s not in act, bill, invoice...' % report_xml_id)
        invoice_date = datetime.strptime(self.date, DEFAULT_SERVER_DATE_FORMAT)
        # invoice_date = datetime.strptime(self.date or fields.Date.context_today(self), DEFAULT_SERVER_DATE_FORMAT)
        name = u'%s %s № %s на сумму %s р.' % (
            doc_type, invoice_date.strftime("%d.%m.%y"), helper.numer(self.number), self.amount_total)
        if self.amount_tax:
            name += u', в т.ч. НДС %s р.' % self.amount_tax
        fname = name.replace(u' ', u'_').replace(u'.', u'_').replace(u',', u'_') + file_ext
        if sbis_exchange:
            fname = self.root.attrib[u'ИдФайл'] + u'.xml'
        edi_utd_id.attachment_id = self.env['ir.attachment'].create({
            'name': name,
            'res_id': edi_utd_id.id,
            'res_model': str(edi_utd_id._name),
            'datas': content,
            'datas_fname': fname,
            'type': 'binary',
        }).id
        self.edi_document_ids = [(4, edi_utd_id.id, _)]

    def open_sbis_url(self):
        return {'type': 'ir.actions.act_url',
                'name': "SBIS url",
                'target': 'new',
                'url': self.sbis_url,
                }
