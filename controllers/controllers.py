# -*- coding: utf-8 -*-
# from odoo import http


# class OdooBuku(http.Controller):
#     @http.route('/odoo_buku/odoo_buku', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_buku/odoo_buku/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_buku.listing', {
#             'root': '/odoo_buku/odoo_buku',
#             'objects': http.request.env['odoo_buku.odoo_buku'].search([]),
#         })

#     @http.route('/odoo_buku/odoo_buku/objects/<model("odoo_buku.odoo_buku"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_buku.object', {
#             'object': obj
#         })

