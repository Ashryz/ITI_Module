from odoo import models, fields


class ItiTracks(models.Model):
    _name = "iti.tracks"

    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    students_ids = fields.One2many('iti.students', 'track_id')

