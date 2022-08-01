from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime
import json


class ChargementPhotos(models.Model):
    _name = 'chargement.photos'

    images = fields.Many2many('ir.attachment', string="Image", required=1)
    note = fields.Text("Note")
    traitement = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")


class ListeChocs(models.Model):
    _name = 'liste.chocs'

    def vider_reparation_fourniture(self, char):
        if char == 'A':
            self.traitement.reparations1_ids = self.traitement.reparations2_ids
            self.traitement.fournitures1_ids = self.traitement.fournitures2_ids
        if char == 'B':
            self.traitement.reparations2_ids = self.traitement.reparations3_ids
            self.traitement.fournitures2_ids = self.traitement.fournitures3_ids
        if char == 'C':
            self.traitement.reparations3_ids = self.traitement.reparations4_ids
            self.traitement.fournitures3_ids = self.traitement.fournitures4_ids
        if char == 'D':
            self.traitement.reparations4_ids = self.traitement.reparations5_ids
            self.traitement.fournitures4_ids = self.traitement.fournitures5_ids
        if char == 'E':
            self.traitement.reparations5_ids = self.traitement.reparations6_ids
            self.traitement.fournitures5_ids = self.traitement.fournitures6_ids

    def vider(self):
        if self.classe == 'F':
            self.name = None
            self.desc = None
            self.traitement.reparations6_ids = None
            self.traitement.fournitures6_ids = None
        else:
            for rec in self.traitement.chocs_ids:
                if rec.classe == chr(ord(self.classe) + 1):
                    self.name = rec.name
                    self.desc = rec.desc
                    rec.name = None
                    rec.desc = None
                    self.vider_reparation_fourniture(self.classe)
                    rec.vider()

    @api.depends("name")
    def compute_obligatoire(self):
        for record in self:
            if record.name:
                record.obligatoire = True
            else:
                record.obligatoire = False

    @api.depends("desc")
    def compute_obligatoire_name(self):
        for record in self:
            if record.desc:
                record.obligatoire_name = True
            else:
                record.obligatoire_name = False

    @api.depends('name', 'traitement.chocs_ids')
    def set_domain_for_chocs_ids(self):
        for record in self:
            choc = []
            for chocs in record.traitement.chocs_ids:
                choc.append(chocs.name.id)
            record.chocs_ids_domain = json.dumps(
                [('id', 'not in', choc)])

    classe = fields.Char("Classe", readonly=1)
    name = fields.Many2one('sae.choc', string='Point du Choc')
    desc = fields.Text("Description du Choc")
    obligatoire = fields.Boolean(string="obligatoire", compute="compute_obligatoire", invisible=1)
    obligatoire_name = fields.Boolean(string="obligatoire", compute="compute_obligatoire_name", invisible=1)
    mode_lecture = fields.Boolean(string="Readonly", invisible=1)
    chocs_ids_domain = fields.Char(compute="set_domain_for_chocs_ids", invisible=1)
    traitement = fields.Many2one('sae.expertise.auto', string="Traitement Expertise", invisible=1)


class ListeReparations(models.Model):
    _name = 'liste.reparations'

    @api.onchange('reparation_id')
    def compute_forfait(self):
        for record in self:
            if record.forfait:
                record.duree = 0
            else:
                record.duree = 1

    @api.depends('reparation_id', 'traitement1')
    def set_domain_for_reparation1_id(self):
        for record in self:
            reparation = []

            for reparations in record.traitement1.reparations1_ids:
                reparation.append(reparations.reparation_id.id)
            record.reparation1_id_domain = json.dumps(
                [('type_id', '=', record.traitement1.type_id.id), ('id', 'not in', reparation)])

    @api.depends('reparation_id', 'traitement2')
    def set_domain_for_reparation2_id(self):
        for record in self:
            reparation = []

            for reparations in record.traitement2.reparations2_ids:
                reparation.append(reparations.reparation_id.id)

            record.reparation2_id_domain = json.dumps(
                [('type_id', '=', record.traitement2.type_id.id), ('id', 'not in', reparation)])

    @api.depends('reparation_id', 'traitement3')
    def set_domain_for_reparation3_id(self):
        reparation = []
        for record in self:
            for reparations in record.traitement3.reparations3_ids:
                reparation.append(reparations.reparation_id.id)
            record.reparation3_id_domain = json.dumps(
                [('type_id', '=', record.traitement3.type_id.id), ('id', 'not in', reparation)])

    @api.depends('reparation_id', 'traitement4')
    def set_domain_for_reparation4_id(self):
        reparation = []
        for record in self:
            for reparations in record.traitement4.reparations4_ids:
                reparation.append(reparations.reparation_id.id)
            record.reparation4_id_domain = json.dumps(
                [('type_id', '=', record.traitement4.type_id.id), ('id', 'not in', reparation)])

    @api.depends('reparation_id', 'traitement5')
    def set_domain_for_reparation5_id(self):
        reparation = []
        for record in self:
            for reparations in record.traitement5.reparations5_ids:
                reparation.append(reparations.reparation_id.id)
            record.reparation5_id_domain = json.dumps(
                [('type_id', '=', record.traitement5.type_id.id), ('id', 'not in', reparation)])

    @api.depends('reparation_id', 'traitement6')
    def set_domain_for_reparation6_id(self):
        reparation = []
        for record in self:
            for reparations in record.traitement6.reparations6_ids:
                reparation.append(reparations.reparation_id.id)
            record.reparation6_id_domain = json.dumps(
                [('type_id', '=', record.traitement6.type_id.id), ('id', ' not in', reparation)])

    @api.onchange('duree', 'reparation_id')
    def compute_amount(self):
        for record in self:
            if record.forfait:
                record.montant = record.reparation_id.amount
            else:
                record.montant = record.reparation_id.amount * record.duree

    reparation_id = fields.Many2one('sae.reparation', string='Nom de la réparation', required=1)
    duree = fields.Float("Durée")
    forfait = fields.Boolean(string="Forfait", related="reparation_id.forfait")
    currency_id = fields.Many2one(comodel_name="res.currency", default=lambda self: self.env.company.currency_id.id)
    montant = fields.Monetary(string='Montant', currency_field='currency_id')
    desc = fields.Text(string="Description")
    reparation1_id_domain = fields.Char(compute="set_domain_for_reparation1_id")
    reparation6_id_domain = fields.Char(compute="set_domain_for_reparation6_id")
    reparation2_id_domain = fields.Char(compute="set_domain_for_reparation2_id")
    reparation3_id_domain = fields.Char(compute="set_domain_for_reparation3_id")
    reparation4_id_domain = fields.Char(compute="set_domain_for_reparation4_id")
    reparation5_id_domain = fields.Char(compute="set_domain_for_reparation5_id")
    traitement1 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")
    traitement2 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")
    traitement3 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")
    traitement4 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")
    traitement5 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")
    traitement6 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")


