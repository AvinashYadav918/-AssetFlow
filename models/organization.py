# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssetFlowDepartment(models.Model):
    _name = 'assetflow.department'
    _description = 'AssetFlow Department Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Department Name', required=True, tracking=True)
    code = fields.Char(string='Department Code', required=True)
    manager_id = fields.Many2one('res.users', string='Department Head', tracking=True)
    parent_id = fields.Many2one('assetflow.department', string='Parent Department', ondelete='restrict')
    child_ids = fields.One2many('assetflow.department', 'parent_id', string='Sub-departments')
    active = fields.Boolean(string='Active', default=True, tracking=True)

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'The department name must be unique!'),
        ('code_unique', 'unique(code)', 'The department code must be unique!')
    ]

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        for dept in self:
            if dept.parent_id == dept:
                raise ValidationError("A department cannot be its own parent.")


class AssetCategory(models.Model):
    _name = 'assetflow.category'
    _description = 'Asset Category'

    name = fields.Char(string='Category Name', required=True)
    code = fields.Char(string='Category Code', required=True, help="Prefix used for Asset Tag generation (e.g., EL for Electronics)")
    description = fields.Text(string='Description')
    warranty_required = fields.Boolean(string='Requires Warranty Details', default=False)
    default_warranty_months = fields.Integer(string='Default Warranty (Months)', default=12)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Category code must be unique!')
    ]


class AssetFlowEmployee(models.Model):
    _name = 'assetflow.employee'
    _description = 'AssetFlow Employee Directory'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Full Name', required=True, tracking=True)
    email = fields.Char(string='Email Address', required=True, tracking=True)
    user_id = fields.Many2one('res.users', string='Related User Account', help="Links to system login account")
    department_id = fields.Many2one('assetflow.department', string='Department', tracking=True)
    
    role = fields.Selection([
        ('employee', 'Regular Employee'),
        ('dept_head', 'Department Head'),
        ('asset_manager', 'Asset Manager'),
        ('admin', 'Administrator')
    ], string='Assigned Role', default='employee', required=True, tracking=True)
    
    status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ], string='Status', default='active', tracking=True)

    _sql_constraints = [
        ('email_unique', 'unique(email)', 'An employee with this email already exists!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('email'):
            vals['email'] = vals['email'].strip().lower()
        return super(AssetFlowEmployee, self).create(vals)
