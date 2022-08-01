from odoo.exceptions import UserError

from odoo import models, fields


class ReaffectationExpert(models.TransientModel):
    _name = 'reaffectation.expert.wizard'

    dossier_id = fields.Many2one(comodel_name='sae.expertise.auto', string="Dossier",
                                 default=lambda self: self.env.context.get('active_id'), readonly=True)

    def _get_default_expert_id(self):
        context = dict(self._context) or {}
        dossier = self.env['sae.expertise.auto'].browse(context.get('active_id', False))
        return dossier.expert_id.id

    expert_id = fields.Many2one('hr.employee', string="Nouvel Expert", domain="[('id', '!=', expert_ancien_id)]")
    expert_ancien_id = fields.Many2one('hr.employee', string="Ancien Expert", readonly=1,
                                       default=_get_default_expert_id)

    def confirmer(self):
        message = "Vous devez choisir Un Nouvel Expert (champs vide)"

        if not self.expert_id:
            raise UserError(message)
        self.dossier_id.expert_id = self.expert_id.id
        self.dossier_id.date_reaffectation = fields.Date.today()

    def annuler(self):
        self.dossier_id.write({'state': self.dossier_id.state})
        return {"type": "ir.actions.act_window_close"}
