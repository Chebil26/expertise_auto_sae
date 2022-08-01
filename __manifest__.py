# -*- coding: utf-8 -*-
{
    'name': "EXPERTISE AUTO",

    'summary': "Ce module est dédié à l'expertise automobile de la SAE",

    'description': """
    """,
    'author': 'AYRADE',
    'maintainer': "OUKACI Nada",
    'website': "http://www.AYRADE.com",

    'category': 'Uncategorized',
    'version': '14.0',

    'depends': ['web',  'operating_unit', 'account',  'l10n_dz_region', 'web_domain_field',
                'web_notify', 'base'],

    # always loaded
    'data': [
        # data
        'data/valeurs_par_defaut.xml',
        'data/sequence_data.xml',
        'data/cron_expertise_auto.xml',

        # reports
        'reports/sae_pv_expert_report.xml',
        'reports/sae_note_honoraire.xml',
        'reports/letttre_invitation.xml',
        # views
        'views/pre_enregistrement_view.xml',
        'views/sae_expertise_auto_view.xml',
        'views/sae_configuration_table_view.xml',
        'views/expertise_a_distance_view.xml',
        'views/traitement_expertise_view.xml',
        'views/res_partner_views.xml',
        'views/operating_unit_view.xml',
        'views/account_move_views.xml',
        'views/product_category_view.xml',
        'views/traitement_expertise_avis_view.xml',
        # 'views/motif_annulation_ods_views.xml',

        # wizards
        'wizards/pre_enre/passage_de_enre_crea_view.xml',
        'wizards/boutons_expertise/reaffectation_expert_view.xml',
        'wizards/boutons_expertise/changement_lieu_visite_view.xml',
        'wizards/boutons_expertise/motif_annulation_ods_wizard_views.xml',
        'wizards/boutons_expertise/creation_ods_view.xml',
        'wizards/boutons_expertise/creation_csv_view.xml',
        'wizards/boutons_expertise_pv/ajouter_photos_view.xml',
        'wizards/boutons_expertise_pv/historique_num_chassis_view.xml',
        'wizards/boutons_expertise_pv/changement_num_chassis_view.xml',
        'wizards/boutons_expertise_pv/choix_prix_pieces_pv_view.xml',
        'wizards/boutons_expertise_pv/recherche_pieces_pv_view.xml',
        'wizards/boutons_avis_technique/cloture_avis_technique_view.xml',
        'wizards/boutons_avis_technique/historique_immatriculation_view.xml',
        'wizards/cloture/annule_remplace_pv_view.xml',

        # security
        'security/ir.model.access.csv',
        # 'security/security.xml',

        # menu
        'menu.xml',
        # 'action.xml',

    ],

}
