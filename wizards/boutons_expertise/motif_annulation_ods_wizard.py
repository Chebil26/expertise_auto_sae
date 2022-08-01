from odoo import api, fields, models


class MotifAnnulation(models.TransientModel):
    _name = 'sae.motif.annulation'
    _description = 'Motif d''Annulation d''un Ods'

    lost_reason = fields.Char( 'Motif d''Annulation')

    def confirmer(self):
        ods = self.env['sae.expertise.auto'].browse(self.env.context.get('active_ids'))
        ods.state = 'annule'
        ods.date_annulation = fields.Date.today()