class ListeFournitures(models.Model):
    _name = 'liste.fournitures'
    _rec_name = "piece_id"

    @api.onchange('piece_id', 'quantite', 'taxe_ids', 'prix_ht')
    def calculer_montant(self):
        for record in self:
            record.montant_tva = 0
            record.montant_ht = record.prix_ht * record.quantite
            record.montant_tva = record.montant_tva + record.montant_ht * (record.taxe_id.amount / 100)
            record.montant_ttc = record.montant_tva + record.montant_ht

    @api.onchange('piece_id')
    def recuperer_taxe_vetuste_prix_ht(self):
        for record in self:
            if record.piece_id:
                record.taxe_id = record.piece_id.taxe_id.id
                record.vetuste = record.piece_id.vetuste
                record.prix_ht = record.piece_id.amount_moy

    @api.onchange('vetuste')
    def calculer_vetuste(self):
        for record in self:
            if not record.vetuste:
                record.taux_vet = 0
            else:
                # je recupere le taux global
                record.taux_vet = record.traitement1.taux_vet_glbl

    def choisir_prix(self):
        view_id = self.env.ref(
            'expertise_auto_sae.view_choix_piece_prix_wizard'
        ).id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Choix de prix par piece'),
            'res_model': 'choix.prix.piece.wizard',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']]
        }

    piece_id = fields.Many2one('sae.piece', string='Pièce (Référence | Désignation)', required=1)
    quantite = fields.Integer("Quantité", default=1)
    taxe_id = fields.Many2one(comodel_name="account.tax", string="TVA", domain="[('type_tax_use', '=','sale')]")
    vetuste = fields.Boolean(string="Vétusté")
    taux_vet = fields.Float("Taux Vétusté")
    facturation = fields.Boolean(string="Facturation")
    currency_id = fields.Many2one(comodel_name="res.currency", default=lambda self: self.env.company.currency_id.id)
    montant_tva = fields.Monetary(string='Montant TVA', currency_field='currency_id', compute="calculer_montant")
    montant_ht = fields.Monetary(string='Montant HT', currency_field='currency_id', compute="calculer_montant",
                                 readonly=1)
    prix_ht = fields.Monetary(string='Prix HT', currency_field='currency_id')
    montant_ttc = fields.Monetary(string='Montant TTC', currency_field='currency_id', compute="calculer_montant")
    type_montant = fields.Selection(string='Type Montant',
                                    selection=[('saisi', 'Montant Saisi'), ('facture', 'Montant Facturé'),
                                               ('a_saisir', 'Montant à Saisir')],
                                    default='saisi')
    ref_fact = fields.Char("Référence Facture")
    date_fact = fields.Date("Date Facture")

    traitement1 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")
    traitement2 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")
    traitement3 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")
    traitement4 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")
    traitement5 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")
    traitement6 = fields.Many2one('sae.expertise.auto', string="Traitement Expertise")


class ResumeChocs(models.Model):
    _name = 'resume.chocs'
    classe = fields.Char("Classe", readonly=1)
    choc = fields.Many2one('sae.choc', string='Choc')
    currency_id = fields.Many2one(comodel_name="res.currency", default=lambda self: self.env.company.currency_id.id)
    montant_tva = fields.Monetary(string='TVA Fournitures', currency_field='currency_id')
    montant_ht = fields.Monetary(string='HT Fournitures', currency_field='currency_id')
    peinture = fields.Monetary(string='Peinture', currency_field='currency_id')
    main_d_oeuvre = fields.Monetary(string="Main d'oeuvre", currency_field='currency_id')
    montant_ttc = fields.Monetary(string='TTC Fournitures', currency_field='currency_id')
    immo = fields.Integer(string="Immobilisation (Jours)")
    nbr_hr = fields.Integer(string="Nombre heures Reparation")
    traitement = fields.Many2one('sae.expertise.auto', string="Traitement Expertise", invisible=1)


