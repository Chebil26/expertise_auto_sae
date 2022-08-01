from odoo import fields, models, api, _


class SaeNature(models.Model):
    _name = "sae.nature"

    name = fields.Char(string="Nom", required=True)
    code = fields.Char(string="Code", required=True)
    default = fields.Boolean("Par Default")
    type_nature = fields.Selection(string='Type Nature',
                                   selection=[('sinistre', 'SINISTRE'), ('avis', 'AVIS TECHNIQUE'),
                                              ('visite', 'VISITES DE RISQUE')])


class SaeCarosserie(models.Model):
    _name = "sae.carosserie"
    name = fields.Char(string="Carosserie", required=True)


class SaeType(models.Model):
    _name = "sae.type"
    name = fields.Char(string="Type", required=True)


class SaeEnergie(models.Model):
    _name = "sae.energie"
    name = fields.Char(string="Energie", required=True)


class SaeCouleur(models.Model):
    _name = "sae.couleur"
    name = fields.Char(string="Couleur", required=True)


class SaeGenre(models.Model):
    _name = "sae.genre"
    name = fields.Char(string="Genre", required=True)


class SaeLieu(models.Model):
    _name = "sae.lieu"
    name = fields.Char(string="Nom", required=True)
    code = fields.Char(string="Code", required=True)


class SaeChoc(models.Model):
    _name = "sae.choc"

    name = fields.Char(string="Nom", required=True)
    desc = fields.Char(string="Description")


class BaremeHonoraires(models.Model):
    _name = "bareme.honoraires"

    currency_id = fields.Many2one(comodel_name="res.currency", default=lambda self: self.env.company.currency_id.id)
    borne_inf = fields.Monetary(string='Borne Inferieure', currency_field='currency_id')
    borne_sup = fields.Monetary(string='Borne Superieure', currency_field='currency_id')
    nh_fixe = fields.Monetary(string='Note Honoraire Fixe', currency_field='currency_id')
    sur_a = fields.Float(string="Sur A(%)", digits=(12, 6))
    sur_b = fields.Float(string="Sur B(%)", digits=(12, 6))


class SaeFamilleReparation(models.Model):
    _name = "sae.famille.reparation"

    name = fields.Char(string="Nom", required=True)
    desc = fields.Char(string="Description")


class SaeReparation(models.Model):
    _name = "sae.reparation"
    _rec_name = 'famille_repa'

    famille_repa = fields.Many2one(string="Nom", comodel_name="sae.famille.reparation", required=True)
    amount = fields.Monetary(string='Prix Unitaire', currency_field='currency_id')
    forfait = fields.Boolean(string="Forfait", default=False)
    default = fields.Boolean(string="Défault", default=False)
    type_id = fields.Many2one(comodel_name="sae.type", string="Type véhicule")
    currency_id = fields.Many2one(comodel_name="res.currency")


class SaePiece(models.Model):
    _name = "sae.piece"

    @api.onchange('name', 'code')
    def compute_display_name(self):
        for record in self:
            record.display_name = str(record.code) + " | " + str(record.name)

    # Cette Fonction Permet d'attribuer la tva_globale à chaque pièce crée
    @api.model
    def create(self, values):
        if self.env['ir.config_parameter'].sudo().get_param('expertise_auto_sae.taxe_global_auto'):
            values['taxe_id'] = int(
                self.env['ir.config_parameter'].sudo().get_param('expertise_auto_sae.taxe_global_auto'))
        return super().create(values)

    @api.onchange('marque_id')
    def vider_modele(self):
        for record in self:
            record.mdl_id = None

    name = fields.Char(string="Désignation", required=True)
    code = fields.Char('Référence', required=True)
    display_name = fields.Char("Pièce (Référence | Désignation)", compute="compute_display_name")
    taxe_id = fields.Many2one(comodel_name="account.tax", string="TVA", domain="[('type_tax_use', '=','sale')]")
    vetuste = fields.Boolean(string="Vétusté")
    concessionaire = fields.Boolean(string="Concessionaire")
    annee = fields.Char("Année", limit=4, required=True)
    amount_moy = fields.Monetary(string='P.U Moyen', currency_field='currency_id', required=True)
    amount_min = fields.Monetary(string='P.U Min', currency_field='currency_id', required=True)
    amount_max = fields.Monetary(string='P.U Max', currency_field='currency_id', required=True)
    amount_fact = fields.Monetary(string='P.U Facturé', currency_field='currency_id', required=True)
    company_id = fields.Many2one('res.company', 'Company', required=True, index=True,
                                 default=lambda self: self.env.company)
    currency_id = fields.Many2one(related="company_id.currency_id")
    marque_id = fields.Many2one('fleet.vehicle.model.brand', string="Marque")
    mdl_id = fields.Many2one('fleet.vehicle.model', string="Modele", domain="[('brand_id', '=', marque_id)]")


class AutoConfig(models.TransientModel):
    _inherit = "res.config.settings"

    # Cet héritage permet de rajouter les parametres par defaults du module Auto
    taxe_global_auto = fields.Many2one(comodel_name="account.tax", string="TVA",
                                       domain="[('type_tax_use', '=','sale')]")

    # cette fonction permet la MAJ de la table pièce lors du changement de la TVA
    def set_values(self):
        super(AutoConfig, self).set_values()
        pieces = self.env['sae.piece'].search([])
        param = self.env['ir.config_parameter'].sudo()
        if self.taxe_global_auto:
            param.set_param('expertise_auto_sae.taxe_global_auto', int(self.taxe_global_auto) or False)
            for piece in pieces:
                piece.update({'taxe_id': self.taxe_global_auto.id})

    # Cette fonction permet de récuperer la derniere tva choisie
    @api.model
    def get_values(self):
        res = super(AutoConfig, self).get_values()
        taxe = self.env['ir.config_parameter'].sudo().get_param('expertise_auto_sae.taxe_global_auto',
                                                                self.taxe_global_auto)
        res.update(taxe_global_auto=int(taxe))
        return res
