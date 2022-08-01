from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = "account.move"
    # ajouter l'information dossier dans facture client
    dossier_ods = fields.Many2one(string="Dossier ODS", comodel_name="sae.expertise.auto")
    compagnie = fields.Many2one('res.partner', string="Compagnie",
                                domain="[('is_customer', '=', True),('first_level', '=', True)]")
# -d SAE -u expertise_auto_sae