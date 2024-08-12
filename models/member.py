from odoo import api, fields, models
from odoo.exceptions import ValidationError

class BookMember(models.Model):
    _name = "book.member"
    _description = "Anggota Perpustakaan"

    name = fields.Char(string = "Nama", required = True)
    identity_number = fields.Char(string = "Nomor Identitas", required = True)
    identity_type = fields.Selection([('id_card', 'KTP'), ('driving_license', 'SIM'), ('passport', 'Passport')], string = "Tipe Identitas", required = True, default = "id_card")
    state = fields.Selection([('draft','Draft'), ('approved','Approved')], string = "Status", readonly = True, default = 'draft')
    transaction_line = fields.One2many('book.transaction', 'renter_id', string="Transaksi")

    @api.constrains('identity_number', 'identity_type')
    def check_unique_identity(self):
        for id in self:
            existing_id = self.search([('identity_type', '=', id.identity_type), ('identity_number', '=', id.identity_number), ('id', '!=', id.id)])

            if existing_id:
                raise ValidationError("Tipe identitas dengan nomor yang sama sudah ada / tidak boleh sama.")
    
    def action_approve(self):
        self.write({'state': 'approved'})
    
    def action_revoke(self):
        self.write({'state': 'draft'})

    def action_print_member(self): 
        return self.env.ref('odoo_buku.action_report_book_member').report_action(self)