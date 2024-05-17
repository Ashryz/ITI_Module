from odoo import models, fields


class HrInherit(models.Model):
    _inherit = "hr.employee"

    military_certificate = fields.Binary()
