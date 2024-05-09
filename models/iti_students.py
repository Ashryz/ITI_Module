from odoo import models, fields


class ItiStudents(models.Model):
    _name = "iti.students"

    name = fields.Char()
    birth_date = fields.Date()
    salary = fields.Integer()
    image = fields.Binary()
    address = fields.Text()
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female')]
    )
    accepted = fields.Boolean()
