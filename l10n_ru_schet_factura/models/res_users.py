from odoo import api, fields, models


class Users(models.Model):
    _inherit = "res.users"

    print_facsimile = fields.Boolean(related="company_id.print_facsimile")
    facsimile = fields.Binary("Facsimile")

    def get_initilals_for_report(self):
        fio = self.name
        if not fio:
            return ''
        return (
                fio.split()[0]
                + " "
                + "".join([fio[0:1] + "." for fio in fio.split()[1:]])
        ).strip()