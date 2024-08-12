from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta

class BookLibrary(models.Model):
    _name = "book.library"
    _description = "Perpustakaan Buku"
    _sql_constraints = [
        ('unique_isbn', 'UNIQUE(code_formatted)', 'Kode ISBN harus unik.')
    ]

    name = fields.Char(string = "Judul", required = True)
    category = fields.Selection([('general', 'Umum'), ('it', 'Teknologi Informasi'), ('health', 'Kesehatan'), ('politics', 'Politik')], string = "Kategori", default = "general")
    release_date = fields.Date(string = "Tanggal Rilis")
    author_ids = fields.Many2many('res.partner','book_author_rel', 'book_id', 'author_id', string = "Penulis", domain = [('author', '=', True)])
    code_input = fields.Char(string = "Input ISBN", required = True)
    code_formatted = fields.Char(string = "Kode ISBN", compute = "_compute_isbn_formatted", readonly = True, default = '-')
    transaction_ids = fields.Many2many('book.transaction', 'book_transaction_rel', 'book_id', 'transaction_id', string="Transaksi")
    price = fields.Float(string = "Harga", default = 0.0)
    quantity = fields.Integer(string = "Stok Buku", required=True, default=0)

    @api.constrains('code_input')
    def _check_isbn(self):
        for data in self:
            cleaned_isbn = data.code_input.replace('-', '').strip()
            if len(cleaned_isbn) != 13 or not cleaned_isbn.isdigit():
                raise ValidationError("Kode ISBN harus diisi dengan 13 angka")

    @api.depends('code_input')
    def _compute_isbn_formatted(self):
        for data in self:
            cleaned_isbn = data.code_input.replace('-', '').strip()
            if len(cleaned_isbn) == 13 and cleaned_isbn.isdigit():
                data.code_formatted = f'ISBN-{cleaned_isbn[:3]}-{cleaned_isbn[3]}-{cleaned_isbn[4:8]}-{cleaned_isbn[8:12]}-{cleaned_isbn[12]}' 
                continue
            else:
                data.code_formatted = ''   
