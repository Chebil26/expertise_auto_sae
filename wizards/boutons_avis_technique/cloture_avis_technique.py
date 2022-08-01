from odoo.exceptions import UserError
from odoo import models, fields, api


class FactureLineSAE(models.Model):
    _name = 'facture.line'

    note_hono = fields.Boolean(related="product_id.note_hono")
    product_id = fields.Many2one("product.product", string="Article")
    name = fields.Char(string='Description')
    quantity = fields.Float(string='Quantité', default=1.0)
    price_unit = fields.Float(string='P U')
    tax_ids = fields.Many2many(comodel_name='account.tax', string="Taxes")

    @api.onchange('product_id')
    def recuperer_infos_related_product(self):
        for record in self:
            list_tax = []
            if record.product_id:
                for tax in record.product_id.taxes_id:
                    list_tax.append(tax.id)
                record.update({'tax_ids': [(6, 0, list_tax)]})
                record.update({'name': record.product_id.display_name})
                record.update({'price_unit': record.product_id.lst_price})


class CloturerAvisTechnique(models.TransientModel):
    _name = 'cloturer.avis.technique'

    dossier_id = fields.Many2one(comodel_name='sae.expertise.auto', string="Dossier",
                                 default=lambda self: self.env.context.get('active_id'), readonly=True)

    lignes_honoraires_ids = fields.Many2many('facture.line')

    @api.onchange('dossier_id')
    def charger_ligne_honoraire(self):
        context = dict(self._context) or {}
        dossier = self.env['sae.expertise.auto'].browse(context.get('active_id', False))
        data = []

        avis_technique = self.env["product.product"].search([('default_code', '=', 3)])
        data.append([0, 0, {
            'product_id': avis_technique.id,
            'price_unit': avis_technique.lst_price,
            'quantity': 1,
            'name': avis_technique.display_name,

            'tax_ids': avis_technique.taxes_id}])

        if dossier.type_pv == "additif":
            hono_additif = self.env["product.product"].search([('default_code', '=', 4)])
            data.append([0, 0, {
                'product_id': hono_additif.id,
                'price_unit': hono_additif.lst_price,
                'quantity': 1,
                'name': hono_additif.display_name,

                'tax_ids': hono_additif.taxes_id,

            }])
        frais_dossier = self.env["product.product"].search([('default_code', '=', 5)])
        data.append([0, 0, {
            'product_id': frais_dossier.id,
            'price_unit': frais_dossier.lst_price,
            'quantity': 1,
            'name': frais_dossier.display_name,

            'tax_ids': frais_dossier.taxes_id,

        }])

        photos = self.env["product.product"].search([('default_code', '=', 6)])
        data.append([0, 0, {
            'product_id': photos.id,
            'price_unit': photos.lst_price,
            'quantity': 0,
            'name': photos.display_name,

            'tax_ids': photos.taxes_id,

        }])
        if dossier.lieu_id.code == "H" or dossier.lieu_id.code == "V":
            frais_deplacement = self.env["product.product"].search([('default_code', '=', 7)])
            data.append([0, 0, {
                'product_id': frais_deplacement.id,
                'price_unit': frais_deplacement.lst_price,
                'quantity': 1,
                'name': frais_deplacement.display_name,

                'tax_ids': frais_deplacement.taxes_id,

            }])
        if dossier.lieu_id.code == "V":
            vacation = self.env["product.product"].search([('default_code', '=', 8)])
            data.append([0, 0, {
                'product_id': vacation.id,
                'price_unit': vacation.lst_price,
                'quantity': 1,
                'name': vacation.display_name,

                'tax_ids': vacation.taxes_id,

            }])
        if dossier.lieu_id.code == "H" or dossier.lieu_id.code == "V":
            repas = self.env["product.product"].search([('default_code', '=', 9)])
            data.append([0, 0, {
                'product_id': repas.id,
                'price_unit': repas.lst_price,
                'quantity': 1,
                'name': repas.display_name,

                'tax_ids': repas.taxes_id,

            }])
        if dossier.lieu_id.code == "H" or dossier.lieu_id.code == "V":
            sejour = self.env["product.product"].search([('default_code', '=', 10)])
            data.append([0, 0, {
                'product_id': sejour.id,
                'price_unit': sejour.lst_price,
                'quantity': 1,
                'name': sejour.display_name,

                'tax_ids': sejour.taxes_id,

            }])
        if dossier.lieu_id.code == "H":
            sejour = self.env["product.product"].search([('default_code', '=', 13)])
            data.append([0, 0, {
                'product_id': sejour.id,
                'price_unit': sejour.lst_price,
                'quantity': 1,
                'name': sejour.display_name,
                'tax_ids': sejour.taxes_id,
            }])
        self.write({'lignes_honoraires_ids': data})

    def confirmer(self):
        message = "Vous devez choisir Une ligne pour la note d'honoraire (champs vide)"

        if not self.lignes_honoraires_ids and not self.dossier_id.avis_gratuit:
            raise UserError(message)
        self.dossier_id.write({'state': 'cloture'})
        self.dossier_id.write({'date_cloture': fields.Date.today()})
        data = []
        for note in self.lignes_honoraires_ids:
            data.append([0, 0, {
                'product_id': note.product_id.id,
                'price_unit': note.price_unit,
                'name': note.name,
                'quantity': note.quantity,
                'tax_ids': note.tax_ids,

            }])
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'narration': self.dossier_id.obsrv,
            'dossier_ods': self.dossier_id.id,
            'currency_id': self.dossier_id.currency_id.id,
            'user_id': self.env.user.id,
            'invoice_user_id': self.env.user.id,
            'partner_id': self.dossier_id.code_agence.id,
            'fiscal_position_id': self.dossier_id.code_agence.property_account_position_id.id,
            'invoice_origin': self.dossier_id.name,
            'invoice_line_ids': data,
            'company_id': self.env.company.id,
            'state': 'draft',
        })
        self.dossier_id.note_honoraire_ids = invoice.id
        action = self.env.ref('expertise_auto_sae.note_hono_auto_report').report_action(self.dossier_id)
        action.update({'close_on_report_download': True})
        return action

    def annuler(self):
        self.dossier_id.write({'state': self.dossier_id.state})
        return {"type": "ir.actions.act_window_close"}
