# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2018 ArtLine (<https://artline-erp.ru/>).
#
##############################################################################

from odoo import api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    print_facsimile = fields.Boolean(related="company_id.print_facsimile")
    facsimile = fields.Binary("Facsimile")

    def get_initilals_for_report(self):
        # todo Решение не надежное, так как имя могут записать в любом порядке, например first name затем last name.
        # todo В репортах используется модель юзера для печати подписей и тд. Сделать имя подписанта как char поле в модели компании а подпись как поле в модели юзера?
        # Сделать пока простое решение в место chief_id и accountant_id сделать простые Char поля, в которые руками будут вписывать ФИО. Добавить ФИО в демо данные.
        self.ensure_one()
        fio = self.name
        return (
                fio.split()[0]
                + " "
                + "".join([fio[0:1] + "." for fio in fio.split()[1:]])
        ).strip()
