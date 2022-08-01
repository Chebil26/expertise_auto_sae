from odoo import models, fields, api


class ChoixPrixPiece(models.TransientModel):
    _name = 'choix.prix.piece.wizard'

    fourniture_id = fields.Many2one(comodel_name='liste.fournitures', string="Ligne Fourniture",
                                    default=lambda self: self.env.context.get('active_id'), readonly=True)
    type_montant = fields.Selection(string='Type Montant',
                                    selection=[('min', 'Montant Min'), ('moy', 'Montant Moy'), ('max', 'Montant Max'),
                                               ('facture', 'Montant Facturé'),
                                               ('a_saisir_h', 'Montant à Saisir HT'),
                                               ('a_saisir_t', 'Montant à Saisir TTC')],
                                    default='moy', required=True)
    amount_saisi = fields.Monetary(string='P.U à Saisir', currency_field='currency_id', required=True)

    def _get_default_amount_min(self):
        context = dict(self._context) or {}
        fourniture = self.env['liste.fournitures'].browse(context.get('active_id', False))
        return fourniture.piece_id.amount_min

    amount_min = fields.Monetary(string='P.U Min', default=_get_default_amount_min,
                                 currency_field='currency_id')

    def _get_default_amount_moy(self):
        context = dict(self._context) or {}
        fourniture = self.env['liste.fournitures'].browse(context.get('active_id', False))
        return fourniture.piece_id.amount_moy

    amount_moy = fields.Monetary(string='P.U Moy', default=_get_default_amount_moy,
                                 currency_field='currency_id')

    def _get_default_amount_max(self):
        context = dict(self._context) or {}
        fourniture = self.env['liste.fournitures'].browse(context.get('active_id', False))
        return fourniture.piece_id.amount_max

    amount_max = fields.Monetary(string='P.U Max', default=_get_default_amount_max,
                                 currency_field='currency_id')

    def _get_default_amount_facture(self):
        context = dict(self._context) or {}
        fourniture = self.env['liste.fournitures'].browse(context.get('active_id', False))
        return fourniture.piece_id.amount_fact

    amount_facture = fields.Monetary(string='P.U Facturé', default=_get_default_amount_facture,
                                     currency_field='currency_id')

    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id")

    def confirmer(self):
        montant = 0
        if self.type_montant == 'min':
            montant = self.amount_min
        elif self.type_montant == 'moy':
            montant = self.amount_moy
        elif self.type_montant == 'max':
            montant = self.amount_max
        elif self.type_montant == 'facture':
            montant = self.amount_facture
        elif self.type_montant == 'a_saisir_h':
            montant = self.amount_saisi
        elif self.type_montant == 'a_saisir_t':
            taxe = 1
            if self.env['ir.config_parameter'].sudo().get_param('expertise_auto_sae.taxe_global_auto'):
                taxe_id = self.env['account.tax'].search([('id', '=', int(
                    self.env['ir.config_parameter'].sudo().get_param('expertise_auto_sae.taxe_global_auto')))])
                taxe = taxe + (taxe_id.amount / 100)
            montant = self.amount_saisi / taxe

        self.fourniture_id.write({"prix_ht": montant})
