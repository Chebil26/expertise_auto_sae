from odoo import models, fields, api, _
from odoo.exceptions import UserError
import json

import base64
import tempfile
import pandas as pd
import csv
import io

from odoo.exceptions import ValidationError




from pyzbar.pyzbar import decode
from PIL import Image


class CreationOds(models.TransientModel):
    _name = 'creation.csv.wizard'



    csvf = fields.Binary("csv file",  readonly=False)

    #code_agence = fields.Many2one('sae.expertise.auto', string="Code Agence", required=True)
    num_sinistre = fields.Char("N° Sinistre")
    survenance_yr = fields.Integer("Année de survenance")
    date_expertise = fields.Date("Date expertise")
    expert = fields.Char("Expert")

    montant_fourniture = fields.Float("Montant TTC des fournitures")
    montant_peinture = fields.Float("Montant TTC de la peinture")
    montant_main_doeuvre = fields.Float("Montant TTC de la main d’œuvre")
    montant_note_honoraires = fields.Float("Montant TTC de la note d’honoraires")
    montant_fourniture_nonsoumis = fields.Float("Montant TTC des fournitures non soumis à vétusté")

    nbrj_immobilisation = fields.Integer("Nombre de jours d’immobilisation")
    vetuste = fields.Float("Taux de la vétusté")
    vin = fields.Char("VIN")



    def doo(self):


        csv_data = base64.b64decode(self.csvf)
        data_file = io.StringIO(csv_data.decode("utf-8"))
        data_file.seek(0)
        file_reader = []
        csv_reader = csv.reader(data_file)
        file_reader.extend(csv_reader)



        for i in file_reader:
            print(i[1])
            print(i[3])
            #self.env['pre.enregistrement'].create()

            #if self.env['sae.expertise.auto'].search([('code_agence', '=', i[1])], limit=1).name:
            #    self.code_agence = self.env['sae.expertise.auto'].search([('code_agence', '=', i[1])], limit=1).id
            #    self.env['res_partner'].create({"code_agence": self.code_agence})

            l_date_ods = i[4].split("/")
            l_date_ods.reverse()
            date_ods = '-'.join(l_date_ods)

            date_ods = date_ods.replace("'", "")

            raise UserError("numero ods manquant")
            raise UserError("code agence non trouvable")


            val = {
                "num_sinistre": i[3],
                "compagnie" : 1,

                #"code_agence": self.env['res_partner'].search([('code_agence', '=', i[2])], limit=1).id,
                "code_agence":'42',
                "date_ods": date_ods,
                "nom_assure": i[5],
                "expert_id": 1,
                "nature_id": 1,
                "num_ods": "11111111",
                "num_chas": i[13],
                }



            print(val)

            a = self.env['sae.expertise.auto'].create(val)
            print(val)
            #self.date_expertise = self.env['sae.expertise.auto'].create({"date_cloture": i[4]})
            #self.vetuste = self.env['sae.expertise.auto'].create({"taux_vet": i[12]})
            #self.vin = self.env['sae.expertise.auto'].create({"num_chas": i[13]})







        #print(self.csvf)
        #file = tempfile.NamedTemporaryFile(suffix=".csv")
        #file.write(self.csvf)
        #print(file.name)
        #print(file.read())
        #dff = pd.read_csv(str(file.name).replace("\\",'/'), header=None).sudo()
        #print(dff)





        #for i in expertise:
            #self.env['res.partner'].create()








