from odoo.exceptions import UserError

from odoo import models, fields


class ChangementLieu(models.TransientModel):
    _name = 'changer.num.chassis.wizard'

    dossier_id = fields.Many2one(comodel_name='sae.expertise.auto', string="Dossier",
                                 default=lambda self: self.env.context.get('active_id'), readonly=True)

    def _get_default_num_chas(self):
        context = dict(self._context) or {}
        dossier = self.env['sae.expertise.auto'].browse(context.get('active_id', False))
        return dossier.num_chas

    def _get_default_num_chas_pv(self):
        context = dict(self._context) or {}
        dossier = self.env['sae.expertise.auto'].browse(context.get('active_id', False))
        return dossier.num_chas_pv

    num_chas_pv = fields.Char("VIN Expert", readonly=1, default=_get_default_num_chas_pv)
    num_chas_pv_ancien = fields.Char(string="VIN Réception", readonly=1,
                                     default=_get_default_num_chas)

    def maj_chas_pv_ancien(self):
        message = "Vous devez saisir le Numéro de Chassis (champs vide)"
        if not self.num_chas_pv:
            raise UserError(message)
        self.dossier_id.write({"num_chas": self.num_chas_pv})

    def maj_chas_num_chas_pv(self):
        message = "Vous devez saisir le Numéro de Chassis (champs vide)"
        if not self.num_chas_pv:
            raise UserError(message)
        self.dossier_id.write({"num_chas_pv": self.num_chas_pv_ancien})
