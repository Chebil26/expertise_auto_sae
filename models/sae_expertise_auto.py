from odoo import fields, models, api, _
import json
from odoo.exceptions import UserError


class SaeExpertiseAuto(models.Model):
    _name = 'sae.expertise.auto'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = 'Cette Classe est dédiée pour l expertise auto'
    _order = "create_date desc"

    state = fields.Selection(
        selection=[('cree', 'Enregistré'), ('acpt', 'En cours de traitement'), ('annule', 'Annulé'),
                   ('cloture', 'Cloturé')],
        group_expand='_expand_groups_state', string="Statut")

    # Cette fonction permet d'afficher les colonnes dans la vue Kanban
    @api.model
    def _expand_groups_state(self, states, domain, order):
        return ['cree', 'acpt', 'annule', 'cloture']

    # Cette fonction permet pour l'expert d'accepter un ods
    def accepter(self):
        self.state = 'acpt'
        self.date_debut_traitement = fields.Date.today()
        # Comme le traitement du ods est spécifique pour chaque type de nature de dossier
        # je fais le Return du Form de traitement_expertise_avis si != sinistre
        if self.nature_id.type_nature != 'sinistre':
            view_id = self.env.ref('expertise_auto_sae.sae_traitement_expertise_avis_form_view').id

            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form,tree',
                'res_model': "sae.expertise.auto",
                'target': 'current',
                'res_id': self.id,
                'views': [[view_id, 'form']],
            }
        else:
            # je fais le Return du Form de sae_traitement_expertise si == sinistre
            view_id = self.env.ref('expertise_auto_sae.sae_traitement_expertise_form_view').id
            context = {
                "default_compagnie": self.compagnie.id,
                "default_expert_id": self.expert_id.id,
                "default_nature_id": self.nature_id.id,
                "default_lieu_id": self.lieu_id.id,
                "default_state_expertise": 'photos',
                "default_name": self.name,
                "default_code_agence": self.code_agence.id,
                "default_date_ods": self.date_ods,
                "default_nom_assure": self.nom_assure,
                "default_contact": self.contact,
                "default_date_sinistre": self.date_sinistre,
                "default_num_sinistre": self.num_sinistre,
                "default_Type_imma": self.Type_imma,
                "default_immatricul": self.immatricul,
                "default_num_chas": self.num_chas,
                "default_obsrv": self.obsrv,
            }
            return {
                'type': 'ir.actions.act_window',
                'view_mode': 'form,tree',
                'res_model': "sae.expertise.auto",
                'target': 'current',
                'context': context,
                'res_id': self.id,
                'views': [[view_id, 'form']],
            }

    def annuler(self):

        view_id = self.env.ref(
            'expertise_auto_sae.sae_motif_annulation_form_view'
        ).id
        return {
            'type': 'ir.actions.act_window',
            'name': _("Motif d'Annulation"),
            'res_model': 'sae.motif.annulation',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']]
        }

    def reaffectation(self):
        view_id = self.env.ref(
            'expertise_auto_sae.view_reaffectation_expert_wizard'
        ).id
        return {
            'type': 'ir.actions.act_window',
            'name': _("Réaffectation de l'expert"),
            'res_model': 'reaffectation.expert.wizard',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']]
        }

    def changement_lieu(self):
        view_id = self.env.ref(
            'expertise_auto_sae.view_changer_lieu_wizard'
        ).id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Changement de lieu de visite'),
            'res_model': 'changer.lieu.wizard',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']]
        }

    def traitement_expertise_sinistre(self):
        view_id = self.env.ref(
            'expertise_auto_sae.sae_traitement_expertise_form_view'
        ).id
        context = {
            "default_compagnie": self.compagnie.id,
            "default_expert_id": self.expert_id.id,
            "default_nature_id": self.nature_id.id,
            "default_lieu_id": self.lieu_id.id,
            "default_state_expertise": 'photos',
            "default_name": self.name,
            "default_code_agence": self.code_agence.id,
            "default_date_ods": self.date_ods,
            "default_nom_assure": self.nom_assure,
            "default_contact": self.contact,
            "default_date_sinistre": self.date_sinistre,
            "default_num_sinistre": self.num_sinistre,
            "default_Type_imma": self.Type_imma,
            "default_immatricul": self.immatricul,
            "default_num_chas": self.num_chas,
            "default_obsrv": self.obsrv,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': "sae.expertise.auto",
            'target': 'current',
            'context': context,
            'res_id': self.id,
            'views': [[view_id, 'form']],
        }

    def traitement_expertise_avis(self):
        view_id = self.env.ref(
            'expertise_auto_sae.sae_traitement_expertise_avis_form_view'
        ).id
        context = {
            "default_compagnie": self.compagnie.id,
            "default_expert_id": self.expert_id.id,
            "default_nature_id": self.nature_id.id,
            "default_lieu_id": self.lieu_id.id,
            "default_name": self.name,
            "default_code_agence": self.code_agence.id,
            "default_date_ods": self.date_ods,
            "default_nom_assure": self.nom_assure,
            "default_contact": self.contact,
            "default_obsrv": self.obsrv,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': "sae.expertise.auto",
            'target': 'current',
            'context': context,
            'res_id': self.id,
            'views': [[view_id, 'form']],
        }

    def _get_default_nature_id(self):
        return self.env.ref('expertise_auto_sae.nature_expertise').id

    def _get_default_lieu_id(self):
        return self.env.ref('expertise_auto_sae.lieu_centre').id

    @api.depends('nature_id', 'code_agence', 'num_sinistre')
    def controle_numero_sinistre(self):
        for record in self:
            if record.nature_id and record.code_agence and record.num_sinistre:
                sinistres = self.env['sae.expertise.auto'].search([
                    ('nature_id', '=', record.nature_id.id),
                    ('code_agence', '=', record.code_agence.id),
                    ('num_sinistre', '=', record.num_sinistre),
                ])
                if sinistres:
                    raise UserError("Ce Sinistre est déja Enregistré !")

    @api.depends('date_ods', 'date_sinistre')
    def verification_sur_date_sinistre_et_ods(self):
        for record in self:
            message = "Date d'ODS doit être : \n"
            test1 = False
            test2 = False
            if record.date_ods:
                if record.date_ods > fields.Date.today():
                    message += "- Inférieure ou égale à la date d'aujourd'hui. \n"
                    test1 = True

                if record.date_sinistre:
                    if record.date_ods < record.date_sinistre:
                        message += "- superieur à la date de Sinistre. \n"
                        test2 = True

            if test1 or test2:
                record.write({"date_sinistre": None})
                raise UserError(message)

    # cette fonction permet de recuperer le 3 eme niveau de client (Agence)
    @api.depends('compagnie', 'code_agence')
    def set_domain_for_code_agence(self):
        compagnie = self.env["res.partner"].search([('is_customer', '=', True), ('first_level', '!=', True)])
        for record in self:
            niveau_2 = []
            niveau_1 = self.env["res.partner"].search(
                [('is_customer', '=', True), ('company_group_id', '=', record.compagnie.id)])
            for line1 in compagnie:
                for line2 in niveau_1:
                    if line1.company_group_id.id == line2.id:
                        niveau_2.append(line1.id)
            record.code_agence_domain = json.dumps([('id', 'in', niveau_2)])

    @api.onchange('compagnie')
    def vider_compagnie(self):
        for record in self:
            record.code_agence = None

    def cron_passage_comptabilise(self):
        pv_a_compt = self.env["sae.expertise.auto"].search(
            [('state', '=', 'cloture'), ('date_cloture', '<', fields.Date.today())])
        for pv in pv_a_compt:
            if pv.note_honoraire_ids.state != 'posted':
                pv.note_honoraire_ids.sudo().action_post()

    name = fields.Char("Numéro de dossier")
    # ce champs sera remplie une fois un ods est validé dans un pré enregistrement
    origin = fields.Char("Origine Pre Enregistrement", readonly=1)
    # informations Client
    compagnie = fields.Many2one('res.partner', string="Compagnie", required=True,
                                domain="[('is_customer', '=', True),('first_level', '=', True)]")
    code_agence = fields.Many2one('res.partner', string="Code Agence", required=True)
    date_ods = fields.Date("Date ODS", required=True)
    nom_assure = fields.Char("Nom Assuré", required=True)
    contact = fields.Char("Contact")
    # informations sinistre
    date_sinistre = fields.Date("Date Sinistre")
    num_sinistre = fields.Char("N° Sinistre")
    # informations Expertise
    expert_id = fields.Many2one('hr.employee', string="Expert", required=True)

    nature_id = fields.Many2one('sae.nature', string="Nature d'expertise", default=_get_default_nature_id,
                                required=True)
    type_nature = fields.Selection(related="nature_id.type_nature")
    lieu_id = fields.Many2one('sae.lieu', string="Lieu de visite", default=_get_default_lieu_id, required=True)
    # informations véhicule
    Type_imma = fields.Selection(
        selection=[('alg_5', 'Algérie 05 chiffres'), ('alg_6', 'Algérie 06 chiffres'),
                   ('neuf', 'Algérie véhicule neuf'), ('autre', 'Autre')],
        string='Type Immatricule', default='alg_5')
    immatricul = fields.Char("Immatriculation")
    num_chas = fields.Char("N° chassis (VIN)")
    num_ods = fields.Char("N° ODS", required=True)
    obsrv = fields.Text("Observation")
    obsrv_pv = fields.Text("Observation")
    code_agence_domain = fields.Char(compute="set_domain_for_code_agence")