class SaeExpertiseAutoPV(models.Model):
    _inherit = 'sae.expertise.auto'

    state_expertise = fields.Selection(selection=[('photos', 'Photos'), ('tiers', 'Details et Tiers'),
                                                  ('vehicule', 'Véhicule'), ('choc', 'Chocs'),
                                                  ('rep', 'Réparations-Réforme'),
                                                  ('fourn', 'Fournitures'), ('resm', 'Résumé')],
                                       group_expand='_expand_groups_state_expertise', default='photos',
                                       string='Etat Expertise')

    reforme_bln = fields.Boolean(string="Réforme", default=False)
    instance_fact = fields.Boolean(string="En instance de Facturation", default=False)
    taux_vet_glbl = fields.Float("Taux Vétusté Global")
    code_lieu = fields.Char(related="lieu_id.code")
    note_honoraire_ids = fields.Many2one('account.move', string="Note d'Honoraire")
    date_cloture = fields.Date("Date Cloture")
    date_reaffectation = fields.Date("Date Réaffectation")
    date_debut_traitement = fields.Date("Date Debut Traitement")
    date_annulation = fields.Date("Date Annulation")

    def write(self, values):
        res = super(SaeExpertiseAutoPV, self).write(values)
        date_lyoum = fields.Date.today()
        if 'reforme_bln' in values or 'chocs_ids' in values or 'reparations1_ids' in values or 'reparations2_ids' in values or 'reparations3_ids' in values or 'reparations4_ids' in values or 'reparations5_ids' in values or 'reparations6_ids' in values or 'fournitures1_ids' in values or 'fournitures2_ids' in values or 'fournitures3_ids' in values or 'fournitures4_ids' in values or 'fournitures5_ids' in values or 'fournitures6_ids' in values or 'taux_vet_glbl' in values or 'montant_pre' in values or 'total_ttc' in values or 'nature_id' in values or 'type_pv' in values or 'photos_ids' in values or 'lieu_id' in values or 'distance' in values or 'nbr_vac' in values or 'nbr_rps' in values or 'nbr_nuit' in values or 'compagnie' in values or 'compagnie.honoraire_fixe' in values:
            if self.state == 'cloture':
                # cas Mise à Jour ODS
                if self.note_honoraire_ids.state == 'draft' and self.date_cloture == date_lyoum:
                    self.note_honoraire_ids.sudo().unlink()
                    self.state = 'acpt'

        return res

    @api.onchange('taux_vet_glbl')
    def compute_taux_vet_glbl(self):
        for rec in self:
            for choc in rec.chocs_ids:
                if choc.classe == 'A' and choc.name:
                    for line in rec.fournitures1_ids:
                        if line.vetuste:
                            line.taux_vet = rec.taux_vet_glbl
                if choc.classe == 'B' and choc.name:
                    for line in rec.fournitures2_ids:
                        if line.vetuste:
                            line.taux_vet = rec.taux_vet_glbl
                if choc.classe == 'C' and choc.name:
                    for line in rec.fournitures3_ids:
                        line.taux_vet = rec.taux_vet_glbl
                if choc.classe == 'D' and choc.name:
                    for line in rec.fournitures4_ids:
                        if line.vetuste:
                            line.taux_vet = rec.taux_vet_glbl
                if choc.classe == 'E' and choc.name:
                    for line in rec.fournitures5_ids:
                        if line.vetuste:
                            line.taux_vet = rec.taux_vet_glbl
                if choc.classe == 'F' and choc.name:
                    for line in rec.fournitures6_ids:
                        if line.vetuste:
                            line.taux_vet = rec.taux_vet_glbl

    def historique_num_chassis(self):

        return self.env["ir.actions.actions"]._for_xml_id(
            "expertise_auto_sae.action_historique_num_chassis_wizard")

    def changement_num_chassis(self):
        view_id = self.env.ref(
            'expertise_auto_sae.view_changer_num_chassis_wizard'
        ).id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Changement de Numéro de Chassis'),
            'res_model': 'changer.num.chassis.wizard',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']]
        }

    def choisir_piece(self):
        view_id = self.env.ref(
            'expertise_auto_sae.view_liste_recherche_prix_wizard'
        ).id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Choix de la pièce'),
            'res_model': 'sae.recherche.piece.wizard',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']]
        }

    def choisir_photos(self):

        view_id = self.env.ref(
            'expertise_auto_sae.view_ajouter_photos_wizard'
        ).id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Choix de Photos'),
            'res_model': 'ajouter.photos.wizard',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']]
        }

    def get_operating_unit_default(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        return user.default_operating_unit_id.id

    @api.model
    def _expand_groups_state_expertise(self, states, domain, order):
        return ['photos', 'tiers', 'vehicule', 'choc', 'rep', 'ref', 'fourn', 'resm']

    @api.depends('chocs_ids', 'reparations1_ids', 'reparations2_ids', 'reparations3_ids', 'reparations4_ids',
                 'reparations5_ids', 'reparations6_ids', 'fournitures1_ids', 'fournitures2_ids', 'fournitures3_ids',
                 'fournitures4_ids', 'fournitures5_ids', 'fournitures6_ids')
    def calcul_resume(self):
        for record in self:
            data = []
            for choc in record.chocs_ids:
                if choc.classe == 'A' and choc.name:
                    montant_tva = 0
                    montant_ht = 0
                    peinture = 0
                    main_d_oeuvre = 0
                    montant_ttc = 0
                    immo = 0
                    for reparation in record.reparations1_ids:
                        if reparation.forfait:
                            peinture += reparation.montant
                        else:
                            main_d_oeuvre += reparation.montant
                        immo += reparation.duree
                    for fourniture in record.fournitures1_ids:
                        montant_tva += fourniture.montant_tva
                        montant_ht += fourniture.montant_ht
                        montant_ttc += fourniture.montant_ttc

                    data.append([0, 0, {
                        'classe': choc.classe,
                        'choc': record.choc_a.id,
                        'montant_tva': montant_tva,
                        'montant_ht': montant_ht,
                        'montant_ttc': montant_ttc,
                        'peinture': peinture,
                        'main_d_oeuvre': main_d_oeuvre,
                        'immo': round(immo / 8),
                        'nbr_hr': immo,

                    }])
                elif choc.classe == 'B' and choc.name:
                    montant_tva = 0
                    montant_ht = 0
                    peinture = 0
                    main_d_oeuvre = 0
                    montant_ttc = 0
                    immo = 0
                    for reparation in record.reparations2_ids:
                        if reparation.forfait:
                            peinture += reparation.montant
                        else:
                            main_d_oeuvre += reparation.montant
                        immo += reparation.duree
                    for fourniture in record.fournitures2_ids:
                        montant_tva += fourniture.montant_tva
                        montant_ht += fourniture.montant_ht
                        montant_ttc += fourniture.montant_ttc

                    data.append([0, 0, {
                        'classe': choc.classe,
                        'choc': record.choc_b.id,
                        'montant_tva': montant_tva,
                        'montant_ht': montant_ht,
                        'montant_ttc': montant_ttc,
                        'peinture': peinture,
                        'main_d_oeuvre': main_d_oeuvre,
                        'immo': round(immo / 8),
                        'nbr_hr': immo,

                    }])

                elif choc.classe == 'C' and choc.name:
                    montant_tva = 0
                    montant_ht = 0
                    peinture = 0
                    main_d_oeuvre = 0
                    montant_ttc = 0
                    immo = 0
                    for reparation in record.reparations3_ids:
                        if reparation.forfait:
                            peinture += reparation.montant
                        else:
                            main_d_oeuvre += reparation.montant
                        immo += reparation.duree
                    for fourniture in record.fournitures3_ids:
                        montant_tva += fourniture.montant_tva
                        montant_ht += fourniture.montant_ht
                        montant_ttc += fourniture.montant_ttc

                    data.append([0, 0, {
                        'classe': choc.classe,
                        'choc': record.choc_c.id,
                        'montant_tva': montant_tva,
                        'montant_ht': montant_ht,
                        'montant_ttc': montant_ttc,
                        'peinture': peinture,
                        'main_d_oeuvre': main_d_oeuvre,
                        'immo': round(immo / 8),
                        'nbr_hr': immo,

                    }])

                elif choc.classe == 'D' and choc.name:
                    montant_tva = 0
                    montant_ht = 0
                    peinture = 0
                    main_d_oeuvre = 0
                    montant_ttc = 0
                    immo = 0
                    for reparation in record.reparations4_ids:
                        if reparation.forfait:
                            peinture += reparation.montant
                        else:
                            main_d_oeuvre += reparation.montant
                        immo += reparation.duree
                    for fourniture in record.fournitures4_ids:
                        montant_tva += fourniture.montant_tva
                        montant_ht += fourniture.montant_ht
                        montant_ttc += fourniture.montant_ttc

                    data.append([0, 0, {
                        'classe': choc.classe,
                        'choc': record.choc_d.id,
                        'montant_tva': montant_tva,
                        'montant_ht': montant_ht,
                        'montant_ttc': montant_ttc,
                        'peinture': peinture,
                        'main_d_oeuvre': main_d_oeuvre,
                        'immo': round(immo / 8),
                        'nbr_hr': immo,

                    }])

                elif choc.classe == 'E' and choc.name:
                    montant_tva = 0
                    montant_ht = 0
                    peinture = 0
                    main_d_oeuvre = 0
                    montant_ttc = 0
                    immo = 0
                    for reparation in record.reparations5_ids:
                        if reparation.forfait:
                            peinture += reparation.montant
                        else:
                            main_d_oeuvre += reparation.montant
                        immo += reparation.duree
                    for fourniture in record.fournitures5_ids:
                        montant_tva += fourniture.montant_tva
                        montant_ht += fourniture.montant_ht
                        montant_ttc += fourniture.montant_ttc

                    data.append([0, 0, {
                        'classe': choc.classe,
                        'choc': record.choc_e.id,
                        'montant_tva': montant_tva,
                        'montant_ht': montant_ht,
                        'montant_ttc': montant_ttc,
                        'peinture': peinture,
                        'main_d_oeuvre': main_d_oeuvre,
                        'immo': round(immo / 8),
                        'nbr_hr': immo,

                    }])

                elif choc.classe == 'F' and choc.name:
                    montant_tva = 0
                    montant_ht = 0
                    peinture = 0
                    main_d_oeuvre = 0
                    montant_ttc = 0
                    immo = 0
                    for reparation in record.reparations6_ids:
                        if reparation.forfait:
                            peinture += reparation.montant
                        else:
                            main_d_oeuvre += reparation.montant
                        immo += reparation.duree
                    for fourniture in record.fournitures6_ids:
                        montant_tva += fourniture.montant_tva
                        montant_ht += fourniture.montant_ht
                        montant_ttc += fourniture.montant_ttc

                    data.append([0, 0, {
                        'classe': choc.classe,
                        'choc': record.choc_f.id,
                        'montant_tva': montant_tva,
                        'montant_ht': montant_ht,
                        'montant_ttc': montant_ttc,
                        'peinture': peinture,
                        'main_d_oeuvre': main_d_oeuvre,
                        'immo': round(immo / 8),
                        'nbr_hr': immo,

                    }])
            return data

    @api.depends('reforme_bln', 'montant_pre', 'total_ttc', 'nature_id', 'type_pv',
                 'photos_ids', 'lieu_id', 'distance', 'nbr_vac', 'nbr_rps',
                 'nbr_nuit', 'compagnie', 'compagnie.honoraire_fixe')
    def calcul_note_honoraire(self):
        for record in self:
            data = []
            if record.nature_id.name != "AVIS TECHNIQUE":
                if record.reforme_bln:
                    amount = record.montant_pre
                else:
                    amount = record.total_ttc
                bareme = self.env["bareme.honoraires"].search([])
                honoraire = self.env["product.product"].search([('default_code', '=', 1)])
                if 0 <= amount <= 10000:
                    data.append([0, 0, {
                        'product_id': honoraire.id,
                        'price_unit': 1000,
                        'tax_ids': honoraire.taxes_id,

                    }])
                elif amount >= 1000001:
                    if record.compagnie.honoraire_fixe:
                        data.append([0, 0, {
                            'product_id': honoraire.id,
                            'price_unit': 7450,
                            'tax_ids': honoraire.taxes_id,

                        }])
                    else:
                        data.append([0, 0, {
                            'product_id': honoraire.id,
                            'price_unit': 1000001 * 0.00656 + (amount - 1000001) * 0.0006,
                            'tax_ids': honoraire.taxes_id,

                        }])
                else:
                    for brm in bareme:
                        if brm.borne_inf <= amount <= brm.borne_sup:
                            if record.compagnie.honoraire_fixe:
                                data.append([0, 0, {
                                    'product_id': honoraire.id,
                                    'price_unit': brm.nh_fixe,
                                    'tax_ids': honoraire.taxes_id,

                                }])
                            else:
                                data.append([0, 0, {
                                    'product_id': honoraire.id,
                                    'price_unit': brm.borne_inf * brm.sur_a + (amount - brm.borne_inf) * brm.sur_b,
                                    'tax_ids': honoraire.taxes_id,

                                }])
            if record.nature_id.name == "CONTRE EXPERTISE":
                contre_expertise = self.env["product.product"].search([('default_code', '=', 2)])
                data.append([0, 0, {
                    'product_id': contre_expertise.id,
                    'price_unit': contre_expertise.lst_price,
                    'quantity': 1,
                    'tax_ids': contre_expertise.taxes_id,

                }])
            if record.nature_id.name == "AVIS TECHNIQUE":
                avis_technique = self.env["product.product"].search([('default_code', '=', 3)])
                data.append([0, 0, {
                    'product_id': avis_technique.id,
                    'price_unit': avis_technique.lst_price,
                    'quantity': 1,
                    'tax_ids': avis_technique.taxes_id,

                }])
            if record.type_pv == "additif":
                hono_additif = self.env["product.product"].search([('default_code', '=', 4)])
                data.append([0, 0, {
                    'product_id': hono_additif.id,
                    'price_unit': hono_additif.lst_price,
                    'quantity': 1,
                    'tax_ids': hono_additif.taxes_id,

                }])
            frais_dossier = self.env["product.product"].search([('default_code', '=', 5)])
            data.append([0, 0, {
                'product_id': frais_dossier.id,
                'price_unit': frais_dossier.lst_price,
                'quantity': 1,
                'tax_ids': frais_dossier.taxes_id,

            }])

            photos = self.env["product.product"].search([('default_code', '=', 6)])
            nbr_photos = 0
            for photo in record.photos_ids:
                nbr_photos += len(photo.images)
            data.append([0, 0, {
                'product_id': photos.id,
                'price_unit': photos.lst_price,
                'quantity': nbr_photos,
                'tax_ids': photos.taxes_id,

            }])
            if record.lieu_id.code == "H" or record.lieu_id.code == "V":
                frais_deplacement = self.env["product.product"].search([('default_code', '=', 7)])
                data.append([0, 0, {
                    'product_id': frais_deplacement.id,
                    'price_unit': frais_deplacement.lst_price,
                    'quantity': record.distance,
                    'tax_ids': frais_deplacement.taxes_id,

                }])
            if record.lieu_id.code == "V":
                vacation = self.env["product.product"].search([('default_code', '=', 8)])
                data.append([0, 0, {
                    'product_id': vacation.id,
                    'price_unit': vacation.lst_price,
                    'quantity': record.nbr_vac,
                    'tax_ids': vacation.taxes_id,

                }])
            if record.lieu_id.code == "H" or record.lieu_id.code == "V":
                repas = self.env["product.product"].search([('default_code', '=', 9)])
                data.append([0, 0, {
                    'product_id': repas.id,
                    'price_unit': repas.lst_price,
                    'quantity': record.nbr_rps,
                    'tax_ids': repas.taxes_id,

                }])
            if record.lieu_id.code == "H" or record.lieu_id.code == "V":
                sejour = self.env["product.product"].search([('default_code', '=', 10)])
                data.append([0, 0, {
                    'product_id': sejour.id,
                    'price_unit': sejour.lst_price,
                    'quantity': record.nbr_nuit,
                    'tax_ids': sejour.taxes_id,

                }])
            if record.lieu_id.code == "H":
                sejour = self.env["product.product"].search([('default_code', '=', 13)])
                data.append([0, 0, {
                    'product_id': sejour.id,
                    'price_unit': sejour.lst_price,
                    'quantity': record.distance,
                    'tax_ids': sejour.taxes_id,
                }])
            return data

    def suivant(self):
        for record in self:
            if record.state_expertise == 'photos':
                record.state_expertise = 'tiers'
            elif record.state_expertise == 'tiers':
                record.state_expertise = 'vehicule'
            elif record.state_expertise == 'vehicule':
                cas_1 = False
                cas_2 = False
                cas_3 = False
                message = "Vous ne pouvez pas aller à l'étape suivante car :"
                if not record.num_chas_pv or not record.mrqe_id or not record.mdle_id or not record.genre_id or not record.type_id or not record.enrg_id or not record.carosserie_id or not record.couleur_id or record.puissance == -1:
                    message += "\n -Informations Identification /Caractéristiques  véhicule manquantes"
                    cas_1 = True
                if record.num_chass_diff:
                    message += "\n -Numéro de VIN est Incorrecte !!"
                    cas_2 = True
                if not record.num_chas_pv:
                    message += "\n -Numéro de VIN est Vide !!"
                    cas_3 = True
                if cas_1 or cas_2 or cas_3:
                    raise UserError(message)
                record.state_expertise = 'choc'
            elif record.state_expertise == 'choc':
                if not record.nbr_choc:
                    raise UserError("Vous devez saisir au moins un choc")
                record.state_expertise = 'rep'
            elif record.reforme_bln:
                record.state_expertise = 'resm'
            elif not record.reforme_bln:
                if record.state_expertise == 'fourn':
                    record.state_expertise = 'resm'
                    record.write({'resume_chocs_ids': self.calcul_resume()})
                    record.write({'taux_vet': self.compute_taux_vet()})
                elif record.state_expertise == 'rep':
                    record.state_expertise = 'fourn'
                if record.type_pv == 'simple':
                    record.obsrv_pv = "AUCUN ADDITIF NE SERA ETABLI AU DELA DE 90 JOURS"

    def precedent(self):
        for record in self:
            if record.state_expertise == 'rep':
                record.state_expertise = 'choc'
            elif record.state_expertise == 'choc':
                record.state_expertise = 'vehicule'
            elif record.state_expertise == 'vehicule':
                record.state_expertise = 'tiers'
            elif record.state_expertise == 'tiers':
                record.state_expertise = 'photos'
            elif record.reforme_bln:
                if record.state_expertise == 'resm':
                    record.state_expertise = 'rep'
            elif not record.reforme_bln:
                if record.state_expertise == 'resm':
                    record.state_expertise = 'fourn'
                    record.write({'resume_chocs_ids': False})
                elif record.state_expertise == 'fourn':
                    record.state_expertise = 'rep'

    def cloture(self):
        self.date_cloture = fields.Date.today()
        if self.instance_fact:
            raise UserError(_('Vous ne pouvez pas Cloturer un PV en Instance de Facturation'))
        data = self.calcul_note_honoraire()
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'narration': self.obsrv_pv,
            'dossier_ods': self.id,
            'currency_id': self.currency_id.id,
            'compagnie': self.compagnie.id,
            'user_id': self.env.user.id,
            'invoice_user_id': self.env.user.id,
            'partner_id': self.code_agence.id,
            'operating_unit_id': self.operating_unit.id,
            'type_activite_id': self.env.ref("sae_borderau.sae_automobile_activite").id,
            'fiscal_position_id': self.code_agence.property_account_position_id.id,
            'invoice_origin': self.name,
            'invoice_line_ids': data,
            'company_id': self.env.company.id,
            'state': 'draft',
        })
        self.note_honoraire_ids = invoice.id
        action = self.env.ref('expertise_auto_sae.pv_expert_auto_report2').report_action(self)
        action.update({'close_on_report_download': True})
        self.state = 'cloture'
        return action

    def annule_remplace_pv(self):
        view_id = self.env.ref(
            'expertise_auto_sae.view_annule_remplace_pv_wizard'
        ).id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Changement de Numéro de Chassis'),
            'res_model': 'annule.remplace.pv.wizard',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']]
        }

    def creer_additif(self):
        dossier_additif = {
            "compagnie": self.compagnie.id,
            "expert_id": self.expert_id.id,
            "nature_id": self.nature_id.id,
            "lieu_id": self.lieu_id.id,
            "state": 'acpt',
            "state_expertise": 'photos',
            "code_agence": self.code_agence.id,
            "etat_vehi": self.etat_vehi,
            "num_ods": self.num_ods,
            "val_vet": self.val_vet,
            "num_chass_diff": self.num_chass_diff,
            "histo_num_chassis": self.histo_num_chassis,
            "taux_vet": self.taux_vet,
            "total_ht": self.total_ht,
            "val_venale_syn": self.val_venale_syn,
            "an_mec": self.an_mec,
            "type_ref": self.type_ref,
            "desc_ref": self.desc_ref,
            "val_venale": self.val_venale,
            "val_epave": self.val_epave,
            "nbr_tiers": self.nbr_tiers,
            "nom_tiers": self.nom_tiers,
            "num_plc": self.num_plc,
            "lettre_bln": self.lettre_bln,
            "agence_tiers": self.agence_tiers,
            "compagnie_tiers": self.compagnie_tiers.id,
            "kilometrage": self.kilometrage,
            "mrqe_id": self.mrqe_id.id,
            "mdle_id": self.mdle_id.id,
            "genre_id": self.genre_id.id,
            "type_id": self.type_id.id,
            "enrg_id": self.enrg_id.id,
            "couleur_id": self.couleur_id.id,
            "carosserie_id": self.carosserie_id.id,
            "puissance": self.puissance,
            "commune_id": self.commune_id.id,
            "operating_unit": self.operating_unit.id,
            "wilaya": self.wilaya.id,
            "distance": self.distance,
            "nbr_nuit": self.nbr_nuit,
            "nbr_rps": self.nbr_rps,
            "nbr_vac": self.nbr_vac,
            "nom_assure": self.nom_assure,
            "contact": self.contact,
            "date_sinistre": self.date_sinistre,
            "num_sinistre": self.num_sinistre,
            "Type_imma": self.Type_imma,
            "immatricul": self.immatricul,
            "num_chas": self.num_chas,
            "obsrv": self.obsrv,
            "date_ods": self.date_ods,
            "num_chas_pv": self.num_chas_pv,
            "type_pv": "additif",
            "origine_additif": self.id,
        }
        auto = self.env["sae.expertise.auto"].create(dossier_additif)

        view_id = self.env.ref('expertise_auto_sae.sae_traitement_expertise_form_view').id

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form,tree',
            'res_model': "sae.expertise.auto",
            'target': 'current',
            'context': dossier_additif,
            'res_id': auto['id'],
            'views': [[view_id, 'form']],
        }

    @api.onchange('photos_ids', 'lettre_bln')
    def compute_photos(self):
        for record in self:
            if not record.photos_ids and record.lettre_bln:
                record.photos_null = True
            if not record.photos_ids and not record.lettre_bln:
                record.photos_lettre_null = True
            if record.photos_ids and not record.lettre_bln:
                record.lettre_null = True
            if record.photos_ids and record.lettre_bln:
                record.photos_null = False
                record.photos_lettre_null = False
                record.lettre_null = False

    @api.depends('chocs_ids')
    def nbr_choc_comp(self):
        for rec in self:
            if rec.chocs_ids:
                rec.nbr_choc = len(rec.chocs_ids.name)
                for choc in rec.chocs_ids:
                    if choc.classe == 'A' and choc.name:
                        rec.choc_a = choc.name
                        rec.chocs_ids.search([('traitement', '=', rec.id), ('classe', '=', 'B')]).mode_lecture = False
                    elif choc.classe == 'B' and choc.name:
                        rec.choc_b = choc.name
                        rec.chocs_ids.search([('traitement', '=', rec.id), ('classe', '=', 'C')]).mode_lecture = False
                    elif choc.classe == 'C' and choc.name:
                        rec.choc_c = choc.name
                        rec.chocs_ids.search([('traitement', '=', rec.id), ('classe', '=', 'D')]).mode_lecture = False
                    elif choc.classe == 'D' and choc.name:
                        rec.choc_d = choc.name
                        rec.chocs_ids.search([('traitement', '=', rec.id), ('classe', '=', 'E')]).mode_lecture = False
                    elif choc.classe == 'E' and choc.name:
                        rec.choc_e = choc.name
                        rec.chocs_ids.search([('traitement', '=', rec.id), ('classe', '=', 'F')]).mode_lecture = False
                    elif choc.classe == 'F' and choc.name:
                        rec.choc_f = choc.name
            else:
                rec.nbr_choc = 0

    @api.onchange('chocs_ids')
    def affectation_reparation(self):
        for record in self:
            data = []
            raparations = self.env["sae.reparation"].search(
                [('default', '=', True), ('type_id', '=', record.type_id.id)])
            for repa in raparations:
                if repa.forfait:
                    duree = 0
                else:
                    duree = 1
                data.append([0, 0, {
                    'reparation_id': repa.id,
                    'duree': duree,
                    'montant': repa.amount,
                }])
            for choc in record.chocs_ids:
                if choc.classe == 'A' and choc.name:
                    if not record.reparations1_ids:
                        record.update({'reparations1_ids': data})
                elif choc.classe == 'B' and choc.name:
                    if not record.reparations2_ids:
                        record.update({'reparations2_ids': data})
                elif choc.classe == 'C' and choc.name:
                    if not record.reparations3_ids:
                        record.update({'reparations3_ids': data})
                elif choc.classe == 'D' and choc.name:
                    if not record.reparations4_ids:
                        record.update({'reparations4_ids': data})
                elif choc.classe == 'E' and choc.name:
                    if not record.reparations5_ids:
                        record.update({'reparations5_ids': data})
                elif choc.classe == 'F' and choc.name:
                    if not record.reparations6_ids:
                        record.update({'reparations6_ids': data})

    def revenir_photo(self):
        for record in self:
            record.state_expertise = "photos"
            record.update({'resume_chocs_ids': False})

    @api.model
    def createe(self, values):
        lieu_id = values.get("lieu_id", False)
        lieu = self.env["sae.lieu"].browse(lieu_id)
        type_pv = values.get("type_pv", False)
        operating_unit = values.get("operating_unit", False)
        if type_pv != 'additif':
            if lieu.code == 'C':
                code = str(operating_unit) + "_seq_centre"
            elif lieu.code == 'H':
                code = str(operating_unit) + "_seq_hors_centre"

            elif lieu.code == 'V':
                code = str(operating_unit) + "_seq_vacation"

            elif lieu.code == 'D':
                code = str(operating_unit) + "_seq_ead"

            values['name'] = self.env['ir.sequence'].next_by_code(code)
        else:
            origine_id = values.get("origine_additif", False)
            origine = self.env["sae.expertise.auto"].browse(origine_id)
            values['name'] = origine.name
        values["state"] = 'cree'

        values["state_expertise"] = 'photos'
        data = [[0, 0, {
            'classe': 'A',
            'mode_lecture': False
        }], [0, 0, {
            'classe': 'B',
            'mode_lecture': True
        }], [0, 0, {
            'classe': 'C',
            'mode_lecture': True
        }], [0, 0, {
            'classe': 'D',
            'mode_lecture': True
        }], [0, 0, {
            'classe': 'E',
            'mode_lecture': True
        }], [0, 0, {
            'classe': 'F',
            'mode_lecture': True
        }]]
        values.update({'chocs_ids': data})
        return super().create(values)

    @api.depends('operating_unit')
    def set_domain_for_operating_unit(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        units = []
        for unit in user.operating_unit_ids:
            units.append(unit.id)
        self.operating_unit_domain = json.dumps([('id', 'in', units)])

    @api.onchange('val_venale', 'val_epave')
    def compute_montant_pre(self):
        for record in self:
            record.montant_pre = record.val_venale - record.val_epave

    @api.depends('num_chas_pv')
    def mettre_a_jour_num_chassis(self):
        for record in self:
            if record.num_chas_pv != record.num_chas:
                record.num_chass_diff = True
            else:
                record.num_chass_diff = False

    @api.depends('chocs_ids', 'fournitures1_ids', 'fournitures2_ids', 'fournitures3_ids',
                 'fournitures4_ids', 'fournitures5_ids', 'fournitures6_ids', 'taux_vet_glbl')
    def compute_taux_vet(self):
        for record in self:
            taux_vet = 0
            for choc in record.chocs_ids:
                if choc.classe == 'A' and choc.name:
                    for fourniture in record.fournitures1_ids:
                        taux_vet += fourniture.taux_vet * fourniture.quantite / len(record.fournitures1_ids)
                elif choc.classe == 'B' and choc.name:
                    for fourniture in record.fournitures2_ids:
                        taux_vet += fourniture.taux_vet * fourniture.quantite / len(record.fournitures2_ids)
                elif choc.classe == 'C' and choc.name:
                    for fourniture in record.fournitures3_ids:
                        taux_vet += fourniture.taux_vet * fourniture.quantite / len(record.fournitures3_ids)
                elif choc.classe == 'D' and choc.name:
                    for fourniture in record.fournitures4_ids:
                        taux_vet += fourniture.taux_vet * fourniture.quantite / len(record.fournitures4_ids)
                elif choc.classe == 'E' and choc.name:
                    for fourniture in record.fournitures5_ids:
                        taux_vet += fourniture.taux_vet * fourniture.quantite / len(record.fournitures5_ids)
                elif choc.classe == 'F' and choc.name:
                    for fourniture in record.fournitures6_ids:
                        if len(record.fournitures1_ids):
                            taux_vet += fourniture.taux_vet * fourniture.quantite / len(record.fournitures6_ids)
            return taux_vet / record.nbr_choc

    @api.onchange('taux_vet')
    def compute_val_vet(self):
        for record in self:
            record.val_vet = record.total_four_ttc * record.taux_vet / 100

    @api.onchange('mrqe_id')
    def vider_modele(self):
        for record in self:
            record.mdle_id = None

    @api.onchange('resume_chocs_ids')
    def compute_totaux(self):
        for record in self:
            record.total_tva = 0
            record.total_ht = 0
            record.total_peinture = 0
            record.total_main_d_oeuvre = 0
            record.total_four_ttc = 0
            record.total_ttc = 0
            record.total_immo = 0
            record.total_heures = 0
            for choc in record.resume_chocs_ids:
                record.total_tva += choc.montant_tva
                record.total_ht += choc.montant_ht
                record.total_four_ttc += choc.montant_ttc
                record.total_peinture += choc.peinture
                record.total_main_d_oeuvre += choc.main_d_oeuvre
                record.total_immo += choc.immo
                record.total_heures += choc.nbr_hr
            record.total_ttc += record.total_four_ttc + record.total_main_d_oeuvre + record.total_peinture
            record.total_ttc_text = record.currency_id.with_context({}).amount_to_text(record.total_ttc)

    origine_additif = fields.Many2one(string="Dossier ODS", comodel_name="sae.expertise.auto")
    operating_unit_domain = fields.Char(compute="set_domain_for_operating_unit")
    operating_unit = fields.Many2one(string="Centre", comodel_name="operating.unit", default=get_operating_unit_default,
                                     required=True)
    photos_null = fields.Boolean(default=False)
    photos_lettre_null = fields.Boolean(default=False)
    lettre_null = fields.Boolean(default=False)
    annule_remplace = fields.Boolean(default=False)
    nbr_choc = fields.Integer(compute="nbr_choc_comp")
    choc_a = fields.Many2one('sae.choc', readonly=1)
    choc_b = fields.Many2one('sae.choc', readonly=1)
    choc_c = fields.Many2one('sae.choc', readonly=1)
    choc_d = fields.Many2one('sae.choc', readonly=1)
    choc_e = fields.Many2one('sae.choc', readonly=1)
    choc_f = fields.Many2one('sae.choc', readonly=1)

    # chargement photos
    photos_ids = fields.One2many('chargement.photos', 'traitement', string='Photos', copy=True)
    # Descriptions des réparations

    reparations1_ids = fields.One2many('liste.reparations', 'traitement1')
    reparations2_ids = fields.One2many('liste.reparations', 'traitement2')
    reparations3_ids = fields.One2many('liste.reparations', 'traitement3')
    reparations4_ids = fields.One2many('liste.reparations', 'traitement4')
    reparations5_ids = fields.One2many('liste.reparations', 'traitement5')
    reparations6_ids = fields.One2many('liste.reparations', 'traitement6')

    # Descriptions des Chocs
    chocs_ids = fields.One2many('liste.chocs', 'traitement')
    # Descriptions des Fournitures
    fournitures1_ids = fields.One2many('liste.fournitures', 'traitement1')
    fournitures2_ids = fields.One2many('liste.fournitures', 'traitement2')
    fournitures3_ids = fields.One2many('liste.fournitures', 'traitement3')
    fournitures4_ids = fields.One2many('liste.fournitures', 'traitement4')
    fournitures5_ids = fields.One2many('liste.fournitures', 'traitement5')
    fournitures6_ids = fields.One2many('liste.fournitures', 'traitement6')

    # informations Expertise
    adrs_vis = fields.Char("Rue")
    commune_id = fields.Many2one(comodel_name='res.commune', string='Commune', domain="[('state_id.id', '=', wilaya)]")
    company_id = fields.Many2one(comodel_name='res.company', string='Company', index=True,
                                 default=lambda self: self.env.user.company_id.id)
    wilaya = fields.Many2one("res.country.state", "Wilaya", domain="[('country_id.name', '=', 'Algérie')]")
    distance = fields.Integer("Distance (KLM)")
    nbr_nuit = fields.Integer("Nombre de Nuitées")
    nbr_rps = fields.Integer("Nombre de Repas")
    nbr_vac = fields.Integer("Nombre de Vacations")

    # informations véhicule
    num_chas_pv = fields.Char("N° chassis (VIN)")
    an_mec = fields.Integer("Année de MeC")
    kilometrage = fields.Float("Kilométrage")
    mrqe_id = fields.Many2one('fleet.vehicle.model.brand', string="Marque")
    mdle_id = fields.Many2one('fleet.vehicle.model', string="Modèle", domain="[('brand_id', '=', mrqe_id)]")
    genre_id = fields.Many2one('sae.genre', string="Genre")
    type_id = fields.Many2one('sae.type', string="Type")
    enrg_id = fields.Many2one('sae.energie', string="Energie")
    couleur_id = fields.Many2one('sae.couleur', string="Couleur")
    carosserie_id = fields.Many2one('sae.carosserie', string="Carosserie")
    puissance = fields.Integer("Puissance(CV)", default=-1)

    # informations tiers
    nbr_tiers = fields.Integer("Nombre des Tiers")
    nom_tiers = fields.Char('Nom et Prénom')
    num_plc = fields.Char('Numéro Police')
    lettre_bln = fields.Boolean(string="Envoyer la Lettre ?", default=False)
    text_lettre = fields.Html("Lettre Invitation")
    compagnie_tiers = fields.Many2one('res.partner', string="Compagnie",
                                      domain="[('is_customer', '=', True),('first_level', '=', True)]")
    agence_tiers = fields.Char('Agence')
    type_pv = fields.Selection(
        selection=[('simple', 'Simple'), ('additif', 'Additif')],
        string='Type Pv', default='simple', readonly=1)
    # Réforme
    type_ref = fields.Selection(
        selection=[('Economique', 'Réforme Economique'), ('Technique', 'Réforme Technique'), ('Vol', 'Vol Total'),
                   ('Incendie', 'Incendie')],
        string='Type Réforme')
    desc_ref = fields.Text(string="Description de la Réforme")
    val_venale = fields.Monetary(string='Valeur Vénale', currency_field='currency_id')
    val_epave = fields.Monetary(string='Valeur Epave', currency_field='currency_id')
    montant_pre = fields.Monetary(string='Montant Préjudice', currency_field='currency_id',
                                  compute='compute_montant_pre')
    currency_id = fields.Many2one(comodel_name="res.currency", default=lambda self: self.env.company.currency_id.id)

    # synthese non reforme
    # infos supplémentaires
    val_venale_syn = fields.Monetary(string='Valeur Vénale', currency_field='currency_id')
    val_vet = fields.Monetary(string='Valeur Vétusté', currency_field='currency_id', compute="compute_val_vet")
    etat_vehi = fields.Selection(
        selection=[('Bon', 'Bon'), ('Moyen', 'Moyen'), ('Dégradé', 'Dégradé')],
        string='Etat Véhicule')
    taux_vet = fields.Float("Taux Vétusté (%)", readonly=1)

    # Résumé des Chocs
    resume_chocs_ids = fields.One2many('resume.chocs', 'traitement')

    # Résumé Global
    total_ht = fields.Monetary(string='HT Fournitures', currency_field='currency_id', compute="compute_totaux")
    total_peinture = fields.Monetary(string='Montant Peinture', currency_field='currency_id', compute="compute_totaux")
    total_main_d_oeuvre = fields.Monetary(string="Montant Main d'oeuvre", currency_field='currency_id',
                                          compute="compute_totaux")
    total_four_ttc = fields.Monetary(currency_field='currency_id', compute="compute_totaux")
    total_ttc = fields.Monetary(string='Montant Total TTC', currency_field='currency_id', compute="compute_totaux")
    total_tva = fields.Monetary(string='TVA Fournitures', currency_field='currency_id', compute="compute_totaux")
    total_immo = fields.Integer(string="Immobilisation (Jours)", default=0)
    total_heures = fields.Integer(compute="compute_totaux", default=0)
    total_ttc_text = fields.Char(string='Montant Total en Lettres', compute="compute_totaux")

    num_chass_diff = fields.Boolean(compute="mettre_a_jour_num_chassis")
    histo_num_chassis = fields.Boolean(default=False)
