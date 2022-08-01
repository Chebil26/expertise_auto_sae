from odoo import models, fields, api, _


class Piece(models.TransientModel):
    _name = 'sae.liste.piece'

    piece_id = fields.Many2one(comodel_name='sae.piece', string="Piece", readonly=1)
    name = fields.Char(related="piece_id.name", readonly=True)
    code = fields.Char(related="piece_id.code", readonly=True)
    taxe_id = fields.Many2one(related="piece_id.taxe_id", readonly=True)
    vetuste = fields.Boolean(related="piece_id.vetuste", readonly=True)
    concessionaire = fields.Boolean(related="piece_id.concessionaire", readonly=True)
    is_checked = fields.Boolean()
    annee = fields.Char(related="piece_id.annee", readonly=True)
    amount_moy = fields.Monetary(related="piece_id.amount_moy", readonly=True)
    amount_min = fields.Monetary(related="piece_id.amount_min", readonly=True)
    amount_max = fields.Monetary(related="piece_id.amount_max", readonly=True)
    amount_fact = fields.Monetary(related="piece_id.amount_fact", readonly=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id")
    marque_id = fields.Many2one(related="piece_id.marque_id", readonly=True)
    mdl_id = fields.Many2one(related="piece_id.mdl_id", readonly=True)
    num_fourniture = fields.Integer(string="Num Fourniture")


class RecherchePiece(models.TransientModel):
    _name = 'sae.recherche.piece.wizard'

    def _get_default_marque_id(self):
        context = dict(self._context) or {}
        fourniture = self.env['sae.expertise.auto'].browse(context.get('active_id', False))
        return fourniture.mrqe_id.id

    def _get_default_modele_id(self):
        context = dict(self._context) or {}
        dossier = self.env['sae.expertise.auto'].browse(context.get('active_id', False))
        return dossier.mdle_id.id

    def _get_default_annee(self):
        context = dict(self._context) or {}
        dossier = self.env['sae.expertise.auto'].browse(context.get('active_id', False))
        return str(dossier.an_mec)

    def rechercher(self):
        data = []
        self.update({"liste_pieces_ids": False})

        if self.marque_id and not self.modele_id and not self.annee:
            if self.designation_piece:
                pieces = self.env['sae.piece'].search(
                    [('marque_id', '=', self.marque_id.id), ('name', "ilike", self.designation_piece)])

            else:
                pieces = self.env['sae.piece'].search([('marque_id', '=', self.marque_id.id)])
        elif not self.marque_id and self.modele_id and not self.annee:
            if self.designation_piece:
                pieces = self.env['sae.piece'].search(
                    [('mdl_id', '=', self.modele_id.id), ('name', "ilike", self.designation_piece)])
            else:
                pieces = self.env['sae.piece'].search([('mdl_id', '=', self.modele_id.id)])
        elif not self.marque_id and not self.modele_id and self.annee:
            if self.designation_piece:
                pieces = self.env['sae.piece'].search(
                    [('annee', 'ilike', self.annee), ('name', "ilike", self.designation_piece)])
            else:
                pieces = self.env['sae.piece'].search([('annee', 'ilike', self.annee)])
        elif self.marque_id and self.modele_id and not self.annee:
            if self.designation_piece:
                pieces = self.env['sae.piece'].search(
                    [('marque_id', '=', self.marque_id.id), ('mdl_id', '=', self.modele_id.id),
                     ('name', "ilike", self.designation_piece)])
            else:
                pieces = self.env['sae.piece'].search(
                    [('marque_id', '=', self.marque_id.id), ('mdl_id', '=', self.modele_id.id)])
        elif self.marque_id and not self.modele_id and self.annee:
            if self.designation_piece:
                pieces = self.env['sae.piece'].search(
                    [('marque_id', '=', self.marque_id.id), ('annee', 'ilike', self.annee),
                     ('name', "ilike", self.designation_piece)])
            else:
                pieces = self.env['sae.piece'].search(
                    [('marque_id', '=', self.marque_id.id), ('annee', 'ilike', self.annee)])
        elif not self.marque_id and self.modele_id and self.annee:
            if self.designation_piece:
                pieces = self.env['sae.piece'].search(
                    [('mdl_id', '=', self.modele_id.id), ('annee', 'ilike', self.annee),
                     ('name', "ilike", self.designation_piece)])

            else:
                pieces = self.env['sae.piece'].search(
                    [('mdl_id', '=', self.modele_id.id), ('annee', 'ilike', self.annee)])
        elif self.marque_id and self.modele_id and self.annee:
            if self.designation_piece:
                pieces = self.env['sae.piece'].search(
                    [('marque_id', '=', self.marque_id.id), ('mdl_id', '=', self.modele_id.id),
                     ('annee', 'ilike', self.annee), ('name', "ilike", self.designation_piece)])
            else:
                pieces = self.env['sae.piece'].search(
                    [('marque_id', '=', self.marque_id.id), ('mdl_id', '=', self.modele_id.id),
                     ('annee', 'ilike', self.annee)])
        elif not self.marque_id and not self.modele_id and not self.annee:
            if self.designation_piece:
                pieces = self.env['sae.piece'].search([('name', "ilike", self.designation_piece)])
            else:
                pieces = self.env['sae.piece'].search([])

        for piece in pieces:
            data.append([0, 0, {
                'piece_id': piece.id,
            }])
        self.sudo().update({"liste_pieces_ids": data})

        return {
            'name': 'Choix de la pièce',
            'view_mode': 'form',
            'view_id': False,
            'res_model': self._name,
            'domain': [],
            'context': dict(self._context, active_ids=self.ids),
            'type': 'ir.actions.act_window',
            'target': 'new',
            'res_id': self.id,
        }

    def confirmer_creation_piece(self):
        data = []
        context = dict(self._context) or {}
        dossier = self.env['sae.expertise.auto'].browse(context.get('active_id', False))
        liste_pieces_ids = self.liste_pieces_ids.search([('is_checked', '=', True)])

        if not liste_pieces_ids:
            raise ("Vous devez aumoins selectionner une ligne")

        for piece in liste_pieces_ids:
            data.append([0, 0, {
                'piece_id': piece.piece_id.id,
                'taxe_id': piece.taxe_id.id,
                'vetuste': piece.vetuste,
                'taux_vet': dossier.taux_vet_glbl,
                'prix_ht': piece.amount_moy,

            }])
            piece.is_checked = False

        if self.num_fourniture == 1:
            dossier.update({"fournitures1_ids": data})
        elif self.num_fourniture == 2:
            dossier.update({"fournitures2_ids": data})
        elif self.num_fourniture == 3:
            dossier.update({"fournitures3_ids": data})
        elif self.num_fourniture == 4:
            dossier.update({"fournitures4_ids": data})
        elif self.num_fourniture == 5:
            dossier.update({"fournitures5_ids": data})
        elif self.num_fourniture == 6:
            dossier.update({"fournitures6_ids": data})

    def vider_modele(self):
        for record in self:
            record.modele_id = None
            return {
                'name': 'Choix de la pièce',
                'view_mode': 'form',
                'view_id': False,
                'res_model': self._name,
                'domain': [],
                'context': dict(self._context, active_ids=self.ids),
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': self.id,
            }
    def vider_annee(self):
        for record in self:
            record.annee = ""
            return {
                'name': 'Choix de la pièce',
                'view_mode': 'form',
                'view_id': False,
                'res_model': self._name,
                'domain': [],
                'context': dict(self._context, active_ids=self.ids),
                'type': 'ir.actions.act_window',
                'target': 'new',
                'res_id': self.id,
            }

    marque_id = fields.Many2one('fleet.vehicle.model.brand', string='Marque', default=_get_default_marque_id)

    modele_id = fields.Many2one('fleet.vehicle.model', string='Modèle', default=_get_default_modele_id,
                                domain="[('brand_id', '=', marque_id)]")

    annee = fields.Char(string='Année MeC', default=_get_default_annee)
    designation_piece = fields.Char(string='Désignation Pièce')

    num_fourniture = fields.Integer(string="Num Fourniture")

    liste_pieces_ids = fields.Many2many(comodel_name='sae.liste.piece', string="Pieces")
