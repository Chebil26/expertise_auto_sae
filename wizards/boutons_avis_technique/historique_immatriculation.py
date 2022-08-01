from odoo import models, fields, api


class HistoriqueImmatriculationWizard(models.TransientModel):
    _name = 'historique.immatriculations.wizard'

    dossier_id = fields.Many2one(comodel_name='sae.expertise.auto', string="Dossier",
                                 default=lambda self: self.env.context.get('active_id'), readonly=True)

    dossier_immatricul_ids = fields.One2many('sae.expertise.auto', compute="historique_num_chassis")

    @api.depends('dossier_id')
    def historique_immatriculation(self):
        self.dossier_immatricul_ids = self.env['sae.expertise.auto'].search([
            ('id', '!=', self.dossier_id.id),
            ('type_nature', '=', 'sinistre'),
            ('immatricul', '=', self.dossier_id.immatricul)
        ])
