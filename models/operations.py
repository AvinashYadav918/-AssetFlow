# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssetMaintenance(models.Model):
    _name = 'assetflow.maintenance'
    _description = 'Asset Maintenance Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    asset_id = fields.Many2one('assetflow.asset', string='Asset', required=True)
    employee_id = fields.Many2one('assetflow.employee', string='Raised By', required=True)
    description = fields.Text(string='Issue Description', required=True)
    priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], string='Priority', default='medium', tracking=True)
    
    state = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('progress', 'In Progress'),
        ('resolved', 'Resolved')
    ], string='Status', default='pending', tracking=True)

    def action_approve(self):
        for rec in self:
            rec.write({'state': 'approved'})
            # Auto-update asset state to Under Maintenance upon approval
            rec.asset_id.write({'state': 'maintenance'})

    def action_resolve(self):
        for rec in self:
            rec.write({'state': 'resolved'})
            # Restore asset state back to Available once repaired
            rec.asset_id.write({'state': 'available'})


class AssetAuditCycle(models.Model):
    _name = 'assetflow.audit'
    _description = 'Asset Audit Cycle'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Audit Cycle Name', required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.context_today)
    end_date = fields.Date(string='End Date')
    auditor_ids = fields.Many2many('assetflow.employee', string='Assigned Auditors')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'In Progress'),
        ('closed', 'Closed')
    ], string='Status', default='draft', tracking=True)
    
    line_ids = fields.One2many('assetflow.audit.line', 'audit_id', string='Audit Verification Lines')

    def action_start_audit(self):
        self.write({'state': 'open'})

    def action_close_audit(self):
        for rec in self:
            # Human-like sanity check before locking the cycle
            if not rec.line_ids:
                raise ValidationError("Cannot close an audit cycle without verification records.")
            
            rec.write({'state': 'closed'})
            # Auto-update statuses for items flagged as Lost during the verification process
            for line in rec.line_ids:
                if line.verification_result == 'missing':
                    line.asset_id.write({'state': 'lost'})


class AssetAuditLine(models.Model):
    _name = 'assetflow.audit.line'
    _description = 'Asset Audit Verification Line'

    audit_id = fields.Many2one('assetflow.audit', string='Audit Cycle', ondelete='cascade')
    asset_id = fields.Many2one('assetflow.asset', string='Asset/Resource', required=True)
    verification_result = fields.Selection([
        ('verified', 'Verified / Present'),
        ('missing', 'Missing'),
        ('damaged', 'Damaged')
    ], string='Verification Status', default='verified')
    notes = fields.Text(string='Auditor Remarks')
