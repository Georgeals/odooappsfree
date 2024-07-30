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

# from odoo import api, fields, models, _
from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sbis_login = fields.Char(strng="Логин",
                             related='company_id.sbis_login', readonly=False,)
    sbis_password = fields.Char(string="Пароль",
                                related='company_id.sbis_password', readonly=False,)
    sbis_number_account = fields.Char(string="Номер Аккаунта",
                                      related='company_id.sbis_number_account',
                                      readonly=False,
                                      help="""
Если у пользователя есть доступ в разные кабинеты СБИС по одному логину/паролю, в запросе в поле «НомерАккаунта»
укажите аккаунт, в который нужно войти. Если номер аккаунта в запросе не указан, будет выполнен вход в тот кабинет,
в котором пользователь авторизовался в предыдущий раз, в том числе через сайт.
Для пользователей с одним аккаунтом номер в запросе указывать не нужно.
Посмотреть номер аккаунта можно в личном кабинете или лицензионном договоре.""")
