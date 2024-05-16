from odoo import models, fields, api
from odoo.exceptions import UserError


class ItiStudents(models.Model):
    _name = "iti.students"

    name = fields.Char(required=True)
    birth_date = fields.Date()
    salary = fields.Integer()
    tax = fields.Float(compute="calc_salary")
    net_salary = fields.Float(compute="calc_salary", store=True)
    image = fields.Binary()
    address = fields.Text()
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female')]
    )
    accepted = fields.Boolean()
    cv = fields.Html()
    track_id = fields.Many2one("iti.tracks")
    track_capacity = fields.Integer(related="track_id.capacity")
    skills_ids = fields.Many2many("iti.skills")
    state = fields.Selection([
        ('applied', 'Applied'),
        ('first', 'Set First Interview'),
        ('second', 'Set Second Interview'),
        ('passed', 'Passed'),
        ('rejected', 'Rejected')
    ], default='applied')
    email = fields.Char(readonly=True)

    @api.onchange("gender")
    def gender_onchange(self):
        if not self.gender:
            return {}
        if self.gender == 'm':
            self.salary = 10000
        elif self.gender == 'f':
            self.salary = 8000
        return {
            'warning': {
                'title': 'Warning!',
                'message': 'default salary for male 1000 when you change the gender to female, '
                           'the salary automatically changed to 8000 '
            }
        }

    def change_state(self):
        if self.state == 'applied':
            self.state = 'first'
        elif self.state == 'first':
            self.state = 'second'
        elif self.state in ['passed', 'rejected']:
            self.state = 'applied'

    def set_passed(self):
        self.state = 'passed'

    def set_rejected(self):
        self.state = 'rejected'

    @api.model
    def create(self, vals):
        new_student = super().create(vals)
        name_split = new_student.name.split()
        new_student.email = f"{name_split[0][0]}{name_split[1]}_sd@iti.edu.eg"
        return new_student

    def write(self, vals):
        if "name" in vals:
            name_split = vals['name'].split()
            vals["email"] = f"{name_split[0][0]}{name_split[1]}_sd@iti.edu.eg"
        super().write(vals)

    def unlink(self):
        for rec in self:
            if rec.state in ['passed', 'rejected']:
                raise UserError("You can't delete passed or rejected student")
        super().unlink()

    @api.constrains("salary")
    def check_salary(self):
        if self.salary > 10000 or self.salary < 5000:
            raise UserError("salary is not available, it must be between 5k-10k")

    @api.constrains("track_id")
    def check_track_capacity(self):
        count_students = len(self.track_id.students_ids)
        track_capacity = self.track_id.capacity
        if count_students > track_capacity:
            raise UserError("this track is full of students")

    @api.depends("salary")
    def calc_salary(self):
        for student in self:
            student.tax = student.salary * 0.02
            student.net_salary = student.salary - student.tax
