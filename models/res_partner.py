from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = "res.users"

    # Ajouter l'information est un Expert pour faire un domaine dans les modules d'expertise pour le champs expert_id
    is_expert = fields.Boolean(string="est un Expert", default=False)


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Informations Liées à l'expertise Auto
    honoraire_fixe = fields.Boolean(string="Honoraires Fixes", default=False)
    val_ven = fields.Boolean(string="Valeur Vénale", default=False)
    ltr_inv = fields.Boolean(string="Lettre Invitation", default=False)
    first_level = fields.Boolean(string="1 er Niveau", default=True, store=True)

    # Cette Fonction permet de differencier entre les compagnies de premier niveau ou pas (si on lui attribue une entreprise parente ou pas)
    @api.onchange('company_group_id')
    def compute_first_level(self):
        for record in self:
            if record.company_group_id:
                record.first_level = False
            else:
                record.first_level = True
