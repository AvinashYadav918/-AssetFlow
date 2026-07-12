# -*- coding: utf-8 -*-
{
    'name': 'AssetFlow - Enterprise Asset & Resource Management',
    'version': '1.0',
    'summary': 'Centralized ERP platform to track, allocate, and maintain assets.',
    'description': """
        AssetFlow simplifies and digitizes how organizations track, allocate, 
        and maintain their physical assets and shared resources.
    """,
    'author': 'Orixa Developer Team',  
    'category': 'Operations',
    'depends': ['base', 'mail'],  
    'data': [
        'security/ir.model.access.csv',
        'views/menus.xml',
        'views/organization_views.xml',
        'views/asset_views.xml',
        'views/operations_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
