from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class ITEquipment(models.Model):
    _name = 'it.equipment'
    _description = 'IT Equipment'

    name = fields.Char(string='Serial Number', required=True)
    acquisition_price = fields.Float(string='Acquisition Price', required=True)
    supplier = fields.Char(string='Supplier')
    state = fields.Selection([
        ('in_stock', 'In Stock'),
        ('assigned', 'Assigned'),
        ('scrapped', 'Scrapped')
    ], string='Status', default='in_stock', required=True)
    assigned_person = fields.Many2one(
        'res.partner',
        string='Assigned Person',
        domain=[('is_company', '=', False)]
    )
    assigned_from = fields.Date(string='Assigned From')
    assigned_to = fields.Date(string='Assigned To')
    assignment_event_ids = fields.One2many('assignment.event', 'equipment_id', string="Assignment Events", readonly=True)

    @api.constrains('state', 'assigned_person', 'assigned_from', 'assigned_to')
    def _check_assigned_fields(self):
        for rec in self:
            if rec.state == 'assigned':
                if not rec.assigned_person:
                    raise ValidationError("When the equipment is assigned, you must select an Assigned Person.")
                if rec.assigned_person.is_company:
                    raise ValidationError("The Assigned Person must be an employee (a person), not a company.")
                if not rec.assigned_from or not rec.assigned_to:
                    raise ValidationError(
                        "When the equipment is assigned, both 'Assigned From' and 'Assigned To' dates must be set.")
                if rec.assigned_from > rec.assigned_to:
                    raise ValidationError("The 'Assigned From' date cannot be after the 'Assigned To' date.")

    @api.onchange('state')
    def _onchange_state(self):
        if self.state != 'assigned':
            self.assigned_person = False
            self.assigned_from = False
            self.assigned_to = False

    @api.model_create_multi
    def create(self, vals_list):
        # Process each set of values individually
        for vals in vals_list:
            if vals.get('state', 'in_stock') != 'assigned':
                vals['assigned_person'] = False
                vals['assigned_from'] = False
                vals['assigned_to'] = False

        records = super(ITEquipment, self).create(vals_list)

        for record in records:
            if record.state == 'assigned':
                self.env['assignment.event'].create({
                    'equipment_id': record.id,
                    'assigner_id': self.env.uid,
                    'assigned_person': record.assigned_person.id,
                    'assigned_from': record.assigned_from,
                    'assigned_to': record.assigned_to,
                })
        return records

    def write(self, vals):
        if 'state' in vals and vals.get('state') != 'assigned':
            vals['assigned_person'] = False
            vals['assigned_from'] = False
            vals['assigned_to'] = False
        res = super(ITEquipment, self).write(vals)
        for rec in self:
            if rec.state == 'assigned' and set(vals.keys()) & {'state', 'assigned_person', 'assigned_from', 'assigned_to'}:
                self.env['assignment.event'].create({
                    'equipment_id': rec.id,
                    'assigner_id': self.env.uid,
                    'assigned_person': rec.assigned_person.id,
                    'assigned_from': rec.assigned_from,
                    'assigned_to': rec.assigned_to,
                })
        return res