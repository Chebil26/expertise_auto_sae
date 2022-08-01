from odoo import models, fields, api, _


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    # ces sequences sont dédiées à l'expertise Auto de Type Sinistre
    sequence_centre_ref = fields.Many2one('ir.sequence', string='Référence Auto Centre', readonly=True)
    sequence_hors_centre_ref = fields.Many2one('ir.sequence', string='Référence  AutoHors Centre', readonly=True)
    sequence_vacation_ref = fields.Many2one('ir.sequence', string='Référence Auto Vacation', readonly=True)
    sequence_ead_ref = fields.Many2one('ir.sequence', string='Référence Auto EAD', readonly=True)

    # informations liées à chaque Centre
    rc = fields.Char(string="RC")
    nif = fields.Char(string="N.I.F")
    rib = fields.Char(string="R.I.B")
    nis = fields.Char(string="N.I.S")
    ai = fields.Char(string="Article d'imposition")

    # L'idée est d'automatiser les changements du field code_seq dans chaque sequence du centre

    # def write(self, values):
    #     unit = super(OperatingUnit, self).write(values)
    #     if 'code_seq' in values:
    #         for record in self:
    #
    #             seq_centre = self.env["ir.sequence"].search([('name', '=', str(record.id) + "_seq_centre")])
    #             seq_hors_centre = self.env["ir.sequence"].search([('name', '=', str(record.id) + "_seq_hors_centre")])
    #             seq_vacation = self.env["ir.sequence"].search([('name', '=', str(record.id) + "_seq_vacation")])
    #             seq_ead = self.env["ir.sequence"].search([('name', '=', str(record.id) + "_seq_ead")])
    #             seq_achat_dp = self.env["ir.sequence"].search([('name', '=', str(record.id) + "_seq_achat")])
    #             seq_achat_bc = self.env["ir.sequence"].search([('name', '=', str(record.id) + "_seq_achat_bc")])
    #             seq_da = self.env["ir.sequence"].search([('name', '=', str(record.id) + "_seq")])
    #             record.sequence_centre_ref.update({'prefix': record.code_seq + 'A' + '%(y)s' + 'C'})
    #             record.sequence_hors_centre_ref.update({'prefix': record.code_seq + 'A' + '%(y)s' + 'H'})
    #             record.sequence_vacation_ref.update({'prefix': record.code_seq + 'A' + '%(y)s' + 'V'})
    #             record.seq_ead.update({'prefix': record.code_seq + 'A' + '%(y)s' + 'D'})
    #             record.seq_achat_dp.update({'prefix': record.code_seq + '/' + '%(y)s' + '/DD/'})
    #             record.seq_achat_bc.update({'prefix': record.code_seq + '/' + '%(y)s' + '/BC/'})
    #             record.seq_da.update({'prefix': record.code_seq + '/' + '%(y)s' + '/DA/'})

    # Lors de la création des Centres j'attribue des sequences, Le code de la seq est une concat d'id et une str car l'id est la seule info unique
    @api.model
    def create(self, vals):
        unit = super(OperatingUnit, self).create(vals)
        sequence_centre = {
            'name': vals['name'] + " seq Centre",
            'code': str(unit['id']) + "_seq_centre",
            'implementation': 'standard',
            'padding': 5,
            'prefix': vals['code_seq'] + 'A' + '%(y)s' + 'C',
            'number_increment': 1,

        }
        vals['sequence_centre_ref'] = self.env['ir.sequence'].create(sequence_centre)
        sequence_hors_centre = {
            'name': vals['name'] + " seq Hors Centre",
            'code': str(unit['id']) + "_seq_hors_centre",
            'implementation': 'standard',
            'padding': 5,
            'prefix': vals['code_seq'] + 'A' + '%(y)s' + 'H',
            'number_increment': 1,

        }
        vals['sequence_hors_centre_ref'] = self.env['ir.sequence'].create(sequence_hors_centre)
        sequence_vacation = {
            'name': vals['name'] + " seq Vacation",
            'code': str(unit['id']) + "_seq_vacation",
            'implementation': 'standard',
            'padding': 5,
            'prefix': vals['code_seq'] + 'A' + '%(y)s' + 'V',
            'number_increment': 1,

        }
        vals['sequence_vacation_ref'] = self.env['ir.sequence'].create(sequence_vacation)
        sequence_ead = {
            'name': vals['name'] + " seq EAD",
            'code': str(unit['id']) + "_seq_ead",
            'implementation': 'standard',
            'padding': 5,
            'prefix': vals['code_seq'] + 'A' + '%(y)s' + 'D',
            'number_increment': 1,

        }
        vals['sequence_ead_ref'] = self.env['ir.sequence'].create(sequence_ead)
        return unit
