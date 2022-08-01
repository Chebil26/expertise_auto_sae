from odoo import models, fields, api


class HistoriqueNumChassisWizard(models.TransientModel):
    _name = 'historique.num.chassis.wizard'

    dossier_id = fields.Many2one(comodel_name='sae.expertise.auto', string="Dossier",
                                 default=lambda self: self.env.context.get('active_id'), readonly=True)

    dossier_chassis_ids = fields.One2many('sae.expertise.auto', compute="historique_num_chassis")

    @api.depends('dossier_id')
    def historique_num_chassis(self):
        pv = self.env["sae.expertise.auto"].search(
            [('num_chas_pv', '=', self.dossier_id.num_chas_pv), ('id', '!=', self.dossier_id.id)])
        self.dossier_chassis_ids = pv
        if pv:
            self.dossier_id.write({"histo_num_chassis": True})


