from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # inn = fields.Char('INN', size=12)
    # kpp = fields.Char('KPP', size=9)
    # okpo = fields.Char('OKPO', size=14)

    def get_representation_act(self):
        self.ensure_one()
        name = self.with_context({"lang": self.env.lang})._get_complete_name()
        if vat := self.vat:
            name += f", ИНН {vat}"
        if kpp := self.kpp:
            name += f", КПП {kpp}"
        if address := self._display_address(without_company=True):
            name += f", {address}"
        if phone := self.phone:
            name += f", тел.: {phone}"
        elif parent_phone := self.parent_id.phone:
            name += f", тел.: {parent_phone}"

        bank = None
        if self.bank_ids:
            bank = self.bank_ids[0]
        elif self.parent_id.bank_ids:
            bank = self.parent_id.bank_ids[0]
        if bank and bank.acc_number:
            name += f", р/сч {bank.acc_number}"
        if bank and bank.bank_name:
            name += f", в банке {bank.bank_name}"
        if bank and bank.bank_bic:
            name += f", БИК {bank.bank_bic}"
        if bank and bank.bank_corr_acc:
            name += f", к/с {bank.bank_corr_acc}"
        return name
