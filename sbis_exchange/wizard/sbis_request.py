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
from datetime import datetime
import requests
# import json

from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.addons.l10n_ru_doc.report_helper import QWebHelper

_logger = logging.getLogger(__name__)

TIMEOUT = 30


class SbisExchange(object):

    # todo: Q: аутентификацию по сертификату. Q: писать ли функцию, которая генерирует код подтверждения и отправляет
    #  его на телефон, который указан в карточке сотрудника.

    # todo: Не сохраняйте в вашей ИС идентификаторы участников документооборота или какие-либо ссылки, кроме
    #  «Документ.СсылкаДляКонтрагент». Оператор связи может изменять ссылки и идентификаторы, не уведомляя
    #  пользователей.
    # todo method: Укажите в формализованных xml-вложениях идентификаторы участников электронного обмена документами
    #  и реквизиты подписанта. Идентификаторы участников ЭДО можно получить вызовом функции
    #  «СБИС.ИнформацияОКонтрагенте».
    # todo: state Состояние и этапы документооборота
    # Чтобы система могла отслеживать состояние документа, в объекте «Документ» предусмотрены:    #
    # «Документ.Этап» — список текущих этапов документооборота;
    # «Документ.Событие» — список событий по документу.

    def __init__(self, login, password, user_agent='Odoo/10.0.0'):
        """https://sbis.ru/help/integration/api/all_methods/auth_one"""
        self.headers = {
            'Content-Type': 'application/json-rpc;charset=utf-8',
            'Accept': '*/*',
            'User-Agent': user_agent,
        }
        url = 'https://online.sbis.ru/auth/service/'
        self.url_service = 'https://online.sbis.ru/service/?srv=1'
        rpc_input = {
            u"jsonrpc": u"2.0",
            u"method": u"СБИС.Аутентифицировать",
            u"params": {
                u"Параметр": {
                    u"Логин": login,
                    u"Пароль": password
                }
            },
            u"id": 0
        }
        response_json = requests.post(url=url, headers=self.headers, json=rpc_input, timeout=TIMEOUT).json()
        self.check_response_json(response_json)
        # self.headers['X-SBISSessionID'] = response_json.get('result')
        self.headers.update({
            'X-SBISSessionID': response_json.get('result')
        })
        # todo: check Timeout
        # Content-Type: application/json-rpc;charset=utf-8
        # X-SBISSessionID: 0000ea78-0000ea79-00ba-d3b85272bc0c4842

    def counterparty_information(self, partner_id, cp_type='organization'):
        """https://sbis.ru/help/integration/api/all_methods/companyinfo"""
        url = 'https://online.sbis.ru/service/?srv=1'
        if cp_type == 'organization':
            rpc_input = {
                "jsonrpc": "2.0",
                "method": u"СБИС.ИнформацияОКонтрагенте",
                "params": {
                    u"Участник": {
                        u"СвЮЛ": {
                            u"ИНН": partner_id.inn,
                            u"КПП": partner_id.kpp,
                            u"Название": partner_id.name
                        }
                        # },
                        # u"ДопПоля": ""
                    }
                },
                "id": 0
            }

        elif cp_type == 'individual_entrepreneur':
            name_parts = partner_id.name.split()
            if name_parts[0].lower() == u'ип':
                name_parts = name_parts[1:]
            last_name, first_name, fathers_name = (name_parts + [' '] * 3)[:3]
            rpc_input = {
                "jsonrpc": "2.0",
                "method": u"СБИС.ИнформацияОКонтрагенте",
                "params": {
                    u"Участник": {
                        u"СвФЛ": {
                            u"ИНН": partner_id.inn,
                            u"Фамилия": last_name,
                            u"Имя": first_name,
                        }
                    }
                },
                "id": 0
            }
        elif cp_type == 'individual':
            rpc_input = {
                "jsonrpc": "2.0",
                "method": u"СБИС.ИнформацияОКонтрагенте",
                "params": {
                    u"Участник": {
                        u"СвФЛ": {
                            u"ИНН": partner_id.inn,
                            u"ЧастноеЛицо": u"Да"
                        }
                    }
                },
                "id": 0
            }
        response_json = requests.post(url=url, headers=self.headers, json=rpc_input, timeout=TIMEOUT).json()
        self.check_response_json(response_json)
        return response_json.get('result')

    def check_response_json(self, response_json):
        if response_json.get('error'):
            # response_json.get('error'):
            message = u'\n '.join(
                str(key) + u': ' + str(value) for key, value in response_json.get('error').items())
            # print(json.dumps(json_object, indent=1))
            raise Exception(message)

    def write_document(self, invoice):
        """https://sbis.ru/help/integration/api/all_methods/doc/"""
        url = 'https://online.sbis.ru/service/?srv=1'
        helper = QWebHelper()
        # counterparty
        if invoice.partner_id.parent_id:
            partner_id = invoice.partner_id.parent_id
        else:
            partner_id = invoice.partner_id
        if len(partner_id.inn) == 10:
            counterparty = {
                u"СвЮЛ": {
                    u"ИНН": partner_id.inn or '',
                    u"КПП": partner_id.kpp or '',
                    u"Название": partner_id.name
                }
            }
        elif len(partner_id.inn) == 12:
            counterparty = {
                u"СвФЛ": {
                    u"ИНН": partner_id.inn,
                }
            }
        # todo: Для физического лица
        #     "": объект:
        # "ИНН": строка, значение соответствует идентификационному номеру налогоплательщика
        # "КодФилиала": строка
        # "КодСтраны": строка, код страны в стандарте ISO 3166-1 numeric
        # "Фамилия": строка
        # "Имя": строка
        # "Отчество": строка
        # "СНИЛС": строка
        # "ЧастноеЛицо": строка "Да"/"Нет"
        else:
            raise Exception(
                'INN length does not correspond to LLC or individual entrepreneur. Invoice id: %s' % invoice.id)
        attachments = []
        invoice_date = datetime.strptime(invoice.date, DEFAULT_SERVER_DATE_FORMAT)
        for edi_document_id in invoice.edi_document_ids:
            file_name = edi_document_id.attachment_id.datas_fname or ''
            if file_name.endswith('.xml'):
                attachments.append({
                    u"Идентификатор": edi_document_id.guid,
                    u"Файл": {
                        u"ДвоичныеДанные": edi_document_id.attachment_id.datas,
                        u"Имя": file_name
                    }
                })
            else:
                attachments.append({
                    u"Идентификатор": edi_document_id.guid,
                    u"Файл": {
                        u"ДвоичныеДанные": edi_document_id.attachment_id.datas,
                        u"Имя": edi_document_id.name + u'.pdf',
                        u"Название": edi_document_id.name
                    }
                })
        rpc_input = {
            "jsonrpc": "2.0",
            "method": u"СБИС.ЗаписатьДокумент",
            "params": {
                u"Документ": {
                    u"Вложение": attachments,
                    u"Дата": invoice_date.strftime("%d.%m.%Y"),  # ДД.ММ.ГГГГ
                    u"Номер": helper.numer(invoice.number),
                    u"Сумма": invoice.amount_total,
                    # u"Идентификатор": "", Назначение идентификатора документа — необязательный этап.
                    # Если при загрузке документа на online.sbis.ru  идентификатор отсутствует,
                    # он будет присвоен документу сервером.
                    u"Контрагент": counterparty,
                    u"НашаОрганизация": {
                        u"СвЮЛ": {
                            u"ИНН": invoice.company_id.inn or '',
                            u"КПП": invoice.company_id.kpp or '',
                            u"Название": invoice.company_id.name
                        }
                    },
                    u"Примечание": invoice.comment or '',
                    u"Тип": u"ДокОтгрИсх"
                }
            },
            "id": 0
        }
        # todo Q: Примечание можно добавить налог? Q: "Редакция"?
        # u"Редакция": [
        #     {
        #         "ПримечаниеИС": "РеализацияТоваровУслуг:8bf669c4-042e-4854-b21b-673e8067e83e"
        #     }
        # ],
        response_json = requests.post(url=url, headers=self.headers, json=rpc_input, timeout=TIMEOUT).json()
        self.check_response_json(response_json)
        return response_json.get('result')

    def read_document(self, invoice):
        """https://sbis.ru/help/integration/api/all_methods/read_doc"""
        rpc_input = {
            "jsonrpc": "2.0",
            "method": u"СБИС.ПрочитатьДокумент",
            "params": {
                u"Документ": {
                    u"Идентификатор": invoice.sbis_guid,
                    # "ДопПоля": "ДополнительныеПоля"
                }
            },
            "id": 0
        }
        response_json = requests.post(url=self.url_service, headers=self.headers, json=rpc_input,
                                      timeout=TIMEOUT).json()
        self.check_response_json(response_json)
        return response_json.get('result')

    def authexit(self):
        """https://sbis.ru/help/integration/api/all_methods/authexit"""
        url = 'https://online.sbis.ru/auth/service/'
        rpc_input = {
            "jsonrpc": "2.0",
            "method": "СБИС.Выход",
            "params": {},
            "id": 0
        }
        response_json = requests.post(url=url, headers=self.headers, json=rpc_input, timeout=TIMEOUT).json()
        self.check_response_json(response_json)
