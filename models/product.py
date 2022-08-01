from odoo import models, fields, api, _


class ProductCategory(models.Model):
    _inherit = "product.category"

    # Ajouter dans la catégorie d'article l'info Note d'honoraire Afin de permettre de faire un domaine sur les articles
    note_honoraire = fields.Boolean(string="Note d'honoraire")


class ProductSAE(models.Model):
    _inherit = 'product.template'

    note_hono = fields.Boolean(related="categ_id.note_honoraire")
