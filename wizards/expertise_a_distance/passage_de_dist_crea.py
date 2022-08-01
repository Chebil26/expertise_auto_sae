from odoo import models, fields, api
from odoo.exceptions import UserError


class PassageEnregistreOdsPre(models.TransientModel):
    _name = 'passage.enregistre.pre.wizard'

    dossier_id = fields.Many2one(comodel_name='pre.enregistrement', string="Dossier",
                                 default=lambda self: self.env.context.get('active_id'), readonly=True)
    # informations Expertise
    expert_id = fields.Many2one('hr.employee', string="Expert")
    nature_id = fields.Many2one('sae.nature', string="Nature d'expertise")
    lieu_id = fields.Many2one('sae.lieu', string="Lieu de visite")

    def confirmer(self):
        message="Les champs suivants sont vides :"
        bln1 = False
        bln2 = False
        bln3 = False
        if not self.expert_id :
            message = message + "\n - Expert."
            bln1 = True
        if not self.nature_id :
            message = message + "\n - Nature d'expertise."
            bln2 = True
        if not self.lieu_id :
            message = message + "\n - Lieu de visite."
            bln3 = True
        if bln1 or bln2 or bln3:
            raise UserError(message)

        self.dossier_id.state = 'val'
        if self.dossier_id.date_ods < self.dossier_id.date_sinistre:
            raise UserError("Date d'ODS doit être inférieur à la date de Sinistre")
        pre_enregistrement = {
            "compagnie": self.dossier_id.compagnie.id,
            "origin": self.dossier_id.name,
            "state": 'cree',
            "code_agence": self.dossier_id.code_agence,
            "date_ods": self.dossier_id.date_ods,
            "nom_assure": self.dossier_id.nom_assure,
            "contact": self.dossier_id.contact,
            "date_sinistre": self.dossier_id.date_sinistre,
            "num_sinistre": self.dossier_id.num_sinistre,
            "Type_imma": self.dossier_id.Type_imma,
            "immatricul": self.dossier_id.immatricul,
            "num_chas": self.dossier_id.num_chas,
            "obsrv": self.dossier_id.obsrv,
            "expert_id": self.expert_id.id,
            "nature_id": self.nature_id.id,
            "lieu_id": self.lieu_id.id,
        }
        auto = self.env["sae.expertise.auto"].create(pre_enregistrement)

    def annuler(self):
        self.dossier_id.write({'state': 'cree'})
        return {"type": "ir.actions.act_window_close"}
