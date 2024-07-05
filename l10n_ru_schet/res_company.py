# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2018 CodUP (<http://codup.com>).
#
##############################################################################

from odoo import api, fields, models

class Company(models.Model):
    _inherit = 'res.company'

    inn = fields.Char(related='partner_id.inn')  # todo Удалить поле INN, в место него использовать стандартное поле VAT
    kpp = fields.Char(related='partner_id.kpp')
    okpo = fields.Char(related='partner_id.okpo')
    chief_id = fields.Many2one('res.users', 'Chief')
    accountant_id = fields.Many2one('res.users', 'General Accountant')
    print_facsimile = fields.Boolean('Print Facsimile', help="Check this for adding Facsimiles of responsible persons to documents.")
    print_stamp = fields.Boolean('Print Stamp', help="Check this for adding Stamp of company to documents.")
    stamp = fields.Binary("Stamp")
    print_anywhere = fields.Boolean('Print Anywhere', help="Uncheck this, if you want add Facsimile and Stamp only in email.", default=True)
    is_ip = fields.Boolean('Индивидуальный предприниматель', default=False)  
    is_self_employed = fields.Boolean('Самозанятый', default=False)   
    # todo: Сточки зрения интерфейса тип поля выбран некорректный, так как физ. лицо не может быть одновременно и ИП и Самозанятый. 
    # todo Сделать по другому. Возможные значения: 1) Физическое лицо (самозанятый) 2) Индивидуальный предприниматель (ИП) 3) Юридическое лицо (ООО, АО, ПАО), 
    # в модели res.partner есть переключатель Individual\Company, нужно это поле вывести в res.company. Так как на печатную форму счета это влияет одинаково, то будет:
    # Individual для
    #   1) Физическое лицо (самозанятый) 
    #   2) Индивидуальный предприниматель (ИП)
    # Company для 
    #   Юридическое лицо (ООО, АО, ПАО)
    #  добавить это в help нового поля company_type.
    bank_id = fields.Many2one('res.partner.bank', 'Bank account for orders.')   # todo добавить для поля дефолтное значение - первый их банковских счетов компании. Добавить домен, чтобы в форме открывались счета только компании

    @api.onchange('is_ip')
    def _onchange_is_ip(self):
        if self.is_ip:
            self.is_self_employed = False

    @api.onchange('is_self_employed')
    def _onchange_is_self_employed(self):
        if self.is_self_employed:
            self.is_ip = False
