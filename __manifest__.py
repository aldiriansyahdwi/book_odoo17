# -*- coding: utf-8 -*-
{
    'name': "Perpustakaan Buku",

    'summary': "Perpustakaan Buku Odoo17",

    'description': """
Perpustakaan Buku menggunakan odoo17
    """,

    'author': "Aldiriansyah Dwi",
    'website': "https://github.com/aldiriansyahdwi",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'report/report_action.xml',
        'report/report_book_member.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/schedular_data.xml',
        'views/book_views.xml',
        'views/author_views.xml',
        'views/member_views.xml',
        'views/transaction_views.xml',
        'views/menuitem_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

