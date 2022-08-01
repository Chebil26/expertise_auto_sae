from odoo import fields, models, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class ExpertiseADistance(models.Model):
    _name = 'sae.distance'
    _description = 'Cette Classe décrit une Expertise A Distance de la SAE'
    state = fields.Selection(
        selection=[('cree', 'Enregistré'), ('anuule', 'Annulé'), ('val', 'Validé')],
        group_expand='_expand_groups_state', string="Statut")

    @api.model
    def _expand_groups_state(self, states, domain, order):
        return ['cree', 'anuule', 'val']

    @api.model
    def create(self, vals):
        new_seq = self.env['ir.sequence'].next_by_code('dist_ref')
        vals["name"] = new_seq
        vals["state"] = 'cree'
        if vals["date_ods"] < vals["date_sinistre"]:
            raise UserError("Date d'ODS doit être superieur à la date de Sinistre")
        return super().create(vals)

    name = fields.Char("N° Dossier", required=True)
    # informations Client
    compagnie = fields.Many2one('res.partner', string="Compagnie")
    code_agence = fields.Char("Code Agence")
    date_ods = fields.Date("Date ODS", default=datetime.today())
    nom_assure = fields.Char("Nom Assuré")
    contact = fields.Char("Contact")
    # informations sinistre
    date_sinistre = fields.Date("Date Sinistre", default=datetime.today())
    num_sinistre = fields.Char("N° Sinistre")
    # informations véhicule
    Type_imma = fields.Selection(
        selection=[('alg_5', 'Algérie 05 chiffres'), ('alg_6', 'Algérie 06 chiffres'),
                   ('neuf', 'Algérie véhicule neuf'), ('autre', 'Autre')],
        string='Type Immatricule')
    immatricul = fields.Char("Immatriculation")
    num_chas = fields.Char("N° chassis (VIN)")
    obsrv = fields.Text("Observation")


    qrtest = fields.Text("qrtext")
    qrf = fields.Binary("qrcode")

    def validate(self):
        for record in self:
            record.state = 'val'
            if record.date_ods < record.date_sinistre:
                raise UserError("Date d'ODS doit être superieur à la date de Sinistre")
            pre_enregistrement = {
                "compagnie": record.compagnie.id,
                "origin": record.name,
                "state": 'cree',
                "code_agence": record.code_agence,
                "date_ods": record.date_ods,
                "nom_assure": record.nom_assure,
                "contact": record.contact,
                "date_sinistre": record.date_sinistre,
                "num_sinistre": record.num_sinistre,
                "Type_imma": record.Type_imma,
                "immatricul": record.immatricul,
                "num_chas": record.num_chas,
                "obsrv": record.obsrv,
            }
            auto = self.env["sae.expertise.auto"].create(pre_enregistrement)
