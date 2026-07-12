# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssetAllocation(models.Model):
    _name = 'assetflow.allocation'
    _description = 'Asset Allocation'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True, domain=[('state', '=', 'available')])
    employee_id = fields.Many2one('assetflow.employee', string='Employee', required=True)
    department_id = fields.Many2one('assetflow.department', string='Department')
    allocated_date = fields.Date(string='Allocation Date', default=fields.Date.context_today)
    expected_return_date = fields.Date(string='Expected Return Date')
    notes = fields.Text(string='Check-in/Out Notes')
    
    state = fields.Selection([
        ('active', 'Active'),
        ('returned', 'Returned'),
        ('transferred', 'Transferred')
    ], string='Status', default='active', tracking=True)

    @api.constrains('asset_id', 'state')
    def _check_double_allocation(self):
        for rec in self:
            if rec.state == 'active':
                # Conflict rule handling: Block if asset is already active in another record
                overlap = self.search([
                    ('asset_id', '=', rec.asset_id.id),
                    ('state', '=', 'active'),
                    ('id', '!=', rec.id)
                ])
                if overlap:
                    raise ValidationError(f"Conflict! This asset is currently held by {overlap[0].employee_id.name}. Please initiate a Transfer Request instead.")

    def action_return_asset(self):
        for rec in self:
            rec.write({'state': 'returned'})
            rec.asset_id.write({'state': 'available'})


class ResourceBooking(models.Model):
    _name = 'assetflow.booking'
    _description = 'Shared Resource Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    asset_id = fields.Many2one('assetflow.asset', string='Resource/Asset', required=True, domain=[('is_shared', '=', True)])
    employee_id = fields.Many2one('assetflow.employee', string='Booked By', required=True)
    start_time = fields.Datetime(string='Start Time', required=True)
    end_time = fields.Datetime(string='End Time', required=True)
    
    state = fields.Selection([
        ('upcoming', 'Upcoming'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], string='Booking Status', default='upcoming', tracking=True)

    @api.constrains('start_time', 'end_time', 'asset_id')
    def _check_booking_overlap(self):
        for rec in self:
            if rec.start_time >= rec.end_time:
                raise ValidationError("End Time must be strictly after Start Time.")
            
            # Time-slot overlap validation logic
            overlap = self.search([
                ('asset_id', '=', rec.asset_id.id),
                ('state', 'in', ['upcoming', 'ongoing']),
                ('id', '!=', rec.id),
                ('start_time', '<', rec.end_time),
                ('end_time', '>', rec.start_time)
            ])
            if overlap:
                raise ValidationError("Time-slot overlap detected! This shared resource is already booked during the requested window.")
