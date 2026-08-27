#!/usr/bin/env python
"""
Synthetic demo corpus generator - "Meridian Labs".

Produces a fictional but structurally realistic quality-management document set
(procedures, risk analysis, team charter, glossary) as both Markdown and PDF.

The Markdown files are the ground-truth source used by `eval.py verify`.
The PDFs are what you feed to the api indexing pipeline.

Usage:
    python build_corpus.py                    # writes ./corpus/md + ./corpus/pdf
    python build_corpus.py --out corpus --formats md,pdf
    python build_corpus.py --formats md       # skip PDFs (no reportlab needed)

Every organisation, person, product and figure in this file is invented.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

ORG = "Meridian Labs"
ORG_SHORT = "MRD"

# --------------------------------------------------------------------------
# Corpus definition
#
# Each section body element is either a string (paragraph), a list of strings
# (bullet list), or {"table": [[header...], [row...], ...]}.
# --------------------------------------------------------------------------

DOCUMENTS: list[dict[str, Any]] = [
    {
        "ref": "AN-QA-MRD-000",
        "title": "Abreviations et definitions du systeme qualite",
        "version": "V3",
        "effective": "2025-01-15",
        "dept": "Assurance Qualite",
        "doc_type": "Annexe",
        "lang": "fr",
        "author": "Sarah Delaunay",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette annexe recense les abreviations et definitions utilisees dans "
                    "l'ensemble des documents du systeme qualite de Meridian Labs. Elle est "
                    "referencee par toutes les procedures du referentiel.",
                ],
            ),
            (
                "2. Abreviations",
                [
                    {
                        "table": [
                            ["Abreviation", "Signification"],
                            ["AQ", "Assurance Qualite"],
                            ["NC", "Non-Conformite"],
                            ["CAPA", "Corrective And Preventive Action"],
                            ["RSSI", "Responsable de la Securite des Systemes d'Information"],
                            ["DPO", "Delegue a la Protection des Donnees"],
                            ["MI", "Information Medicale"],
                            ["PV", "Pharmacovigilance"],
                            ["RTO", "Recovery Time Objective"],
                            ["RPO", "Recovery Point Objective"],
                            ["EBIOS RM", "Expression des Besoins et Identification des Objectifs de Securite - Risk Manager"],
                            ["MedDRA", "Medical Dictionary for Regulatory Activities"],
                            ["ALCOA+", "Attributable, Legible, Contemporaneous, Original, Accurate, plus"],
                        ]
                    }
                ],
            ),
            (
                "3. Definitions",
                [
                    "Non-conformite majeure : ecart susceptible d'affecter la securite du patient, "
                    "la qualite du service rendu au client, ou la conformite reglementaire.",
                    "Non-conformite mineure : ecart documentaire ou operationnel sans impact direct "
                    "sur la securite du patient ni sur la conformite reglementaire.",
                    "Mise en activite : date a partir de laquelle un document devient applicable et "
                    "opposable aux collaborateurs concernes.",
                ],
            ),
            (
                "4. Documents applicables",
                [
                    ["PR-QA-MRD-001 - Gestion documentaire du systeme qualite"],
                    ["PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)"],
                    ["PR-QA-MRD-011 - Revue de direction"],
                    ["PR-QA-MRD-012 - Maitrise du changement"],
                    ["PR-QA-MRD-017 - Maitrise des enregistrements qualite"],
                ],
            ),
        ],
        "revisions": [
            ("V3", "2025-01-15", "Ajout des termes ALCOA+ et EBIOS RM"),
            ("V2", "2023-09-04", "Ajout des termes RTO et RPO"),
            ("V1", "2022-03-01", "Creation"),
        ],
    },
    {
        "ref": "PR-QA-MRD-001",
        "title": "Gestion documentaire du systeme qualite",
        "version": "V6",
        "effective": "2025-02-10",
        "dept": "Assurance Qualite",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Sarah Delaunay",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet et domaine d'application",
                [
                    "La presente procedure decrit le cycle de vie des documents du systeme qualite "
                    "de Meridian Labs : redaction, verification, approbation, diffusion, revision "
                    "et archivage. Elle s'applique a l'ensemble des collaborateurs, y compris les "
                    "prestataires intervenant sur les processus qualite.",
                ],
            ),
            (
                "2. Responsabilites",
                [
                    [
                        "Le redacteur produit la version de travail et renseigne le tableau de revisions.",
                        "Le verificateur controle la coherence technique et les references croisees.",
                        "Le Responsable Assurance Qualite approuve le document et declenche sa mise en activite.",
                        "Chaque manager s'assure de l'accuse de reception de ses collaborateurs.",
                    ]
                ],
            ),
            (
                "3. Circuit d'approbation",
                [
                    "Aucun document ne peut etre mis en activite sans l'approbation du Responsable "
                    "Assurance Qualite. L'approbation est tracee electroniquement dans l'outil de "
                    "gestion documentaire, avec horodatage et identite de l'approbateur.",
                ],
            ),
            (
                "4. Auto-formation et accuse de reception",
                [
                    "Apres approbation, le document est diffuse aux collaborateurs concernes. "
                    "Ceux-ci disposent d'un delai d'auto-formation de 15 jours ouvres pour prendre "
                    "connaissance du document et accuser reception avant sa mise en activite.",
                    "Passe ce delai, le manager relance nominativement les collaborateurs n'ayant "
                    "pas accuse reception. Un taux d'accuse de reception inferieur a 90 pour cent a "
                    "la date de mise en activite constitue une non-conformite mineure au sens de la "
                    "procedure PR-QA-MRD-009.",
                ],
            ),
            (
                "5. Revision periodique",
                [
                    "Chaque document du systeme qualite fait l'objet d'une revision periodique tous "
                    "les 3 ans, ou de facon anticipee en cas d'evolution reglementaire, de "
                    "reorganisation, ou a la suite d'une action corrective.",
                ],
            ),
            (
                "6. Archivage et conservation",
                [
                    "Les documents qualite approuves sont archives pendant 10 ans a compter de leur "
                    "date de retrait. L'archivage est electronique, sur le coffre-fort documentaire "
                    "decrit dans la procedure PR-ITS-MRD-004.",
                    "La conservation des dossiers individuels de formation des collaborateurs releve "
                    "de la procedure PR-EXM-MRD-003 et suit une regle distincte.",
                ],
            ),
            (
                "7. Documents externes",
                [
                    "Un document externe (norme, texte reglementaire, exigence client) est enregistre "
                    "dans le meme referentiel documentaire que les documents internes, avec mention de "
                    "sa source et de sa date de derniere verification aupres de l'emetteur. Sa revision "
                    "n'est pas planifiee : elle est declenchee par la publication d'une nouvelle "
                    "version par l'emetteur.",
                ],
            ),
            (
                "8. Documents associes",
                [
                    ["PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)"],
                    ["PR-QA-MRD-012 - Maitrise du changement"],
                    ["PR-QA-MRD-017 - Maitrise des enregistrements qualite"],
                ],
            ),
        ],
        "revisions": [
            ("V6", "2025-02-10", "Delai d'auto-formation porte de 10 a 15 jours ouvres"),
            ("V5", "2024-04-22", "Ajout du seuil de 90 pour cent d'accuse de reception"),
            ("V4", "2023-01-30", "Revision periodique alignee sur 3 ans"),
        ],
    },
    {
        "ref": "PR-QA-MRD-009",
        "title": "Gestion des non-conformites et des actions correctives (CAPA)",
        "version": "V4",
        "effective": "2025-03-03",
        "dept": "Assurance Qualite",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Sarah Delaunay",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure definit le traitement des non-conformites detectees en interne "
                    "ou signalees par un client, ainsi que la conduite des plans d'action correctifs "
                    "et preventifs.",
                ],
            ),
            (
                "2. Classification",
                [
                    "Toute non-conformite est classee majeure ou mineure par le Responsable "
                    "Assurance Qualite dans les 2 jours ouvres suivant sa detection. Les criteres "
                    "de classification sont definis dans l'annexe AN-QA-MRD-000.",
                ],
            ),
            (
                "3. Information du client",
                [
                    "En cas de non-conformite majeure, le client concerne est informe dans un delai "
                    "maximum de 24 heures apres la classification. L'information est transmise par "
                    "ecrit et tracee dans le dossier de la non-conformite.",
                    "Pour une non-conformite mineure, l'information du client est realisee dans le "
                    "cadre du reporting mensuel.",
                ],
            ),
            (
                "4. Delais de cloture des plans d'action",
                [
                    {
                        "table": [
                            ["Classification", "Delai de cloture", "Validation"],
                            ["Non-conformite majeure", "45 jours calendaires", "Responsable AQ + Direction"],
                            ["Non-conformite mineure", "90 jours calendaires", "Responsable AQ"],
                            ["Observation", "Sans delai contraignant", "Pilote de processus"],
                        ]
                    },
                    "Tout depassement de delai fait l'objet d'une demande de prolongation motivee, "
                    "soumise au Responsable Assurance Qualite avant l'echeance initiale.",
                ],
            ),
            (
                "5. Verification d'efficacite",
                [
                    "L'efficacite de chaque action corrective est verifiee 3 mois apres la cloture "
                    "du plan d'action. Une action jugee inefficace donne lieu a la reouverture de la "
                    "non-conformite.",
                ],
            ),
            (
                "6. Escalade",
                [
                    "La survenue de plus de 2 non-conformites majeures sur un meme trimestre pour un "
                    "meme processus declenche une revue exceptionnelle par la Direction et "
                    "l'ouverture d'un audit interne cible selon PR-QA-MRD-010.",
                ],
            ),
            (
                "7. Non-conformites d'origine externe",
                [
                    "Une non-conformite peut etre ouverte a partir d'une reclamation client "
                    "qualifiee selon PR-CLI-MRD-013, d'un ecart releve lors d'un audit fournisseur "
                    "conduit selon PR-ACH-MRD-007, ou d'une anomalie detectee lors d'une revue de "
                    "pistes d'audit selon SOP-QA-MRD-015. Le circuit de classification et de "
                    "cloture reste identique quelle que soit son origine.",
                ],
            ),
            (
                "8. Documents associes",
                [
                    ["PR-QA-MRD-010 - Programme d'audits internes"],
                    ["PR-CLI-MRD-013 - Gestion des reclamations clients"],
                    ["PR-QA-MRD-011 - Revue de direction"],
                ],
            ),
        ],
        "revisions": [
            ("V4", "2025-03-03", "Delai de cloture majeur ramene de 60 a 45 jours calendaires"),
            ("V3", "2024-02-19", "Ajout de la verification d'efficacite a 3 mois"),
            ("V2", "2022-11-08", "Ajout du critere d'escalade trimestriel"),
        ],
    },
    {
        "ref": "PR-QA-MRD-010",
        "title": "Programme d'audits internes",
        "version": "V3",
        "effective": "2024-11-18",
        "dept": "Assurance Qualite",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Nadia Bouchard",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit la planification, la realisation et le suivi des audits "
                    "internes du systeme qualite de Meridian Labs.",
                ],
            ),
            (
                "2. Programme annuel",
                [
                    "Un programme d'audit annuel est etabli par le Responsable Assurance Qualite "
                    "avant le 30 novembre de l'annee precedente. Chaque processus critique est "
                    "audite au moins une fois tous les 2 ans.",
                ],
            ),
            (
                "3. Prerequis de l'auditeur interne",
                [
                    "Pour etre habilite auditeur interne, un collaborateur doit satisfaire "
                    "l'ensemble des prerequis suivants :",
                    [
                        "avoir suivi une formation a l'audit conforme a la norme ISO 19011 ;",
                        "avoir participe a 2 audits en observation aupres d'un auditeur habilite ;",
                        "etre independant du processus audite, sans lien hierarchique avec les audites ;",
                        "avoir une anciennete minimale de 12 mois dans l'organisation.",
                    ],
                    "L'habilitation d'auditeur interne est valable 3 ans. Son maintien est "
                    "conditionne a la realisation d'au moins un audit par an.",
                ],
            ),
            (
                "4. Rapport d'audit",
                [
                    "Le rapport d'audit est diffuse aux audites et au Responsable Assurance Qualite "
                    "dans un delai de 10 jours ouvres apres la reunion de cloture. Les ecarts releves "
                    "sont traites selon la procedure PR-QA-MRD-009.",
                ],
            ),
            (
                "5. Types d'audits",
                [
                    "Le programme annuel distingue les audits de processus internes, les audits "
                    "documentaires cibles declenches par une non-conformite recurrente, et les audits "
                    "fournisseurs realises conjointement avec l'equipe Achats selon PR-ACH-MRD-007. "
                    "Les resultats consolides sont presentes en revue de direction selon "
                    "PR-QA-MRD-011.",
                ],
            ),
            (
                "6. Documents associes",
                [
                    ["PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)"],
                    ["PR-ACH-MRD-007 - Qualification et evaluation des fournisseurs"],
                    ["PR-QA-MRD-011 - Revue de direction"],
                ],
            ),
        ],
        "revisions": [
            ("V3", "2024-11-18", "Prerequis porte de 1 a 2 audits en observation"),
            ("V2", "2023-05-12", "Ajout du delai de diffusion du rapport"),
        ],
    },
    {
        "ref": "PR-MI-MRD-001",
        "title": "Traitement des demandes d'information medicale",
        "version": "V5",
        "effective": "2025-01-27",
        "dept": "Information Medicale",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Dr Helene Marchetti",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit la reception, la qualification et la reponse aux "
                    "demandes d'information medicale adressees a Meridian Labs par les "
                    "professionnels de sante et les patients.",
                ],
            ),
            (
                "2. Canaux et disponibilite",
                [
                    "Le service d'information medicale est joignable par telephone, courriel et "
                    "formulaire web. Une astreinte est assuree 24 heures sur 24 et 7 jours sur 7 "
                    "pour les demandes qualifiees d'urgentes.",
                ],
            ),
            (
                "3. Indicateurs de performance",
                [
                    "Les indicateurs de performance du processus d'information medicale sont revus "
                    "mensuellement en comite qualite :",
                    {
                        "table": [
                            ["Indicateur", "Cible", "Frequence"],
                            ["Taux de reponse sous 24 heures", "superieur ou egal a 95 pour cent", "Mensuelle"],
                            ["Delai moyen de reponse", "inferieur ou egal a 8 heures", "Mensuelle"],
                            ["Taux de reclamation", "inferieur a 2 pour cent", "Mensuelle"],
                            ["Taux de tracabilite des demandes", "100 pour cent", "Mensuelle"],
                            ["Satisfaction declaree des demandeurs", "superieur ou egal a 4,2 sur 5", "Trimestrielle"],
                        ]
                    },
                ],
            ),
            (
                "4. Articulation avec la pharmacovigilance",
                [
                    "Toute demande contenant la description d'un effet indesirable est transmise "
                    "sans delai au service de pharmacovigilance et traitee selon PR-PV-MRD-002.",
                ],
            ),
            (
                "5. Base de connaissances",
                [
                    "Les charges d'information medicale s'appuient en priorite sur la base de "
                    "connaissances decrite dans PR-MI-MRD-023 pour les demandes recurrentes. Une "
                    "demande non couverte par une fiche existante est traitee individuellement et "
                    "peut donner lieu a la creation d'une nouvelle fiche.",
                ],
            ),
            (
                "6. Documents associes",
                [
                    ["PR-PV-MRD-002 - Pharmacovigilance - reception et transmission des cas"],
                    ["PR-MI-MRD-023 - Base de connaissances medicale et FAQ"],
                    ["PR-CLI-MRD-013 - Gestion des reclamations clients"],
                ],
            ),
        ],
        "revisions": [
            ("V5", "2025-01-27", "Ajout de l'indicateur de satisfaction declaree"),
            ("V4", "2024-03-15", "Cible de reponse sous 24 heures portee a 95 pour cent"),
        ],
    },
    {
        "ref": "PR-PV-MRD-002",
        "title": "Pharmacovigilance - reception et transmission des cas",
        "version": "V4",
        "effective": "2025-04-07",
        "dept": "Pharmacovigilance",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Dr Helene Marchetti",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit le circuit de traitement des cas de pharmacovigilance, "
                    "de leur reception jusqu'a leur transmission aux autorites competentes.",
                ],
            ),
            (
                "2. Accuse de reception",
                [
                    "Tout signalement recu fait l'objet d'un accuse de reception adresse au "
                    "notificateur dans un delai de 2 jours ouvres.",
                ],
            ),
            (
                "3. Delais de transmission",
                [
                    {
                        "table": [
                            ["Type de cas", "Delai de transmission", "Destinataire"],
                            ["Cas grave", "15 jours calendaires", "Autorite competente"],
                            ["Cas non grave", "90 jours calendaires", "Autorite competente"],
                            ["Cas grave et inattendu", "7 jours calendaires", "Autorite competente"],
                        ]
                    },
                    "Le delai court a compter de la date de premiere reception de l'information "
                    "par tout collaborateur de Meridian Labs, et non a compter de sa qualification.",
                ],
            ),
            (
                "4. Codification",
                [
                    "Les evenements sont codifies avec le dictionnaire MedDRA version 27.0. La mise "
                    "a jour de la version du dictionnaire fait l'objet d'une analyse d'impact "
                    "documentee.",
                ],
            ),
            (
                "5. Veille reglementaire et signaux",
                [
                    "Les cas traites alimentent la base de donnees interne surveillee dans le cadre "
                    "de la veille reglementaire et de la detection de signaux decrite dans "
                    "SOP-PV-MRD-019. Un signal confirme est escalade selon les delais de transmission "
                    "definis dans la presente procedure.",
                ],
            ),
            (
                "6. Documents associes",
                [
                    ["SOP-PV-MRD-019 - Regulatory Watch and Signal Detection"],
                    ["PR-MI-MRD-001 - Traitement des demandes d'information medicale"],
                ],
            ),
        ],
        "revisions": [
            ("V4", "2025-04-07", "Passage a MedDRA version 27.0"),
            ("V3", "2024-06-11", "Ajout du delai de 7 jours pour les cas graves et inattendus"),
        ],
    },
    {
        "ref": "PR-EXM-MRD-003",
        "title": "Securite des systemes d'information et des postes de travail",
        "version": "V7",
        "effective": "2025-05-20",
        "dept": "Exploitation et Maintenance",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Julien Kessler",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure definit les mesures de securite applicables aux postes de "
                    "travail et aux serveurs exploites par Meridian Labs.",
                ],
            ),
            (
                "2. Protection antivirale",
                [
                    "L'ensemble du parc informatique est protege par la solution antivirus "
                    "Bitdefender GravityZone, administree de facon centralisee par l'equipe "
                    "Exploitation. Les signatures sont mises a jour automatiquement toutes les "
                    "4 heures. Aucun poste ne peut se connecter au reseau interne sans agent actif.",
                ],
            ),
            (
                "3. Politique de mot de passe",
                [
                    [
                        "longueur minimale de 14 caracteres ;",
                        "rotation obligatoire tous les 12 mois ;",
                        "authentification multifacteur obligatoire pour tous les acces distants ;",
                        "verrouillage automatique de la session apres 5 minutes d'inactivite ;",
                        "blocage du compte apres 5 tentatives infructueuses.",
                    ]
                ],
            ),
            (
                "4. Sauvegardes",
                [
                    "Les donnees de production font l'objet d'une sauvegarde quotidienne "
                    "incrementale et d'une sauvegarde complete hebdomadaire. La retention des "
                    "sauvegardes est de 35 jours. Un test de restauration est realise chaque "
                    "trimestre et son resultat est consigne.",
                ],
            ),
            (
                "5. Conservation des dossiers de formation des collaborateurs",
                [
                    "Les dossiers individuels de formation et d'habilitation des collaborateurs "
                    "sont conserves 5 ans a compter de la date de depart du collaborateur. Cette "
                    "regle est distincte de la conservation des documents qualite definie dans "
                    "PR-QA-MRD-001.",
                ],
            ),
            (
                "6. Incidents de securite",
                [
                    "Toute anomalie de securite constatee sur un poste de travail ou un serveur est "
                    "traitee selon la procedure PR-ITS-MRD-016, y compris lorsqu'elle est detectee "
                    "par l'agent antivirus ou lors d'un test de restauration.",
                ],
            ),
            (
                "7. Documents associes",
                [
                    ["PR-ITS-MRD-016 - Gestion des incidents de securite informatique"],
                    ["PR-EXM-MRD-014 - Plan de continuite d'activite"],
                    ["PR-ITS-MRD-004 - Gestion des acces et des habilitations"],
                ],
            ),
        ],
        "revisions": [
            ("V7", "2025-05-20", "Longueur minimale de mot de passe portee a 14 caracteres"),
            ("V6", "2024-08-30", "Migration de l'antivirus vers Bitdefender GravityZone"),
            ("V5", "2023-10-02", "Ajout du test de restauration trimestriel"),
        ],
    },
    {
        "ref": "PR-ITS-MRD-004",
        "title": "Gestion des acces et des habilitations",
        "version": "V3",
        "effective": "2024-09-16",
        "dept": "Systemes d'Information",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Julien Kessler",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit l'attribution, la revue et la suppression des acces aux "
                    "applications et aux infrastructures de Meridian Labs.",
                ],
            ),
            (
                "2. Principes",
                [
                    [
                        "principe du moindre privilege applique a tous les comptes ;",
                        "comptes d'administration strictement nominatifs, sans compte partage ;",
                        "separation des environnements de production et de recette.",
                    ]
                ],
            ),
            (
                "3. Revue des habilitations",
                [
                    "Une revue complete des habilitations est realisee tous les 6 mois par les "
                    "proprietaires d'application, sous le controle du RSSI. Les ecarts constates "
                    "sont corriges sous 15 jours ouvres.",
                ],
            ),
            (
                "4. Depart d'un collaborateur",
                [
                    "Les acces d'un collaborateur quittant l'organisation sont supprimes dans un "
                    "delai maximum de 24 heures apres son depart effectif. Le service Ressources "
                    "Humaines notifie l'equipe Systemes d'Information au moins 5 jours ouvres avant "
                    "la date de depart lorsque celle-ci est connue.",
                ],
            ),
            (
                "5. Acces exceptionnel",
                [
                    "Un acces exceptionnel peut etre accorde pour une duree maximale de 72 heures, "
                    "sur validation du RSSI. Il est automatiquement revoque a echeance et fait "
                    "l'objet d'une trace dans le journal d'audit.",
                ],
            ),
            (
                "6. Comptes de service",
                [
                    "Un compte de service utilise par une integration technique est associe a un "
                    "proprietaire nominatif responsable de sa revue. Il ne peut jamais etre utilise "
                    "pour une connexion interactive et suit la meme frequence de revue que les "
                    "comptes individuels.",
                ],
            ),
            (
                "7. Documents associes",
                [
                    ["PR-ITS-MRD-016 - Gestion des incidents de securite informatique"],
                    ["PR-RH-MRD-018 - Integration des nouveaux collaborateurs"],
                ],
            ),
        ],
        "revisions": [
            ("V3", "2024-09-16", "Revue des habilitations portee de 12 a 6 mois"),
            ("V2", "2023-04-25", "Ajout de la procedure d'acces exceptionnel"),
        ],
    },
    {
        "ref": "TEAM-ITS-MRD-001",
        "title": "Organisation de l'equipe Systemes d'Information",
        "version": "V8",
        "effective": "2025-06-02",
        "dept": "Systemes d'Information",
        "doc_type": "Fiche d'organisation",
        "lang": "fr",
        "author": "Julien Kessler",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Ce document decrit la composition, les roles et les responsabilites de "
                    "l'equipe Systemes d'Information de Meridian Labs.",
                ],
            ),
            (
                "2. Composition de l'equipe",
                [
                    "L'equipe compte 9 collaborateurs au 2 juin 2025 :",
                    {
                        "table": [
                            ["Role", "Titulaire", "Suppleant"],
                            ["Directeur des Systemes d'Information", "Julien Kessler", "Theo Mbala"],
                            ["Lead Developer", "Camille Renard", "Ines Bouziane"],
                            ["Developpeur backend", "Ines Bouziane", "-"],
                            ["Developpeur frontend", "Lucas Ferreira", "-"],
                            ["Responsable Infrastructure", "Theo Mbala", "Lucas Ferreira"],
                            ["Administrateur base de donnees", "Priya Raghavan", "Theo Mbala"],
                            ["Delegue a la Protection des Donnees", "Anais Fournier", "-"],
                            ["Technicien support niveau 2", "Yassine Haddad", "-"],
                            ["Alternant developpement", "Emma Lindqvist", "-"],
                        ]
                    },
                    "Le role de RSSI est porte par Julien Kessler en complement de la fonction de "
                    "Directeur des Systemes d'Information.",
                ],
            ),
            (
                "3. Astreinte",
                [
                    "Une astreinte technique hebdomadaire est assuree par rotation entre les "
                    "membres de l'equipe Infrastructure. Le planning est publie le 25 de chaque "
                    "mois pour le mois suivant.",
                ],
            ),
            (
                "4. Documents associes",
                [
                    ["PR-ITS-MRD-004 - Gestion des acces et des habilitations"],
                    ["PR-ITS-MRD-016 - Gestion des incidents de securite informatique"],
                    ["DR_RISKA-ITS-MRD-005 - Analyse de risques de la plateforme MeridianCore"],
                ],
            ),
        ],
        "revisions": [
            ("V8", "2025-06-02", "Arrivee de Emma Lindqvist en alternance, effectif porte a 9"),
            ("V7", "2024-12-09", "Camille Renard nommee Lead Developer"),
            ("V6", "2024-05-14", "Creation du poste d'administrateur base de donnees"),
        ],
    },
    {
        "ref": "DR_RISKA-ITS-MRD-005",
        "title": "Analyse de risques de la plateforme MeridianCore",
        "version": "V2",
        "effective": "2025-03-12",
        "dept": "Systemes d'Information",
        "doc_type": "Dossier de risques",
        "lang": "fr",
        "author": "Julien Kessler",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet et perimetre",
                [
                    "Ce dossier presente l'analyse de risques de la plateforme MeridianCore, "
                    "socle applicatif hebergeant les modules qualite, information medicale et "
                    "pharmacovigilance. L'analyse a ete conduite le 12 mars 2025.",
                ],
            ),
            (
                "2. Methode",
                [
                    "L'analyse s'appuie sur la methode EBIOS Risk Manager. La criticite est "
                    "calculee comme le produit de la vraisemblance (1 a 4) et de la gravite (1 a 4), "
                    "soit une echelle de 1 a 16.",
                ],
            ),
            (
                "3. Synthese des risques",
                [
                    {
                        "table": [
                            ["Categorie", "Nombre"],
                            ["Risques identifies", "29"],
                            ["Risques majeurs", "3"],
                            ["Risques non bloquants", "7"],
                            ["Risques acceptes sous controle", "19"],
                        ]
                    },
                    "Le risque de criticite la plus elevee est la perte de disponibilite de la base "
                    "de donnees principale, evalue a une criticite de 16. Les mesures de reduction "
                    "associees sont la replication synchrone et le test de restauration trimestriel "
                    "decrit dans PR-EXM-MRD-003.",
                ],
            ),
            (
                "4. Objectifs de reprise",
                [
                    "Les objectifs de reprise retenus pour MeridianCore sont un RTO de 4 heures et "
                    "un RPO de 1 heure. Ces objectifs sont contractualises avec les directions "
                    "metier et verifies lors de l'exercice annuel de continuite d'activite.",
                ],
            ),
            (
                "5. Revision",
                [
                    "Cette analyse de risques est revisee annuellement ou lors de tout changement "
                    "majeur d'architecture.",
                ],
            ),
            (
                "6. Documents associes",
                [
                    ["PR-EXM-MRD-014 - Plan de continuite d'activite"],
                    ["PR-EXM-MRD-003 - Securite des systemes d'information et des postes de travail"],
                    ["PR-ITS-MRD-016 - Gestion des incidents de securite informatique"],
                ],
            ),
        ],
        "revisions": [
            ("V2", "2025-03-12", "Reevaluation apres migration de l'hebergement, 29 risques identifies"),
            ("V1", "2023-07-19", "Creation, 24 risques identifies"),
        ],
    },
    {
        "ref": "PR-RH-MRD-006",
        "title": "Formation et habilitation du personnel",
        "version": "V3",
        "effective": "2024-10-07",
        "dept": "Ressources Humaines",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Nadia Bouchard",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit l'elaboration du plan de formation, la realisation des "
                    "actions de formation et l'habilitation des collaborateurs aux activites "
                    "reglementees.",
                ],
            ),
            (
                "2. Plan de formation",
                [
                    "Un plan de formation annuel est etabli avant le 31 janvier de chaque annee. "
                    "Chaque collaborateur beneficie d'un volume minimal de 21 heures de formation "
                    "par an, dont au moins 7 heures consacrees au systeme qualite.",
                ],
            ),
            (
                "3. Evaluation",
                [
                    "L'evaluation a chaud est realisee dans les 7 jours suivant la formation. "
                    "L'evaluation a froid, mesurant le transfert en situation de travail, est "
                    "realisee 6 mois apres la formation.",
                ],
            ),
            (
                "4. Habilitation",
                [
                    "Une habilitation a une activite reglementee est valable 2 ans. Son "
                    "renouvellement est conditionne a une evaluation pratique realisee par le "
                    "manager et validee par l'Assurance Qualite.",
                ],
            ),
            (
                "5. Types de formation",
                [
                    "Le plan de formation distingue la formation initiale dispensee dans le cadre de "
                    "l'integration decrite dans PR-RH-MRD-018, la formation continue liee au poste, "
                    "et la formation reglementaire obligatoire (systeme qualite, securite des "
                    "systemes d'information, pharmacovigilance selon le poste occupe).",
                ],
            ),
            (
                "6. Documents associes",
                [
                    ["PR-RH-MRD-018 - Integration des nouveaux collaborateurs"],
                    ["PR-QA-MRD-010 - Programme d'audits internes"],
                ],
            ),
        ],
        "revisions": [
            ("V3", "2024-10-07", "Volume annuel porte de 14 a 21 heures"),
            ("V2", "2023-02-13", "Ajout de l'evaluation a froid a 6 mois"),
        ],
    },
    {
        "ref": "SOP-QA-MRD-015",
        "title": "Data Integrity and ALCOA+ Controls",
        "version": "V2",
        "effective": "2025-04-28",
        "dept": "Quality Assurance",
        "doc_type": "Standard Operating Procedure",
        "lang": "en",
        "author": "Sarah Delaunay",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Purpose",
                [
                    "This standard operating procedure defines the data integrity controls applied "
                    "to electronic records produced and maintained by Meridian Labs across its "
                    "quality, medical information and pharmacovigilance systems.",
                ],
            ),
            (
                "2. ALCOA+ principles",
                [
                    "All electronic records must be Attributable, Legible, Contemporaneous, "
                    "Original and Accurate, and in addition Complete, Consistent, Enduring and "
                    "Available throughout the retention period.",
                ],
            ),
            (
                "3. Audit trail review",
                [
                    "Audit trails of GxP-relevant systems are reviewed on a monthly basis by the "
                    "system owner. Any anomaly detected during the review is raised as a "
                    "non-conformity under PR-QA-MRD-009.",
                ],
            ),
            (
                "4. Electronic signatures",
                [
                    "Electronic signatures comply with 21 CFR Part 11. Each signature captures the "
                    "signer identity, the date and time in UTC, and the meaning of the signature. "
                    "Signature components are never reused or reassigned to another individual.",
                ],
            ),
            (
                "5. Record retention",
                [
                    "GxP electronic records are retained for 15 years from the date of creation. "
                    "Retention is enforced technically through storage lifecycle policies and "
                    "verified during the annual data integrity self-inspection.",
                ],
            ),
            (
                "6. Training",
                [
                    "All staff handling GxP electronic records complete data integrity training as "
                    "part of the initial training path described in PR-RH-MRD-018, and a refresher "
                    "every 2 years alongside the training plan defined in PR-RH-MRD-006.",
                ],
            ),
            (
                "7. Related documents",
                [
                    ["PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)"],
                    ["PR-RH-MRD-006 - Formation et habilitation du personnel"],
                ],
            ),
        ],
        "revisions": [
            ("V2", "2025-04-28", "Audit trail review frequency changed from quarterly to monthly"),
            ("V1", "2023-11-06", "Initial release"),
        ],
    },
    {
        "ref": "FT-EXM-MRD-008",
        "title": "Fiche technique - prerequis du poste client MeridianCore",
        "version": "V4",
        "effective": "2025-05-05",
        "dept": "Exploitation et Maintenance",
        "doc_type": "Fiche technique",
        "lang": "fr",
        "author": "Theo Mbala",
        "approver": "Julien Kessler",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette fiche technique precise les caracteristiques minimales requises pour "
                    "l'utilisation de la plateforme MeridianCore sur un poste client.",
                ],
            ),
            (
                "2. Caracteristiques minimales requises",
                [
                    {
                        "table": [
                            ["Element", "Minimum requis", "Recommande"],
                            ["Memoire vive", "16 Go", "32 Go"],
                            ["Stockage disponible", "500 Go SSD", "1 To SSD"],
                            ["Systeme d'exploitation", "Windows 11 22H2", "Windows 11 24H2"],
                            ["Navigateur", "Chrome ou Edge, derniere version -1", "Derniere version"],
                            ["Bande passante descendante", "10 Mbit/s", "50 Mbit/s"],
                            ["Resolution ecran", "1920 x 1080", "2560 x 1440"],
                        ]
                    }
                ],
            ),
            (
                "3. Postes non conformes",
                [
                    "Un poste ne respectant pas les caracteristiques minimales ne peut pas etre "
                    "raccorde a MeridianCore. Une derogation temporaire de 30 jours peut etre "
                    "accordee par l'equipe Exploitation dans l'attente d'un renouvellement de "
                    "materiel.",
                ],
            ),
            (
                "4. Configuration reseau",
                [
                    "Le poste client doit pouvoir joindre les domaines de la plateforme MeridianCore "
                    "au travers du proxy d'entreprise, sans inspection SSL sur ces domaines, "
                    "conformement aux exceptions definies par l'equipe Infrastructure.",
                ],
            ),
            (
                "5. Documents associes",
                [
                    ["PR-EXM-MRD-003 - Securite des systemes d'information et des postes de travail"],
                ],
            ),
        ],
        "revisions": [
            ("V4", "2025-05-05", "Memoire vive minimale portee de 8 a 16 Go"),
            ("V3", "2024-07-01", "Passage a Windows 11 22H2 comme socle minimal"),
        ],
    },
    {
        "ref": "PR-ACH-MRD-007",
        "title": "Qualification et evaluation des fournisseurs",
        "version": "V3",
        "effective": "2025-02-24",
        "dept": "Achats",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Karim Belaidi",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet et domaine d'application",
                [
                    "Cette procedure decrit la qualification initiale et l'evaluation continue des "
                    "fournisseurs et prestataires de Meridian Labs susceptibles d'avoir un impact sur "
                    "la qualite du service rendu aux clients ou sur la conformite reglementaire.",
                ],
            ),
            (
                "2. Classification des fournisseurs",
                [
                    "Chaque fournisseur est classe des sa premiere consultation selon son impact "
                    "potentiel sur les processus qualite, information medicale ou pharmacovigilance :",
                    {
                        "table": [
                            ["Classe", "Exemple de perimetre", "Frequence de reevaluation"],
                            ["Critique", "Hebergement, sous-traitance MedDRA, archivage electronique", "Annuelle"],
                            ["Standard", "Fournitures bureautiques, prestations ponctuelles", "Tous les 3 ans"],
                            ["Non classifie", "Achats sans impact sur les processus reglementes", "Sur demande"],
                        ]
                    },
                ],
            ),
            (
                "3. Qualification initiale",
                [
                    "Un fournisseur critique ne peut etre retenu qu'apres qualification initiale, "
                    "comprenant l'analyse de son questionnaire qualite, la revue de ses certifications "
                    "(ISO 27001, ISO 9001 selon le perimetre) et, si necessaire, un audit documentaire "
                    "realise par l'equipe Achats avec l'appui de l'Assurance Qualite.",
                    "Le dossier de qualification est archive selon les regles de PR-QA-MRD-017 et "
                    "reste opposable pendant toute la duree de la relation contractuelle.",
                ],
            ),
            (
                "4. Evaluation annuelle",
                [
                    "Chaque fournisseur critique fait l'objet d'une notation annuelle sur 3 criteres : "
                    "qualite de service, respect des delais contractuels, et reactivite en cas "
                    "d'incident.",
                    {
                        "table": [
                            ["Score", "Interpretation", "Action"],
                            ["Superieur ou egal a 8 sur 10", "Fournisseur performant", "Reconduction sans reserve"],
                            ["Entre 5 et 7,9 sur 10", "Points d'amelioration identifies", "Plan d'action fournisseur sous 60 jours"],
                            ["Inferieur a 5 sur 10", "Performance non satisfaisante", "Revue de la relation en comite Achats"],
                        ]
                    },
                ],
            ),
            (
                "5. Clauses contractuelles obligatoires",
                [
                    "Tout contrat avec un fournisseur critique integre une clause d'audit, une clause "
                    "de notification des incidents de securite sous 48 heures, et une clause de "
                    "reversibilite garantissant la restitution des donnees en fin de contrat.",
                ],
            ),
            (
                "6. Suspension et retrait",
                [
                    "Un fournisseur critique peut etre suspendu de la liste des fournisseurs qualifies "
                    "en cas de non-conformite majeure averee ou de score annuel inferieur a 5 sur 10 "
                    "deux annees consecutives. La decision est validee en revue de direction "
                    "conformement a PR-QA-MRD-011.",
                ],
            ),
            (
                "7. Documents associes",
                [
                    ["PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)"],
                    ["PR-QA-MRD-011 - Revue de direction"],
                    ["PR-QA-MRD-017 - Maitrise des enregistrements qualite"],
                ],
            ),
        ],
        "revisions": [
            ("V3", "2025-02-24", "Ajout de la clause de notification des incidents sous 48 heures"),
            ("V2", "2023-10-11", "Introduction de la notation annuelle sur 3 criteres"),
            ("V1", "2022-06-01", "Creation"),
        ],
    },
    {
        "ref": "PR-CLI-MRD-013",
        "title": "Gestion des reclamations clients",
        "version": "V4",
        "effective": "2025-01-08",
        "dept": "Relation Client",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Claire Dumont",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit la reception, la qualification et le traitement des "
                    "reclamations formulees par les clients de Meridian Labs concernant la qualite du "
                    "service rendu, a l'exclusion des signalements de pharmacovigilance qui relevent de "
                    "PR-PV-MRD-002.",
                ],
            ),
            (
                "2. Canaux de reception",
                [
                    "Les reclamations sont recues par courriel dedie, par le formulaire du portail "
                    "client, ou verbalement aupres d'un interlocuteur Meridian Labs. Toute reclamation "
                    "verbale est consignee par ecrit par son destinataire dans un delai d'un jour "
                    "ouvre.",
                ],
            ),
            (
                "3. Qualification et accuse de reception",
                [
                    "Chaque reclamation est qualifiee des sa reception selon sa criticite :",
                    {
                        "table": [
                            ["Criticite", "Exemple", "Accuse de reception"],
                            ["Critique", "Indisponibilite prolongee, erreur affectant la securite du patient", "4 heures"],
                            ["Standard", "Erreur documentaire, delai de reponse depasse", "2 jours ouvres"],
                            ["Mineure", "Remarque d'amelioration, question de comprehension", "5 jours ouvres"],
                        ]
                    },
                ],
            ),
            (
                "4. Investigation",
                [
                    "Toute reclamation critique ou standard donne lieu a l'ouverture d'une "
                    "non-conformite dans les conditions de PR-QA-MRD-009. L'investigation identifie la "
                    "cause racine et propose, le cas echeant, une action corrective.",
                    "Une reclamation mineure peut etre cloturee directement par le charge de relation "
                    "client, avec traçabilite dans le registre des reclamations.",
                ],
            ),
            (
                "5. Delai de reponse au client",
                [
                    "La reponse formelle au client, incluant le resultat de l'investigation et les "
                    "actions engagees, est transmise sous 10 jours ouvres pour une reclamation "
                    "critique et sous 20 jours ouvres pour une reclamation standard.",
                ],
            ),
            (
                "6. Indicateurs de suivi",
                [
                    "Le taux de reclamations cloturees dans les delais et le taux de reclamations "
                    "recurrentes sur un meme motif sont revus mensuellement et presentes en revue de "
                    "direction selon PR-QA-MRD-011.",
                ],
            ),
            (
                "7. Documents associes",
                [
                    ["PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)"],
                    ["PR-PV-MRD-002 - Pharmacovigilance - reception et transmission des cas"],
                    ["PR-QA-MRD-011 - Revue de direction"],
                ],
            ),
        ],
        "revisions": [
            ("V4", "2025-01-08", "Delai d'accuse de reception critique ramene de 8 a 4 heures"),
            ("V3", "2023-09-19", "Ajout du seuil de reclamations recurrentes"),
        ],
    },
    {
        "ref": "PR-QA-MRD-011",
        "title": "Revue de direction",
        "version": "V2",
        "effective": "2025-02-03",
        "dept": "Assurance Qualite",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Sarah Delaunay",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit l'organisation de la revue de direction du systeme "
                    "qualite de Meridian Labs, instance au cours de laquelle la Direction evalue "
                    "l'efficacite du systeme et arbitre les priorites qualite.",
                ],
            ),
            (
                "2. Frequence et participants",
                [
                    "La revue de direction se tient a frequence semestrielle. Elle reunit la "
                    "Direction, le Responsable Assurance Qualite, et les pilotes des processus "
                    "concernes (Information Medicale, Pharmacovigilance, Systemes d'Information, "
                    "Ressources Humaines, Achats, Relation Client).",
                ],
            ),
            (
                "3. Elements d'entree",
                [
                    "La revue de direction examine a minima les elements suivants :",
                    [
                        "bilan des non-conformites et des plans d'action CAPA en cours ;",
                        "resultats du programme d'audits internes ;",
                        "indicateurs de performance des processus (information medicale, "
                        "reclamations clients, pharmacovigilance) ;",
                        "etat des risques identifies dans les analyses de risques en vigueur ;",
                        "bilan du plan de formation et des habilitations ;",
                        "evaluation annuelle des fournisseurs critiques.",
                    ],
                ],
            ),
            (
                "4. Elements de sortie",
                [
                    "La revue de direction produit un plan d'actions priorise, avec un responsable et "
                    "une echeance pour chaque action retenue. Les decisions relatives aux ressources "
                    "necessaires a l'amelioration du systeme qualite sont formalisees dans le "
                    "compte-rendu.",
                ],
            ),
            (
                "5. Diffusion",
                [
                    "Le compte-rendu de revue de direction est diffuse aux participants et aux "
                    "pilotes de processus sous 15 jours ouvres suivant la reunion. Le suivi des "
                    "actions est verifie lors de la revue suivante.",
                ],
            ),
            (
                "6. Documents associes",
                [
                    ["PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)"],
                    ["PR-QA-MRD-010 - Programme d'audits internes"],
                    ["PR-ACH-MRD-007 - Qualification et evaluation des fournisseurs"],
                ],
            ),
        ],
        "revisions": [
            ("V2", "2025-02-03", "Frequence portee d'annuelle a semestrielle"),
            ("V1", "2022-09-15", "Creation"),
        ],
    },
    {
        "ref": "PR-QA-MRD-012",
        "title": "Maitrise du changement",
        "version": "V2",
        "effective": "2025-03-19",
        "dept": "Assurance Qualite",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Sarah Delaunay",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet et domaine d'application",
                [
                    "Cette procedure decrit l'analyse d'impact et le circuit de validation applicables "
                    "a tout changement affectant les processus, les systemes ou l'organisation de "
                    "Meridian Labs susceptible d'avoir un impact sur la qualite ou la conformite.",
                ],
            ),
            (
                "2. Classification des changements",
                [
                    {
                        "table": [
                            ["Classe", "Exemple", "Validation requise"],
                            ["Mineur", "Correction documentaire, ajustement d'indicateur", "Pilote de processus"],
                            ["Majeur", "Evolution de procedure, changement de fournisseur critique", "Responsable AQ + pilote"],
                            ["Urgent", "Correctif de securite, contournement d'incident", "RSSI ou Responsable AQ a posteriori"],
                        ]
                    }
                ],
            ),
            (
                "3. Analyse d'impact",
                [
                    "Tout changement majeur fait l'objet d'une analyse d'impact prealable couvrant les "
                    "processus impactes, les risques induits et les documents a mettre a jour. "
                    "L'analyse est jointe a la demande de changement.",
                ],
            ),
            (
                "4. Circuit de validation",
                [
                    "Un changement mineur est mis en oeuvre directement par le pilote de processus, "
                    "avec information de l'Assurance Qualite. Un changement majeur requiert la "
                    "validation ecrite du Responsable Assurance Qualite avant sa mise en oeuvre. Un "
                    "changement urgent peut etre applique immediatement par le RSSI ou le Responsable "
                    "Assurance Qualite, sous reserve d'une validation formelle a posteriori sous 5 "
                    "jours ouvres.",
                ],
            ),
            (
                "5. Verification post-implementation",
                [
                    "L'efficacite de tout changement majeur est verifiee dans un delai de 60 jours "
                    "calendaires apres sa mise en oeuvre. Une verification defavorable donne lieu a "
                    "l'ouverture d'une non-conformite selon PR-QA-MRD-009.",
                ],
            ),
            (
                "6. Documents associes",
                [
                    ["PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)"],
                    ["PR-QA-MRD-011 - Revue de direction"],
                    ["PR-ITS-MRD-016 - Gestion des incidents de securite informatique"],
                ],
            ),
        ],
        "revisions": [
            ("V2", "2025-03-19", "Ajout de la classe de changement urgent"),
            ("V1", "2023-01-09", "Creation"),
        ],
    },
    {
        "ref": "PR-QA-MRD-017",
        "title": "Maitrise des enregistrements qualite",
        "version": "V2",
        "effective": "2024-12-02",
        "dept": "Assurance Qualite",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Nadia Bouchard",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit l'identification, la conservation et la destruction des "
                    "enregistrements qualite de Meridian Labs, par opposition aux documents "
                    "normatifs dont le cycle de vie est decrit dans PR-QA-MRD-001.",
                ],
            ),
            (
                "2. Identification et classification",
                [
                    "Un enregistrement qualite est toute preuve objective produite par l'execution "
                    "d'un processus : compte-rendu d'audit, fiche de non-conformite, dossier de "
                    "qualification fournisseur, releve d'indicateur, accuse de reception de "
                    "formation.",
                ],
            ),
            (
                "3. Modalites de conservation",
                [
                    "Les enregistrements qualite sont conserves sous forme electronique dans le "
                    "coffre-fort documentaire decrit dans PR-ITS-MRD-004, avec une sauvegarde "
                    "redondante conforme a PR-EXM-MRD-003. L'acces en lecture est ouvert a "
                    "l'Assurance Qualite et, sur habilitation, aux auditeurs externes.",
                ],
            ),
            (
                "4. Duree de conservation par type",
                [
                    {
                        "table": [
                            ["Type d'enregistrement", "Duree de conservation"],
                            ["Fiche de non-conformite et plan d'action CAPA", "10 ans"],
                            ["Compte-rendu d'audit interne", "10 ans"],
                            ["Dossier de qualification fournisseur", "Duree du contrat + 5 ans"],
                            ["Releve mensuel d'indicateurs", "5 ans"],
                            ["Accuse de reception de formation", "5 ans apres le depart du collaborateur"],
                        ]
                    }
                ],
            ),
            (
                "5. Destruction",
                [
                    "A l'echeance de sa duree de conservation, un enregistrement est detruit selon un "
                    "calendrier trimestriel valide par le Responsable Assurance Qualite. La "
                    "destruction est tracee dans un registre dedie, mentionnant la reference, la date "
                    "et le motif.",
                ],
            ),
            (
                "6. Documents associes",
                [
                    ["PR-QA-MRD-001 - Gestion documentaire du systeme qualite"],
                    ["PR-ITS-MRD-004 - Gestion des acces et des habilitations"],
                    ["PR-EXM-MRD-003 - Securite des systemes d'information et des postes de travail"],
                ],
            ),
        ],
        "revisions": [
            ("V2", "2024-12-02", "Ajout de la duree de conservation des dossiers fournisseurs"),
            ("V1", "2023-03-20", "Creation"),
        ],
    },
    {
        "ref": "PR-EXM-MRD-014",
        "title": "Plan de continuite d'activite",
        "version": "V3",
        "effective": "2025-04-14",
        "dept": "Exploitation et Maintenance",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Theo Mbala",
        "approver": "Julien Kessler",
        "sections": [
            (
                "1. Objet et perimetre",
                [
                    "Ce plan decrit l'organisation retenue par Meridian Labs pour assurer la "
                    "continuite des activites critiques en cas de sinistre affectant les locaux, les "
                    "systemes d'information, ou une part significative du personnel.",
                ],
            ),
            (
                "2. Scenarios de sinistre couverts",
                [
                    [
                        "indisponibilite du site principal d'hebergement ;",
                        "indisponibilite prolongee de la plateforme MeridianCore ;",
                        "indisponibilite des locaux administratifs ;",
                        "indisponibilite d'une part significative du personnel cle.",
                    ]
                ],
            ),
            (
                "3. Site de secours et bascule",
                [
                    "La plateforme MeridianCore beneficie d'une replication synchrone vers un site "
                    "d'hebergement secondaire. La bascule vers le site de secours est declenchee par "
                    "le Responsable Infrastructure sur decision du Directeur des Systemes "
                    "d'Information.",
                ],
            ),
            (
                "4. Objectifs de reprise",
                [
                    "Les objectifs de reprise par systeme sont alignes sur l'analyse de risques "
                    "DR_RISKA-ITS-MRD-005 :",
                    {
                        "table": [
                            ["Systeme", "RTO", "RPO"],
                            ["Plateforme MeridianCore", "4 heures", "1 heure"],
                            ["Messagerie et outils collaboratifs", "8 heures", "4 heures"],
                            ["Systemes administratifs internes", "48 heures", "24 heures"],
                        ]
                    },
                ],
            ),
            (
                "5. Exercice annuel",
                [
                    "Un exercice de continuite d'activite grandeur reelle est organise chaque annee, "
                    "incluant la bascule effective vers le site de secours. Le rapport d'exercice est "
                    "presente en revue de direction selon PR-QA-MRD-011.",
                ],
            ),
            (
                "6. Documents associes",
                [
                    ["DR_RISKA-ITS-MRD-005 - Analyse de risques de la plateforme MeridianCore"],
                    ["PR-EXM-MRD-003 - Securite des systemes d'information et des postes de travail"],
                    ["PR-QA-MRD-011 - Revue de direction"],
                ],
            ),
        ],
        "revisions": [
            ("V3", "2025-04-14", "Ajout des objectifs de reprise par systeme"),
            ("V2", "2023-11-28", "Passage a un exercice annuel grandeur reelle"),
        ],
    },
    {
        "ref": "PR-ITS-MRD-016",
        "title": "Gestion des incidents de securite informatique",
        "version": "V2",
        "effective": "2025-05-30",
        "dept": "Systemes d'Information",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Julien Kessler",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit la detection, la qualification et le traitement des "
                    "incidents de securite informatique susceptibles d'affecter la confidentialite, "
                    "l'integrite ou la disponibilite des systemes de Meridian Labs.",
                ],
            ),
            (
                "2. Classification des incidents",
                [
                    {
                        "table": [
                            ["Niveau", "Exemple", "Delai de prise en charge"],
                            ["Critique", "Compromission averee, fuite de donnees personnelles", "1 heure"],
                            ["Majeur", "Activite suspecte confirmee, indisponibilite de service", "4 heures"],
                            ["Mineur", "Tentative bloquee, anomalie sans impact confirme", "2 jours ouvres"],
                        ]
                    }
                ],
            ),
            (
                "3. Detection et remontee",
                [
                    "Tout collaborateur suspectant un incident de securite le signale sans delai a "
                    "l'equipe Systemes d'Information par le canal d'astreinte decrit dans "
                    "TEAM-ITS-MRD-001. Les alertes automatiques des outils de supervision sont "
                    "qualifiees par l'equipe Infrastructure dans le delai fixe par le niveau "
                    "presume.",
                ],
            ),
            (
                "4. Confinement et eradication",
                [
                    "Le RSSI coordonne les mesures de confinement (isolement reseau, revocation "
                    "d'acces, changement d'identifiants) puis l'eradication de la cause identifiee, "
                    "en s'appuyant si necessaire sur la procedure d'acces exceptionnel de "
                    "PR-ITS-MRD-004.",
                ],
            ),
            (
                "5. Notification",
                [
                    "Un incident critique impliquant des donnees a caractere personnel est notifie au "
                    "Delegue a la Protection des Donnees dans un delai de 24 heures, en vue d'une "
                    "eventuelle notification a l'autorite de controle dans le delai reglementaire de "
                    "72 heures.",
                ],
            ),
            (
                "6. Retour d'experience",
                [
                    "Tout incident critique ou majeur donne lieu a un retour d'experience formalise "
                    "sous 10 jours ouvres apres cloture, et a l'ouverture d'une non-conformite selon "
                    "PR-QA-MRD-009 lorsque l'incident revele une defaillance de controle.",
                ],
            ),
            (
                "7. Documents associes",
                [
                    ["PR-ITS-MRD-004 - Gestion des acces et des habilitations"],
                    ["PR-EXM-MRD-003 - Securite des systemes d'information et des postes de travail"],
                    ["PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)"],
                ],
            ),
        ],
        "revisions": [
            ("V2", "2025-05-30", "Ajout du delai de notification DPO a 24 heures"),
            ("V1", "2024-02-05", "Creation"),
        ],
    },
    {
        "ref": "PR-RH-MRD-018",
        "title": "Integration des nouveaux collaborateurs",
        "version": "V2",
        "effective": "2025-01-20",
        "dept": "Ressources Humaines",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Sophie Marchand",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit le parcours d'integration des nouveaux collaborateurs de "
                    "Meridian Labs, de leur arrivee jusqu'a la fin de leur periode d'essai.",
                ],
            ),
            (
                "2. Parcours d'integration",
                [
                    {
                        "table": [
                            ["Etape", "Contenu"],
                            ["Jour 1", "Accueil, remise du materiel, presentation de l'equipe"],
                            ["Semaine 1", "Formation initiale a la securite des systemes d'information"],
                            ["Mois 1", "Formation au systeme qualite et aux procedures du poste"],
                            ["Mois 3", "Entretien de suivi avec le manager"],
                        ]
                    }
                ],
            ),
            (
                "3. Habilitations et acces initiaux",
                [
                    "Les acces necessaires au poste sont demandes par le manager au moins 5 jours "
                    "ouvres avant l'arrivee, selon le principe du moindre privilege decrit dans "
                    "PR-ITS-MRD-004. Aucun acces n'est active avant la signature du contrat.",
                ],
            ),
            (
                "4. Formation initiale obligatoire",
                [
                    "Tout nouveau collaborateur suit la formation initiale a la securite des systemes "
                    "d'information et, selon son poste, la formation au systeme qualite decrite dans "
                    "PR-RH-MRD-006, avant toute intervention sur les processus reglementes.",
                ],
            ),
            (
                "5. Entretien de fin de periode d'essai",
                [
                    "Un entretien formel est realise avec le manager avant le terme de la periode "
                    "d'essai. Son compte-rendu est verse au dossier individuel du collaborateur et "
                    "conserve selon les regles de PR-EXM-MRD-003.",
                ],
            ),
            (
                "6. Documents associes",
                [
                    ["PR-ITS-MRD-004 - Gestion des acces et des habilitations"],
                    ["PR-RH-MRD-006 - Formation et habilitation du personnel"],
                    ["PR-EXM-MRD-003 - Securite des systemes d'information et des postes de travail"],
                ],
            ),
        ],
        "revisions": [
            ("V2", "2025-01-20", "Ajout de l'entretien de fin de periode d'essai"),
            ("V1", "2023-06-14", "Creation"),
        ],
    },
    {
        "ref": "SOP-PV-MRD-019",
        "title": "Regulatory Watch and Signal Detection",
        "version": "V2",
        "effective": "2025-03-25",
        "dept": "Pharmacovigilance",
        "doc_type": "Standard Operating Procedure",
        "lang": "en",
        "author": "Dr Helene Marchetti",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Purpose",
                [
                    "This standard operating procedure describes the regulatory watch and signal "
                    "detection activities performed by the Meridian Labs pharmacovigilance team.",
                ],
            ),
            (
                "2. Sources monitored",
                [
                    [
                        "regulatory authority bulletins and safety communications;",
                        "scientific literature relevant to the therapeutic areas covered;",
                        "the internal case database maintained under PR-PV-MRD-002;",
                        "aggregate reports received from partner organisations.",
                    ]
                ],
            ),
            (
                "3. Signal detection frequency",
                [
                    {
                        "table": [
                            ["Source", "Review frequency", "Owner"],
                            ["Regulatory bulletins", "Weekly", "Pharmacovigilance team"],
                            ["Internal case database", "Monthly", "Pharmacovigilance team"],
                            ["Scientific literature", "Monthly", "Dr Helene Marchetti"],
                        ]
                    }
                ],
            ),
            (
                "4. Signal evaluation and escalation",
                [
                    "Any potential signal is evaluated within 5 working days of detection. A "
                    "confirmed signal is escalated to the competent authority following the "
                    "transmission timelines defined in PR-PV-MRD-002.",
                ],
            ),
            (
                "5. Reporting to management",
                [
                    "A summary of regulatory watch activity and any confirmed signal is presented at "
                    "the management review described in PR-QA-MRD-011.",
                ],
            ),
            (
                "6. Related documents",
                [
                    ["PR-PV-MRD-002 - Pharmacovigilance - reception et transmission des cas"],
                    ["PR-QA-MRD-011 - Revue de direction"],
                ],
            ),
        ],
        "revisions": [
            ("V2", "2025-03-25", "Signal evaluation window shortened from 10 to 5 working days"),
            ("V1", "2023-08-01", "Initial release"),
        ],
    },
    {
        "ref": "TEAM-QA-MRD-020",
        "title": "Organisation de l'equipe Assurance Qualite",
        "version": "V4",
        "effective": "2025-04-02",
        "dept": "Assurance Qualite",
        "doc_type": "Fiche d'organisation",
        "lang": "fr",
        "author": "Sarah Delaunay",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Ce document decrit la composition et la repartition des activites de l'equipe "
                    "Assurance Qualite de Meridian Labs.",
                ],
            ),
            (
                "2. Composition de l'equipe",
                [
                    "L'equipe compte 4 collaborateurs au 2 avril 2025 :",
                    {
                        "table": [
                            ["Role", "Titulaire"],
                            ["Responsable Assurance Qualite", "Sarah Delaunay"],
                            ["Auditrice interne et formation", "Nadia Bouchard"],
                            ["Qualiticien processus", "Farid Amrani"],
                            ["Alternante Assurance Qualite", "Lea Girard"],
                        ]
                    },
                ],
            ),
            (
                "3. Repartition des activites",
                [
                    "Sarah Delaunay pilote la gestion documentaire, la revue de direction et la "
                    "maitrise du changement. Nadia Bouchard pilote le programme d'audits internes et "
                    "le plan de formation. Farid Amrani assure le traitement courant des "
                    "non-conformites et le suivi des indicateurs de processus. Lea Girard appuie "
                    "l'equipe sur la maitrise des enregistrements et la preparation des revues.",
                ],
            ),
            (
                "4. Documents associes",
                [
                    ["PR-QA-MRD-001 - Gestion documentaire du systeme qualite"],
                    ["PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)"],
                    ["PR-QA-MRD-010 - Programme d'audits internes"],
                    ["PR-QA-MRD-011 - Revue de direction"],
                ],
            ),
        ],
        "revisions": [
            ("V4", "2025-04-02", "Arrivee de Lea Girard en alternance, effectif porte a 4"),
            ("V3", "2024-01-22", "Creation du poste de qualiticien processus"),
        ],
    },
    {
        "ref": "DR_RISKA-QA-MRD-022",
        "title": "Analyse de risques du processus de gestion documentaire",
        "version": "V1",
        "effective": "2025-02-17",
        "dept": "Assurance Qualite",
        "doc_type": "Dossier de risques",
        "lang": "fr",
        "author": "Sarah Delaunay",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet et perimetre",
                [
                    "Ce dossier presente l'analyse de risques du processus de gestion documentaire du "
                    "systeme qualite de Meridian Labs, couvrant la redaction, l'approbation, la "
                    "diffusion et l'archivage des documents.",
                ],
            ),
            (
                "2. Methode",
                [
                    "L'analyse retient une echelle qualitative de criticite calculee comme le produit "
                    "de la probabilite (1 a 3) et de la gravite (1 a 3), soit une echelle de 1 a 9. "
                    "Cette echelle est distincte de celle utilisee dans les analyses de risques "
                    "techniques, qui couvrent un perimetre different.",
                ],
            ),
            (
                "3. Synthese des risques",
                [
                    {
                        "table": [
                            ["Categorie", "Nombre"],
                            ["Risques identifies", "14"],
                            ["Risques majeurs", "2"],
                            ["Risques acceptes sous controle", "12"],
                        ]
                    },
                    "Le risque de criticite la plus elevee est la mise en activite d'un document "
                    "avant la fin du delai d'auto-formation, evalue a une criticite de 9. La mesure "
                    "de reduction associee est le controle automatise du taux d'accuse de reception "
                    "decrit dans PR-QA-MRD-001.",
                ],
            ),
            (
                "4. Revision",
                [
                    "Cette analyse de risques est revisee tous les 2 ans ou a la suite de toute "
                    "evolution majeure du processus de gestion documentaire.",
                ],
            ),
            (
                "5. Documents associes",
                [
                    ["PR-QA-MRD-001 - Gestion documentaire du systeme qualite"],
                    ["PR-QA-MRD-017 - Maitrise des enregistrements qualite"],
                ],
            ),
        ],
        "revisions": [
            ("V1", "2025-02-17", "Creation, 14 risques identifies"),
        ],
    },
    {
        "ref": "PR-MI-MRD-023",
        "title": "Base de connaissances medicale et FAQ",
        "version": "V3",
        "effective": "2025-01-13",
        "dept": "Information Medicale",
        "doc_type": "Procedure",
        "lang": "fr",
        "author": "Dr Helene Marchetti",
        "approver": "Marc Villeneuve",
        "sections": [
            (
                "1. Objet",
                [
                    "Cette procedure decrit la creation, la validation et la revision des fiches de "
                    "la base de connaissances medicale utilisee par le service d'information "
                    "medicale de Meridian Labs pour repondre aux demandes recurrentes.",
                ],
            ),
            (
                "2. Structure de la base",
                [
                    "La base de connaissances est organisee en 4 categories : posologie et modalites "
                    "d'administration, interactions et contre-indications, effets indesirables "
                    "connus, et questions administratives frequentes.",
                ],
            ),
            (
                "3. Creation et validation d'une fiche",
                [
                    "Toute nouvelle fiche est redigee par un charge d'information medicale puis "
                    "validee par Dr Helene Marchetti avant sa mise a disposition de l'equipe. Une "
                    "fiche non validee ne peut pas etre utilisee pour repondre a une demande.",
                ],
            ),
            (
                "4. Revision periodique",
                [
                    "Chaque fiche est revisee au moins une fois par an, ou sans delai en cas "
                    "d'evolution reglementaire ou de signal de pharmacovigilance confirme selon "
                    "SOP-PV-MRD-019.",
                ],
            ),
            (
                "5. Documents associes",
                [
                    ["PR-MI-MRD-001 - Traitement des demandes d'information medicale"],
                    ["SOP-PV-MRD-019 - Regulatory Watch and Signal Detection"],
                ],
            ),
        ],
        "revisions": [
            ("V3", "2025-01-13", "Ajout de la categorie questions administratives frequentes"),
            ("V2", "2023-05-30", "Passage a une revision annuelle systematique"),
        ],
    },
]


# --------------------------------------------------------------------------
# Rendering
# --------------------------------------------------------------------------


def _header_rows(doc: dict[str, Any]) -> list[list[str]]:
    return [
        ["Reference", doc["ref"], "Version", doc["version"]],
        ["Type", doc["doc_type"], "Mise en activite", doc["effective"]],
        ["Entite", f"{ORG} - {doc['dept']}", "Redacteur", doc["author"]],
        ["Statut", "En activite", "Approbateur", doc["approver"]],
    ]


def render_markdown(doc: dict[str, Any]) -> str:
    lines: list[str] = [f"# {doc['ref']} - {doc['title']}", ""]

    lines.append("| Champ | Valeur | Champ | Valeur |")
    lines.append("|---|---|---|---|")
    for row in _header_rows(doc):
        lines.append("| " + " | ".join(row) + " |")
    lines.append("")

    for heading, body in doc["sections"]:
        lines.append(f"## {heading}")
        lines.append("")
        for element in body:
            if isinstance(element, str):
                lines.append(element)
                lines.append("")
            elif isinstance(element, list):
                for item in element:
                    lines.append(f"- {item}")
                lines.append("")
            elif isinstance(element, dict) and "table" in element:
                table = element["table"]
                lines.append("| " + " | ".join(table[0]) + " |")
                lines.append("|" + "---|" * len(table[0]))
                for row in table[1:]:
                    lines.append("| " + " | ".join(row) + " |")
                lines.append("")

    lines.append("## Historique des revisions")
    lines.append("")
    lines.append("| Version | Date | Objet de la revision |")
    lines.append("|---|---|---|")
    for version, date, note in doc["revisions"]:
        lines.append(f"| {version} | {date} | {note} |")
    lines.append("")
    lines.append(
        f"_Document fictif genere pour une demonstration technique. "
        f"{ORG} est une organisation imaginaire._"
    )
    lines.append("")

    return "\n".join(lines)


def render_pdf(doc: dict[str, Any], path: Path) -> None:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.platypus import (
        ListFlowable,
        ListItem,
        PageBreak,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
        Table,
        TableStyle,
    )

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "MRDBody",
        parent=styles["BodyText"],
        fontSize=9.5,
        leading=13.5,
        alignment=TA_JUSTIFY,
        spaceAfter=5,
    )
    title_style = ParagraphStyle(
        "MRDTitle", parent=styles["Title"], fontSize=15, leading=19, spaceAfter=2
    )
    subtitle_style = ParagraphStyle(
        "MRDSubtitle",
        parent=styles["Normal"],
        fontSize=9,
        textColor=colors.HexColor("#555555"),
        spaceAfter=10,
    )
    heading_style = ParagraphStyle(
        "MRDHeading",
        parent=styles["Heading2"],
        fontSize=11,
        leading=14,
        spaceBefore=10,
        spaceAfter=4,
        textColor=colors.HexColor("#1a3d5c"),
    )
    cell_style = ParagraphStyle("MRDCell", parent=styles["Normal"], fontSize=8.5, leading=11)

    def _footer(canvas, _doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(colors.HexColor("#777777"))
        canvas.drawString(
            18 * mm, 12 * mm, f"{doc['ref']} - {doc['version']} - {ORG} (document fictif)"
        )
        canvas.drawRightString(192 * mm, 12 * mm, f"Page {canvas.getPageNumber()}")
        canvas.restoreState()

    pdf = SimpleDocTemplate(
        str(path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=20 * mm,
        title=f"{doc['ref']} - {doc['title']}",
        author=ORG,
    )

    grid = TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#aaaaaa")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eef4")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]
    )

    story: list[Any] = []
    story.append(Paragraph(f"{doc['ref']} - {doc['title']}", title_style))
    story.append(Paragraph(f"{ORG} - {doc['dept']}", subtitle_style))

    header = Table(
        [[Paragraph(c, cell_style) for c in row] for row in _header_rows(doc)],
        colWidths=[30 * mm, 62 * mm, 32 * mm, 50 * mm],
    )
    header.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#aaaaaa")),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e8eef4")),
                ("BACKGROUND", (2, 0), (2, -1), colors.HexColor("#e8eef4")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    story.append(header)
    story.append(Spacer(1, 8))

    for heading, body in doc["sections"]:
        story.append(Paragraph(heading, heading_style))
        for element in body:
            if isinstance(element, str):
                story.append(Paragraph(element, body_style))
            elif isinstance(element, list):
                story.append(
                    ListFlowable(
                        [ListItem(Paragraph(item, body_style), leftIndent=12) for item in element],
                        bulletType="bullet",
                        start="circle",
                        leftIndent=14,
                    )
                )
                story.append(Spacer(1, 4))
            elif isinstance(element, dict) and "table" in element:
                rows = element["table"]
                width = 174 * mm / len(rows[0])
                table = Table(
                    [[Paragraph(c, cell_style) for c in row] for row in rows],
                    colWidths=[width] * len(rows[0]),
                    repeatRows=1,
                )
                table.setStyle(grid)
                story.append(table)
                story.append(Spacer(1, 6))

    story.append(PageBreak())
    story.append(Paragraph("Historique des revisions", heading_style))
    rev_rows = [["Version", "Date", "Objet de la revision"]] + [
        list(r) for r in doc["revisions"]
    ]
    rev = Table(
        [[Paragraph(c, cell_style) for c in row] for row in rev_rows],
        colWidths=[24 * mm, 30 * mm, 120 * mm],
        repeatRows=1,
    )
    rev.setStyle(grid)
    story.append(rev)
    story.append(Spacer(1, 10))
    story.append(
        Paragraph(
            f"Document fictif genere pour une demonstration technique. "
            f"{ORG} est une organisation imaginaire ; toute ressemblance avec une "
            f"organisation reelle serait fortuite.",
            subtitle_style,
        )
    )

    pdf.build(story, onFirstPage=_footer, onLaterPages=_footer)


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the Meridian Labs demo corpus")
    parser.add_argument("--out", default="corpus", help="Output directory (default: corpus)")
    parser.add_argument(
        "--formats",
        default="md,pdf",
        help="Comma-separated output formats: md, pdf (default: md,pdf)",
    )
    args = parser.parse_args()

    formats = {f.strip().lower() for f in args.formats.split(",") if f.strip()}
    unknown = formats - {"md", "pdf"}
    if unknown:
        print(f"Unknown format(s): {', '.join(sorted(unknown))}", file=sys.stderr)
        return 2

    out_root = Path(args.out).resolve()
    md_dir = out_root / "md"
    pdf_dir = out_root / "pdf"

    if "pdf" in formats:
        try:
            import reportlab  # noqa: F401
        except ImportError:
            print(
                "reportlab is required for PDF output. Install it with:\n"
                "    pip install reportlab\n"
                "or generate Markdown only with --formats md",
                file=sys.stderr,
            )
            return 3

    refs = [d["ref"] for d in DOCUMENTS]
    if len(set(refs)) != len(refs):
        print("Duplicate document references in DOCUMENTS", file=sys.stderr)
        return 4

    if "md" in formats:
        md_dir.mkdir(parents=True, exist_ok=True)
    if "pdf" in formats:
        pdf_dir.mkdir(parents=True, exist_ok=True)

    for doc in DOCUMENTS:
        if "md" in formats:
            target = md_dir / f"{doc['ref']}.md"
            target.write_text(render_markdown(doc), encoding="utf-8")
            print(f"  md   {target.relative_to(out_root.parent)}")
        if "pdf" in formats:
            target = pdf_dir / f"{doc['ref']}.pdf"
            render_pdf(doc, target)
            print(f"  pdf  {target.relative_to(out_root.parent)}")

    print(f"\n{len(DOCUMENTS)} documents written to {out_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
