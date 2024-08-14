from odoo import api, fields, models

class Company(models.Model):
    _inherit = 'res.company'

    chief_id = fields.Many2one('res.users', 'Chief')
    print_facsimile = fields.Boolean('Print Facsimile',
                                     help="Check this for adding Facsimiles of responsible persons to documents.")
    print_stamp = fields.Boolean('Print Stamp',
                                 help="Check this for adding Stamp of company to documents.")
    print_anywhere = fields.Boolean('Print Anywhere',
                                    help="Uncheck this, if you want add Facsimile and Stamp only in email.",
                                    default=True)
    stamp = fields.Binary("Stamp")