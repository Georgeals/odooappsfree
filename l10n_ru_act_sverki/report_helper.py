# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo
#    Copyright (C) 2014-2016 CodUP (<http://codup.com>).
#
##############################################################################

import re


class QWebHelper(object):

    def img(self, img, type='png', width=0, height=0) :
        if width :
            width = "width='%spx'"%(width)
        else :
            width = " "
        if height :
            height = "height='%spx'"%(height)
        else :
            height = " "
        toreturn = "<img %s %s src='data:image/%s;base64,%s' />"%(
            width,
            height,
            type,
            str(img))
        return toreturn

    def numer(self, name):
        if name:
            numeration = re.findall('\d+$', name)
            if numeration: return numeration[0]
        return ''

    def initials(self, fio):
        if fio:
            return (fio.split()[0]+' '+''.join([fio[0:1]+'.' for fio in fio.split()[1:]])).strip()
        return ''

    def address(self, partner):
        repr = []
        if partner.zip: repr.append(partner.zip)
        if partner.city: repr.append(partner.city)
        if partner.street: repr.append(partner.street)
        if partner.street2: repr.append(partner.street2)
        return ', '.join(repr)

    def representation(self, partner):
        repr = []
        if partner.name: repr.append(partner.name)
        if partner.inn: repr.append(u"ИНН " + partner.inn)
        if partner.kpp: repr.append(u"КПП " + partner.kpp)
        repr.append(self.address(partner))
        return ', '.join(repr)

    def full_representation(self, partner):
        repr = [self.representation(partner)]
        if partner.phone: repr.append(u"тел.: " + partner.phone)
        elif partner.parent_id.phone: repr.append(u"тел.: " + partner.parent_id.phone)
        bank = None
        if partner.bank_ids: bank = partner.bank_ids[0]
        elif partner.parent_id.bank_ids: bank = partner.parent_id.bank_ids[0]
        if bank and bank.acc_number: repr.append(u"р/сч " + bank.acc_number)
        if bank and bank.bank_name: repr.append(u"в банке " + bank.bank_name)
        if bank and bank.bank_bic: repr.append(u"БИК " + bank.bank_bic)
        if bank and bank.bank_corr_acc: repr.append(u"к/с " + bank.bank_corr_acc)
        return ', '.join(repr)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: