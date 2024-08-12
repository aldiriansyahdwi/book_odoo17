from odoo import api, fields, models
from odoo.exceptions import ValidationError
from datetime import timedelta

class BookTransaction(models.Model):
    _name = "book.transaction"
    _description = "Transaksi Penyewaan Buku"

    rental_date = fields.Date(string = 'Tanggal Penyewaan', default=lambda self: fields.Date.context_today(self))
    renter_id = fields.Many2one('book.member', string = "Penyewa", domain=[('state', '=', 'approved')])
    book_ids = fields.Many2many('book.library', 'book_transaction_rel', 'transaction_id','book_id')
    state = fields.Selection([('rented', 'Sedang Dipinjam'), ('overdue', 'Belum Dikembalikan'), ('done', 'Selesai')], string = "Status", readonly=True, default = 'rented')
    return_date = fields.Date(string = "Tanggal Mengembalikan", default = lambda self: self._get_default_return_date())
    rent_fee = fields.Float(string = "Biaya Penyewaan", compute = "_compute_rent_fee", store = True)
    return_state = fields.Boolean(string = "Pengembalian", default=False)

    book_rented_ids = fields.One2many(
        'book.transaction.line',
        'transaction_id',
        string='Buku Disewa'
    )

    def action_return(self):
        self.write({'state': 'done', 'return_state': True})
        
    @api.depends('book_rented_ids')
    def _compute_rent_fee(self):
        for transaction in self:
            if transaction.state == 'rented':
                transaction.rent_fee = sum(line.book_id.price * line.quantity for line in transaction.book_rented_ids)

    @api.model
    def create(self, vals):
        record = super(BookTransaction, self).create(vals)
        record._update_book_quantities()
        return record

    def write(self, vals):
        # update quantity jika state menjadi 'done'
        if 'state' in vals and vals['state'] == 'done':
            for transaction in self:
                if transaction.state != 'done':
                    for line in transaction.book_rented_ids:
                        book = line.book_id
                        book.quantity += line.quantity
        res = super(BookTransaction, self).write(vals)

        # if 'state' in vals and vals['state'] != 'done':
        #     self._update_book_quantities()
        return res
        

    def _update_book_quantities(self):
        for transaction in self:
            rented_books = transaction.book_rented_ids
            for line in rented_books:
                book = line.book_id
                if book.quantity < line.quantity:
                    raise ValidationError('Kuantitas buku tidak mencukupi untuk dipinjam.')
                else:
                    book.quantity -= line.quantity
                    book.transaction_ids =[(4, transaction.id)]

    def unlink(self):
        for transaction in self:
            if transaction.state != 'done':
                for line in transaction.book_rented_ids:
                    book = line.book_id
                    book.quantity += line.quantity
        return super(BookTransaction, self).unlink()
    
    def _get_default_return_date(self):
        rental_date = fields.Date.context_today(self)
        return rental_date + timedelta(days=7)

    def cron_overdue_rental(self):
        now = fields.Date.today()
        overdue_ids = self.search([('return_date', '<', now), ('state', '=', 'rented')])
        overdue_ids.write({'state': 'overdue'})

class BookTransactionLine(models.Model):
    _name = "book.transaction.line"
    _description = "Baris Peminjaman Buku"

    transaction_id = fields.Many2one('book.transaction', string='Transaksi')
    book_id = fields.Many2one('book.library', string='Buku')
    quantity = fields.Integer(string='Kuantitas', required=True, default=1)