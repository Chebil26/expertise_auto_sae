from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class PassageEnregistreOdsPre(models.TransientModel):
    _name = 'passage.enregistre.pre.wizard'

    dossier_id = fields.Many2one(comodel_name='pre.enregistrement', string="Dossier",
                                 default=lambda self: self.env.context.get('active_id'), readonly=True)

    def _get_default_compagnie(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.compagnie.id

    def _get_default_code_agence(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.code_agence

    def _get_default_date_ods(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.date_ods

    def _get_default_nom_assure(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.compagnie.id

    def _get_default_contact(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.contact

    def _get_default_num_sinistre(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.num_sinistre

    def _get_default_Type_imma(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.Type_imma
    def _get_default_num_ods(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.num_ods

    def _get_default_immatricul(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.immatricul

    def _get_default_num_chas(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.num_chas

    def _get_default_obsrv(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.obsrv

    def _get_default_date_sinistre(self):
        context = dict(self._context) or {}
        pre_id = self.env['pre.enregistrement'].browse(context.get('active_id', False))
        return pre_id.date_sinistre

    # informations Client
    compagnie = fields.Many2one('res.partner', string="Compagnie", default=_get_default_compagnie)
    code_agence = fields.Char("Code Agence", default=_get_default_code_agence)
    date_ods = fields.Date("Date ODS", default=_get_default_date_ods)
    num_ods = fields.Char("N° ODS", default=_get_default_num_ods)
    nom_assure = fields.Char("Nom Assuré", default=_get_default_nom_assure)
    contact = fields.Char("Contact", default=_get_default_contact)
    # informations sinistre
    date_sinistre = fields.Date("Date Sinistre", default=_get_default_date_sinistre)
    num_sinistre = fields.Char("N° Sinistre", default=_get_default_num_sinistre)
    # informations véhicule
    Type_imma = fields.Selection(
        selection=[('alg_5', 'Algérie 05 chiffres'), ('alg_6', 'Algérie 06 chiffres'),
                   ('neuf', 'Algérie véhicule neuf'), ('autre', 'Autre')],
        string='Type Immatricule', default=_get_default_Type_imma)
    immatricul = fields.Char("Immatriculation", default=_get_default_immatricul)
    num_chas = fields.Char("N° chassis (VIN)", default=_get_default_num_chas)
    obsrv = fields.Text("Observation", default=_get_default_obsrv)
    # informations Expertise
    expert_id = fields.Many2one('hr.employee', string="Expert")
    nature_id = fields.Many2one('sae.nature', string="Nature d'expertise")
    lieu_id = fields.Many2one('sae.lieu', string="Lieu de visite")

    def confirmer(self):

        message = "Les champs suivants sont vides :"
        bln1 = False
        bln2 = False
        bln3 = False
        if not self.expert_id:
            message = message + "\n - Expert."
            bln1 = True
        if not self.nature_id:
            message = message + "\n - Nature d'expertise."
            bln2 = True
        if not self.lieu_id:
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
            "num_ods": self.dossier_id.num_ods,
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
