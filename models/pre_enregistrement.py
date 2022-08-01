from odoo import fields, models, api, _
from datetime import datetime, timedelta
from odoo.exceptions import UserError


class PresEnregistrement(models.Model):
    _name = 'pre.enregistrement'
    _description = 'Cette Classe décrit un Pre Enregistrement d un dossier SAE'
    state = fields.Selection(
        selection=[('cree', 'Enregistré'), ('anuule', 'Annulé'), ('val', 'Validé')],
        group_expand='_expand_groups_state',string="Statut")

    @api.model
    def _expand_groups_state(self, states, domain, order):
        return ['cree', 'anuule', 'val']

    def validate(self):
            view_id = self.env.ref(
                'expertise_auto_sae.view_passage_enregistre_wizard'
            ).id
            return {
                'type': 'ir.actions.act_window',
                'name': _("Réaffectation de l'expert"),
                'res_model': 'passage.enregistre.pre.wizard',
                'target': 'new',
                'view_mode': 'form',
                'views': [[view_id, 'form']]
            }



    @api.model
    def create(self, vals):
        new_seq = self.env['ir.sequence'].next_by_code('pre_ref')
        vals["name"] = new_seq
        vals["state"] = 'cree'
        if vals["date_ods"] < vals["date_sinistre"]:
            raise UserError("Date d'ODS doit être superieur à la date de Sinistre")
        return super().create(vals)

    name = fields.Char("N° Dossier", required=True)
    bln = fields.Boolean(compute="passage_archive", default=False)
    duree = fields.Integer("Durée", default=30)

    def passage_archive(self):
        for record in self:
            current_date = datetime.now().date()
            if timedelta(days=record.duree) + record.date_ods < current_date:
                record.state = 'anuule'
            record.bln = True

    # informations Client
    compagnie = fields.Many2one('res.partner', string="Compagnie")
    code_agence = fields.Char("Code Agence")
    date_ods = fields.Date("Date ODS", default=datetime.today())
    num_ods = fields.Char("N° ODS")
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