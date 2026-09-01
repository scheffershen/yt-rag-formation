# PR-EXM-MRD-014 - Plan de continuite d'activite

| Champ | Valeur | Champ | Valeur |
|---|---|---|---|
| Reference | PR-EXM-MRD-014 | Version | V3 |
| Type | Procedure | Mise en activite | 2025-04-14 |
| Entite | Meridian Labs - Exploitation et Maintenance | Redacteur | Theo Mbala |
| Statut | En activite | Approbateur | Julien Kessler |

## 1. Objet et perimetre

Ce plan decrit l'organisation retenue par Meridian Labs pour assurer la continuite des activites critiques en cas de sinistre affectant les locaux, les systemes d'information, ou une part significative du personnel.

## 2. Scenarios de sinistre couverts

- indisponibilite du site principal d'hebergement ;
- indisponibilite prolongee de la plateforme MeridianCore ;
- indisponibilite des locaux administratifs ;
- indisponibilite d'une part significative du personnel cle.

## 3. Site de secours et bascule

La plateforme MeridianCore beneficie d'une replication synchrone vers un site d'hebergement secondaire. La bascule vers le site de secours est declenchee par le Responsable Infrastructure sur decision du Directeur des Systemes d'Information.

## 4. Objectifs de reprise

Les objectifs de reprise par systeme sont alignes sur l'analyse de risques DR_RISKA-ITS-MRD-005 :

| Systeme | RTO | RPO |
|---|---|---|
| Plateforme MeridianCore | 4 heures | 1 heure |
| Messagerie et outils collaboratifs | 8 heures | 4 heures |
| Systemes administratifs internes | 48 heures | 24 heures |

## 5. Exercice annuel

Un exercice de continuite d'activite grandeur reelle est organise chaque annee, incluant la bascule effective vers le site de secours. Le rapport d'exercice est presente en revue de direction selon PR-QA-MRD-011.

## 6. Documents associes

- DR_RISKA-ITS-MRD-005 - Analyse de risques de la plateforme MeridianCore

- PR-EXM-MRD-003 - Securite des systemes d'information et des postes de travail

- PR-QA-MRD-011 - Revue de direction

## Historique des revisions

| Version | Date | Objet de la revision |
|---|---|---|
| V3 | 2025-04-14 | Ajout des objectifs de reprise par systeme |
| V2 | 2023-11-28 | Passage a un exercice annuel grandeur reelle |

_Document fictif genere pour une demonstration technique. Meridian Labs est une organisation imaginaire._
