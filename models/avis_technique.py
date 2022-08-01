from odoo import fields, models, api, _


class SaeExpertiseAuto(models.Model):
    _inherit = 'sae.expertise.auto'

    # cette partie est dediée à l'expertise != Sinistre

    file_pv = fields.Binary("PV", required=1)
    image = fields.Many2many('ir.attachment', string="Image")
    piece_jointe = fields.Many2many('ir.attachment', relation="piece_ods_rel",
                                    column1="piece_id",
                                    column2="ods_id", string="Pièce Jointe")
    avis_gratuit = fields.Boolean(string="Facturation Gratuite", default=False)
    state_avis = fields.Selection(
        selection=[('photos', 'Photos'), ('piece', 'Pièce Jointe'), ('cloture', 'Cloturé')], string="Statut Avis",
        default='photos')

    # Je fais appel au wizard qui calcule les lignes de la Note d'honoraires lors de la cloture du dossier afin de permettre à l'expert de + ou - les lignes
    def cloturer_avis(self):
        if not self.avis_gratuit:
            action = self.env["ir.actions.actions"]._for_xml_id(
                "expertise_auto_sae.action_cloturer_avis_wizard")

            return action
        else:
            self.state = 'cloture'

    def suivant_pv(self):
        for record in self:
            if record.state_avis == 'photos':
                record.state_avis = 'piece'
            elif record.state_avis == 'piece':
                record.state_avis = 'cloture'

    def precedent_avis(self):
        for record in self:
            if record.state_avis == 'piece':
                record.state_avis = 'photos'
            elif record.state_avis == 'cloture':
                record.state_avis = 'piece'

    # ce bouton permet de visualiser les dossier qui portent la meme immatriculation
    def historique_immatriculation(self):

        return self.env["ir.actions.actions"]._for_xml_id(
            "expertise_auto_sae.action_historique_immatriculations_wizard")
