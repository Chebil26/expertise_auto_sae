from odoo.exceptions import UserError

from odoo import models, fields


class ChangementLieu(models.TransientModel):
    _name = 'changer.lieu.wizard'

    dossier_id = fields.Many2one(comodel_name='sae.expertise.auto', string="Dossier",
                                 default=lambda self: self.env.context.get('active_id'), readonly=True)

    def _get_default_lieu_id(self):
        context = dict(self._context) or {}
        dossier = self.env['sae.expertise.auto'].browse(context.get('active_id', False))
        return dossier.lieu_id.id

    lieu_id = fields.Many2one('sae.lieu', string="Lieu de visite", domain="[('id', '!=', lieu_ancien_id)]")
    lieu_ancien_id = fields.Many2one('sae.lieu', string="Ancien Lieu de visite", readonly=1,
                                     default=_get_default_lieu_id)

    def confirmer(self):
        message = "Vous devez choisir Un Nouveau Lieu de visite (champs vide)"
        for record in self:
            if not record.lieu_id:
                raise UserError(message)
            # self.dossier_id.lieu_id = self.lieu_id.id
            if record.dossier_id.obsrv:
                record.dossier_id.write({'obsrv': str(self.dossier_id.obsrv + "\n Changement lieu de Visite")})
            else:
                record.dossier_id.write({'obsrv': "Changement lieu de Visite"})
            photo_ids = []
            for photo in record.dossier_id.photos_ids.ids:
                img = []
                for image in photo.images:
                    img.append(image.id)
                photo_ids.append([0, 0, {
                    'images': img,
                    'note': photo.note,
                    'traitement': photo.traitement.id
                }])
            choc = []
            for chocs in record.dossier_id.chocs_ids:
                choc.append([0, 0, {
                    'classe': chocs.classe,
                    'name': chocs.name.id,
                    'desc': chocs.desc,
                    'obligatoire': chocs.obligatoire,
                    'traitement': chocs.traitement.id
                }])
            reparations = []
            for reparation in record.dossier_id.reparations1_ids:
                reparations.append([0, 0, {
                    'reparation_id': reparation.reparation_id.id,
                    'duree': reparation.duree,
                    'forfait': reparation.forfait,
                    'montant': reparation.montant,
                    'desc': reparation.desc,
                    'traitement1': reparation.traitement1.id
                }])
            reparation2 = []
            for reparation in record.dossier_id.reparations2_ids:
                reparation2.append([0, 0, {
                    'reparation_id': reparation.reparation_id.id,
                    'duree': reparation.duree,
                    'forfait': reparation.forfait,
                    'montant': reparation.montant,
                    'desc': reparation.desc,
                    'traitement2': reparation.traitement2.id
                }])
            reparation3 = []
            for reparation in record.dossier_id.reparations3_ids:
                reparation3.append([0, 0, {
                    'reparation_id': reparation.reparation_id.id,
                    'duree': reparation.duree,
                    'forfait': reparation.forfait,
                    'montant': reparation.montant,
                    'desc': reparation.desc,
                    'traitement3': reparation.traitement3.id
                }])
            reparation4 = []
            for reparation in record.dossier_id.reparations4_ids:
                reparation4.append([0, 0, {
                    'reparation_id': reparation.reparation_id.id,
                    'duree': reparation.duree,
                    'forfait': reparation.forfait,
                    'montant': reparation.montant,
                    'desc': reparation.desc,
                    'traitement4': reparation.traitement4.id
                }])
            reparation5 = []
            for reparation in record.dossier_id.reparations5_ids:
                reparation5.append([0, 0, {
                    'reparation_id': reparation.reparation_id.id,
                    'duree': reparation.duree,
                    'forfait': reparation.forfait,
                    'montant': reparation.montant,
                    'desc': reparation.desc,
                    'traitement5': reparation.traitement5.id
                }])
            reparation6 = []
            for reparation in record.dossier_id.reparations6_ids:
                reparation6.append([0, 0, {
                    'reparation_id': reparation.reparation_id.id,
                    'duree': reparation.duree,
                    'forfait': reparation.forfait,
                    'montant': reparation.montant,
                    'desc': reparation.desc,
                    'traitement6': reparation.traitement6.id
                }])
            fourniture1 = []
            for fourniture in record.dossier_id.fournitures1_ids:
                list_tax = []
                for tax in fourniture.taxe_ids:
                    list_tax.append(tax.id)
                fourniture1.append([0, 0, {
                    'piece_id': fourniture.piece_id.id,
                    'taxe_ids': list_tax,
                    'quantite': fourniture.quantite,
                    'vetuste': fourniture.vetuste,
                    'taux_vet': fourniture.taux_vet,
                    'facturation': fourniture.facturation,
                    'montant_ht': fourniture.montant_ht,
                    'prix_ht': fourniture.prix_ht,
                    'montant_ttc': fourniture.montant_ttc,
                    'type_montant': fourniture.type_montant,
                    'ref_fact': fourniture.ref_fact,
                    'date_fact': fourniture.date_fact,
                    'traitement1': fourniture.traitement1.id
                }])
            fourniture2 = []
            for fourniture in record.dossier_id.fournitures2_ids:
                list_tax = []
                for tax in fourniture.taxe_ids:
                    list_tax.append(tax.id)
                fourniture2.append([0, 0, {
                    'piece_id': fourniture.piece_id.id,
                    'taxe_ids': list_tax,
                    'quantite': fourniture.quantite,
                    'vetuste': fourniture.vetuste,
                    'taux_vet': fourniture.taux_vet,
                    'facturation': fourniture.facturation,
                    'montant_ht': fourniture.montant_ht,
                    'prix_ht': fourniture.prix_ht,
                    'montant_ttc': fourniture.montant_ttc,
                    'type_montant': fourniture.type_montant,
                    'ref_fact': fourniture.ref_fact,
                    'date_fact': fourniture.date_fact,
                    'traitement2': fourniture.traitement2.id
                }])
            fourniture3 = []
            for fourniture in record.dossier_id.fournitures3_ids:
                list_tax = []
                for tax in fourniture.taxe_ids:
                    list_tax.append(tax.id)
                fourniture3.append([0, 0, {
                    'piece_id': fourniture.piece_id.id,
                    'taxe_ids': list_tax,
                    'quantite': fourniture.quantite,
                    'vetuste': fourniture.vetuste,
                    'taux_vet': fourniture.taux_vet,
                    'facturation': fourniture.facturation,
                    'montant_ht': fourniture.montant_ht,
                    'prix_ht': fourniture.prix_ht,
                    'montant_ttc': fourniture.montant_ttc,
                    'type_montant': fourniture.type_montant,
                    'ref_fact': fourniture.ref_fact,
                    'date_fact': fourniture.date_fact,
                    'traitement3': fourniture.traitement3.id
                }])
            fourniture4 = []
            for fourniture in record.dossier_id.fournitures4_ids:
                list_tax = []
                for tax in fourniture.taxe_ids:
                    list_tax.append(tax.id)
                fourniture4.append([0, 0, {
                    'piece_id': fourniture.piece_id.id,
                    'taxe_ids': list_tax,
                    'quantite': fourniture.quantite,
                    'vetuste': fourniture.vetuste,
                    'taux_vet': fourniture.taux_vet,
                    'facturation': fourniture.facturation,
                    'montant_ht': fourniture.montant_ht,
                    'prix_ht': fourniture.prix_ht,
                    'montant_ttc': fourniture.montant_ttc,
                    'type_montant': fourniture.type_montant,
                    'ref_fact': fourniture.ref_fact,
                    'date_fact': fourniture.date_fact,
                    'traitement4': fourniture.traitement4.id
                }])
            fourniture5 = []
            for fourniture in record.dossier_id.fournitures5_ids:
                list_tax = []
                for tax in fourniture.taxe_ids:
                    list_tax.append(tax.id)
                fourniture5.append([0, 0, {
                    'piece_id': fourniture.piece_id.id,
                    'taxe_ids': list_tax,
                    'quantite': fourniture.quantite,
                    'vetuste': fourniture.vetuste,
                    'taux_vet': fourniture.taux_vet,
                    'facturation': fourniture.facturation,
                    'montant_ht': fourniture.montant_ht,
                    'prix_ht': fourniture.prix_ht,
                    'montant_ttc': fourniture.montant_ttc,
                    'type_montant': fourniture.type_montant,
                    'ref_fact': fourniture.ref_fact,
                    'date_fact': fourniture.date_fact,
                    'traitement5': fourniture.traitement5.id
                }])
            fourniture6 = []
            for fourniture in record.dossier_id.fournitures6_ids:
                list_tax = []
                for tax in fourniture.taxe_ids:
                    list_tax.append(tax.id)
                fourniture6.append([0, 0, {
                    'piece_id': fourniture.piece_id.id,
                    'taxe_ids': list_tax,
                    'quantite': fourniture.quantite,
                    'vetuste': fourniture.vetuste,
                    'taux_vet': fourniture.taux_vet,
                    'facturation': fourniture.facturation,
                    'montant_ht': fourniture.montant_ht,
                    'prix_ht': fourniture.prix_ht,
                    'montant_ttc': fourniture.montant_ttc,
                    'type_montant': fourniture.type_montant,
                    'ref_fact': fourniture.ref_fact,
                    'date_fact': fourniture.date_fact,
                    'traitement6': fourniture.traitement6.id
                }])
            print(record.dossier_id.state)
            pre_enregistrement = {
                "compagnie": self.dossier_id.compagnie.id,
                "expert_id": self.dossier_id.expert_id.id,
                "nature_id": self.dossier_id.nature_id.id,
                "lieu_id": self.lieu_id.id,
                "state":self.dossier_id.state,
                "state_expertise": 'photos',
                "code_agence": self.dossier_id.code_agence.id,
                "etat_vehi": self.dossier_id.etat_vehi,
                "num_ods": self.dossier_id.num_ods,
                "val_vet": self.dossier_id.val_vet,
                "num_chass_diff": self.dossier_id.num_chass_diff,
                "histo_num_chassis": self.dossier_id.histo_num_chassis,
                "taux_vet": self.dossier_id.taux_vet,
                "total_ht": self.dossier_id.total_ht,
                "val_venale_syn": self.dossier_id.val_venale_syn,
                "an_mec": self.dossier_id.an_mec,
                "type_ref": self.dossier_id.type_ref,
                "desc_ref": self.dossier_id.desc_ref,
                "val_venale": self.dossier_id.val_venale,
                "val_epave": self.dossier_id.val_epave,
                "nbr_tiers": self.dossier_id.nbr_tiers,
                "nom_tiers": self.dossier_id.nom_tiers,
                "num_plc": self.dossier_id.num_plc,
                "lettre_bln": self.dossier_id.lettre_bln,
                "agence_tiers": self.dossier_id.agence_tiers,
                "compagnie_tiers": self.dossier_id.compagnie_tiers.id,
                "kilometrage": self.dossier_id.kilometrage,
                "mrqe_id": self.dossier_id.mrqe_id.id,
                "mdle_id": self.dossier_id.mdle_id.id,
                "genre_id": self.dossier_id.genre_id.id,
                "type_id": self.dossier_id.type_id.id,
                "enrg_id": self.dossier_id.enrg_id.id,
                "origine_additif": self.dossier_id.origine_additif.id,
                "operating_unit": self.dossier_id.operating_unit.id,
                "couleur_id": self.dossier_id.couleur_id.id,
                "carosserie_id": self.dossier_id.carosserie_id.id,
                "puissance": self.dossier_id.puissance,
                "commune_id": self.dossier_id.commune_id.id,
                "wilaya": self.dossier_id.wilaya.id,
                "distance": self.dossier_id.distance,
                "nbr_nuit": self.dossier_id.nbr_nuit,
                "nbr_rps": self.dossier_id.nbr_rps,
                "nbr_vac": self.dossier_id.nbr_vac,
                "nom_assure": self.dossier_id.nom_assure,
                "contact": self.dossier_id.contact,
                "date_sinistre": self.dossier_id.date_sinistre,
                "num_sinistre": self.dossier_id.num_sinistre,
                "Type_imma": self.dossier_id.Type_imma,
                "immatricul": self.dossier_id.immatricul,
                "num_chas": self.dossier_id.num_chas,
                "obsrv": self.dossier_id.obsrv,
                "date_ods": self.dossier_id.date_ods,
                "num_chas_pv": self.dossier_id.num_chas_pv,
                "photos_null": self.dossier_id.photos_null,
                "type_pv": self.dossier_id.type_pv,
                "photos_lettre_null": self.dossier_id.photos_lettre_null,
                "lettre_null": self.dossier_id.lettre_null,

            }
            auto = self.env["sae.expertise.auto"].create(pre_enregistrement)
            auto.write({"photos_ids": photo_ids})
            auto.write({"chocs_ids": False})
            auto.write({"chocs_ids": choc})
            auto.write({"reparations1_ids": reparations})
            auto.write({"reparations2_ids": reparation2})
            auto.write({"reparations3_ids": reparation3})
            auto.write({"reparations4_ids": reparation4})
            auto.write({"reparations5_ids": reparation5})
            auto.write({"reparations6_ids": reparation6})
            auto.write({"fournitures6_ids": fourniture6})
            auto.write({"fournitures5_ids": fourniture5})
            auto.write({"fournitures4_ids": fourniture4})
            auto.write({"fournitures3_ids": fourniture3})
            auto.write({"fournitures2_ids": fourniture2})
            auto.write({"fournitures1_ids": fourniture1})
            view_id = self.env.ref('expertise_auto_sae.sae_expertise_auto_form_view').id
            self.dossier_id.write({'state': 'annule'})
            self.ensure_one()
            return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form,tree',
            'res_model': "sae.expertise.auto",
            'target': 'current',
            'context': pre_enregistrement,
            'res_id': auto['id'],
            'views': [[view_id, 'form']],
        }

    def annuler(self):
        self.dossier_id.write({'state': self.dossier_id.state})
        return {"type": "ir.actions.act_window_close"}
