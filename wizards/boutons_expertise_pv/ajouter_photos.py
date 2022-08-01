from odoo import models, fields, api
from odoo.exceptions import UserError


class AjouterPhotos(models.TransientModel):
    _name = 'ajouter.photos.wizard'

    images = fields.Many2many('ir.attachment', string="Image", required=1)
    note = fields.Text("Note")

    def confirmer(self):
        dossier = self.env['sae.expertise.auto'].browse(self.env.context.get('active_id'))
        data = []
        img = []
        if not self.images:
            raise UserError("veuillez choisir aumoins une seule photo")
        for image in self.images:
            img.append(image.id)
        data.append([0, 0, {
            'images': img,
            'note': self.note,
        }])
        dossier.update({'photos_ids': data})

