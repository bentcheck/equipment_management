{
    'name': 'it_equipment_management',
    'version': '1.0',
    'category': 'Inventory/IT',
    'summary': 'Manage IT equipment',
    'author': 'Sergiu Ghita',
    'depends': ['base'],
    'data': [
        "security/ir.model.access.csv",
        'views/it_equipment_views.xml',
        'views/report_assignment.xml',
        'report/it_equipment_templates.xml',
        'report/it_equipment_reports.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'it_equipment_management/static/src/xml/state_icon_field.xml',
            'it_equipment_management/static/src/js/state_icon_field.js',
        ],
    },
    'installable': True,
    'application': True,
}