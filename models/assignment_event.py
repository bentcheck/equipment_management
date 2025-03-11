from odoo import models, fields

class AssignmentEvent(models.Model):
    _name = 'assignment.event'
    _description = 'Assignment Event'

    equipment_id = fields.Many2one(
        'it.equipment',
        string="Equipment",
        required=True,
        ondelete='cascade'
    )
    assigner_id = fields.Many2one(
        'res.users',
        string="Assigned By",
        required=True,
        default=lambda self: self.env.uid
    )
    assigned_person = fields.Many2one(
        'res.partner',
        string="Assigned Person",
        required=True
    )
    assigned_from = fields.Date(
        string="Assigned From",
        required=True
    )
    assigned_to = fields.Date(
        string="Assigned To",
        required=True
    )