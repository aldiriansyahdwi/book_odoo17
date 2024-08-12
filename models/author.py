from odoo import api, fields, models

class Author(models.Model):
    _inherit = "res.partner"

    author = fields.Boolean(string = "Penulis", default=True)
    book_ids = fields.Many2many('book.library', 'book_author_rel','author_id', 'book_id', string='Penulis Buku', readonly=True)