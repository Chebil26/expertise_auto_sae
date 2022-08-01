from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json

import base64
import tempfile

from pyzbar.pyzbar import decode
from PIL import Image


class CreationOds(models.TransientModel):
    _name = 'creation.ods.wizard'

    code_agence_domain = fields.Char( compute="set_domain_for_code_agence")

    @api.depends('compagnie', 'code_agence')
    def set_domain_for_code_agence(self):
        compagnie = self.env["res.partner"].search([('is_customer', '=', True), ('first_level', '!=', True)])
        for record in self:
            niveau_2 = []
            niveau_1 = self.env["res.partner"].search(
                [('is_customer', '=', True), ('company_group_id', '=', record.compagnie.id)])
            for line1 in compagnie:
                for line2 in niveau_1:
                    if line1.company_group_id.id == line2.id:
                        niveau_2.append(line1.id)
            record.code_agence_domain = json.dumps([('id', 'in', niveau_2)])

    # informations Client
    compagnie = fields.Many2one('res.partner', string="Compagnie", required=True,
                                domain="[('is_customer', '=', True),('first_level', '=', True)]")
    code_agence = fields.Many2one('res.partner', string="Code Agence", required=True)
    date_ods = fields.Date("Date ODS", required=True)
    nom_assure = fields.Char("Nom Assuré", required=True)
    contact = fields.Char("Contact")
    # informations sinistre
    date_sinistre = fields.Date("Date Sinistre")
    num_sinistre = fields.Char("N° Sinistre")
    # informations Expertise
    expert_id = fields.Many2one('hr.employee', string="Expert", required=True)

    qrf = fields.Binary("qrcode")
    qrt = fields.Text("QR CodeF")

    def _get_default_nature_id(self):
        return self.env.ref('expertise_auto_sae.nature_expertise').id

    nature_id = fields.Many2one('sae.nature', string="Nature d'expertise", default=_get_default_nature_id,
                                required=True)
    type_nature = fields.Selection(related="nature_id.type_nature")

    def _get_default_lieu_id(self):
        return self.env.ref('expertise_auto_sae.lieu_centre').id

    lieu_id = fields.Many2one('sae.lieu', string="Lieu de visite", default=_get_default_lieu_id, required=True)
    # informations véhicule
    Type_imma = fields.Selection(
        selection=[('alg_5', 'Algérie 05 chiffres'), ('alg_6', 'Algérie 06 chiffres'),
                   ('neuf', 'Algérie véhicule neuf'), ('autre', 'Autre')],
        string='Type Immatricule', default='alg_5')
    immatricul = fields.Char("Immatriculation")
    num_chas = fields.Char("N° chassis (VIN)")
    num_ods = fields.Char("N° ODS", required=True)
    obsrv = fields.Text("Observation")

    def get_operating_unit_default(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        return user.default_operating_unit_id.id

    operating_unit_domain = fields.Char(
        compute="set_domain_for_operating_unit",
        readonly=True,
        store=False,
    )

    @api.depends('operating_unit')
    def set_domain_for_operating_unit(self):
        context = self._context
        current_uid = context.get('uid')
        user = self.env['res.users'].browse(current_uid)
        units = []
        for unit in user.operating_unit_ids:
            units.append(unit.id)
        self.operating_unit_domain = json.dumps([('id', 'in', units)])

    operating_unit = fields.Many2one(string="Centre", comodel_name="operating.unit", default=get_operating_unit_default,
                                     required=True)

    @api.onchange('nature_id', 'code_agence', 'num_sinistre')
    def controle_numero_sinistre(self):
        for record in self:
            if record.nature_id and record.code_agence and record.num_sinistre:
                sinistres = self.env['sae.expertise.auto'].search([
                    ('nature_id', '=', record.nature_id.id),
                    ('code_agence', '=', record.code_agence.id),
                    ('num_sinistre', '=', record.num_sinistre),
                ])
                if sinistres:
                    raise UserError("Ce Sinistre est déja Enregistré !")

    @api.onchange('date_ods', 'date_sinistre')
    def verification_sur_date_sinistre_et_ods(self):
        for record in self:
            message = "Date d'ODS doit être : \n"
            test1 = False
            test2 = False
            if record.date_ods:
                if record.date_ods > fields.Date.today():
                    message += "- Inférieure ou égale à la date d'aujourd'hui. \n"
                    test1 = True

            if record.date_ods and record.date_sinistre:
                if record.date_ods < record.date_sinistre:
                    message += "- superieur à la date de Sinistre. \n"
                    test2 = True

            if test1 or test2:
                raise UserError(message)

    def creer(self):

        dossier = {
            "compagnie": self.compagnie.id,
            "state": 'cree',
            "code_agence": self.code_agence.id,
            "date_ods": self.date_ods,
            "num_ods": self.num_ods,
            "nom_assure": self.nom_assure,
            "contact": self.contact,
            "date_sinistre": self.date_sinistre,
            "num_sinistre": self.num_sinistre,
            "Type_imma": self.Type_imma,
            "immatricul": self.immatricul,
            "num_chas": self.num_chas,
            "obsrv": self.obsrv,
            "expert_id": self.expert_id.id,
            "nature_id": self.nature_id.id,
            "lieu_id": self.lieu_id.id,
            "operating_unit": self.operating_unit.id,
        }
        auto = self.env["sae.expertise.auto"].create(dossier)
        msg = str("Votre ODS Avec Le Numéro : " + str(auto['name']) + "a bien été crée")
        self.env.user.notify_success(message=msg)

    def sauvegarder_et_creer(self):
        self.creer()
        view_id = self.env.ref(
            'expertise_auto_sae.view_creation_ods_wizard'
        ).id
        return {
            'type': 'ir.actions.act_window',
            'name': _('Création ODS'),
            'res_model': 'creation.ods.wizard',
            'target': 'new',
            'view_mode': 'form',
            'views': [[view_id, 'form']]
        }



    # fonction qui permet de remplir les champs du dossier a partir d'un qr code
    @api.onchange('qrt')
    def qr(self):

        #if (self.qrf):
            #file = tempfile.TemporaryFile(suffix=".png")
            #file.write(base64.decodestring(self.qrf))
            #d = decode(Image.open(file))
            #st = d[0].data.decode("ascii")
            #strr = "AUTOMOBILE;O;2920;2020-0010;30-12-2019;2020-110010;30-12-2019;LEGHIOUGH   ABDELHAFID;1100014169;MAAMAR AHMED;2674/1100007135;SAA;2674 CONSTANTINE;WV1ZZZ2KZR001729;064885-00-48;2019;6;LEGER"


            #creation d'une list des champs a partir du qr code saisie
            stlist = str(self.qrt).split(";")


            #test de compatibiliter du code saisie
            if len(stlist) > 15:

                #reformatation des dates de "yy-mm-dd" a "dd-mm-yy"
                l_date_ods = stlist[4].split("-")
                l_date_ods.reverse()
                date_ods = '-'.join(l_date_ods)

                l_date_sin = stlist[6].split("-")
                l_date_sin.reverse()
                date_sin = '-'.join(l_date_sin)


                #affection des valeurs a leur champs
                self.contact = stlist[0]

                if self.env['res.partner'].search([('name', '=', stlist[2])], limit=1).name:
                    self.code_agence = self.env['res.partner'].search([('name', '=', stlist[2])], limit=1).id

                self.code_agence = stlist[2]
                self.num_ods = stlist[3]
                self.date_ods = date_ods
                self.num_sinistre = stlist[5]
                self.date_sinistre = date_sin
                self.nom_assure = stlist[7]

                if self.env['res.partner'].search([('name', '=', stlist[11])], limit=1).name:
                    self.compagnie = self.env['res.partner'].search([('name', '=', stlist[11])], limit=1).id

                self.num_chas = stlist[13]
                self.immatricul = stlist[14]



