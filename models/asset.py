# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AssetFlowAsset(models.Model):
    _name = 'assetflow.asset'
    _description = 'Asset Registry'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Asset Name', required=True, tracking=True)
    asset_tag = fields.Char(string='Asset Tag', required=True, copy=False, readonly=True, index=True)
    category_id = fields.Many2one('assetflow.category', string='Category', required=True, tracking=True)
    serial_number = fields.Char(string='Serial Number', tracking=True)
    acquisition_date = fields.Date(string='Acquisition Date', default=fields.Date.context_today)
    acquisition_cost = fields.Float(string='Acquisition Cost', help="For ranking/reports only")
    condition = fields.Selection([
        ('new', 'New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('damaged', 'Damaged')
    ], string='Condition', default='good', tracking=True)
    
    location = fields.Char(string='Current Location', tracking=True)
    is_shared = fields.Boolean(string='Shared / Bookable Resource', default=False)
    
    state = fields.Selection([
        ('available', 'Available'),
        ('allocated', 'Allocated'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
        ('lost', 'Lost'),
        ('retired', 'Retired'),
        ('disposed', 'Disposed')
    ], string='Status', default='available', tracking=True, required=True)

    _sql_constraints = [
        ('asset_tag_unique', 'unique(asset_tag)', 'The Asset Tag must be unique!'),
        ('serial_unique', 'unique(serial_number)', 'The Serial Number must be unique!')
    ]

    @api.model
    def create(self, vals):
        # Human-like unique sequence generation logic based on Category code
        if not vals.get('asset_tag'):
            category = self.env['assetflow.category'].browse(vals.get('category_id'))
            prefix = category.code if category and category.code else 'AF'
            
            last_asset = self.search([('asset_tag', 'like', f'{prefix}-%')], order='id desc', limit=1)
            if last_asset:
                try:
                    last_seq = int(last_asset.asset_tag.split('-')[1])
                    new_seq = last_seq + 1
                except (ValueError, IndexError):
                    new_seq = 1
            else:
                new_seq = 1
            
            vals['asset_tag'] = f"{prefix}-{new_seq:04d}"
            
        return super(AssetFlowAsset, self).create(vals)
