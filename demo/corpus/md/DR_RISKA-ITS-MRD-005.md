# DR_RISKA-ITS-MRD-005 - Analyse de risques de la plateforme MeridianCore

| Champ | Valeur | Champ | Valeur |
|---|---|---|---|
| Reference | DR_RISKA-ITS-MRD-005 | Version | V2 |
| Type | Dossier de risques | Mise en activite | 2025-03-12 |
| Entite | Meridian Labs - Systemes d'Information | Redacteur | Julien Kessler |
| Statut | En activite | Approbateur | Marc Villeneuve |

## 1. Objet et perimetre

Ce dossier presente l'analyse de risques de la plateforme MeridianCore, socle applicatif hebergeant les modules qualite, information medicale et pharmacovigilance. L'analyse a ete conduite le 12 mars 2025.

## 2. Methode

L'analyse s'appuie sur la methode EBIOS Risk Manager. La criticite est calculee comme le produit de la vraisemblance (1 a 4) et de la gravite (1 a 4), soit une echelle de 1 a 16.

## 3. Synthese des risques

| Categorie | Nombre |
|---|---|
| Risques identifies | 29 |
| Risques majeurs | 3 |
| Risques non bloquants | 7 |
| Risques acceptes sous controle | 19 |

Le risque de criticite la plus elevee est la perte de disponibilite de la base de donnees principale, evalue a une criticite de 16. Les mesures de reduction associees sont la replication synchrone et le test de restauration trimestriel decrit dans PR-EXM-MRD-003.

## 4. Objectifs de reprise

Les objectifs de reprise retenus pour MeridianCore sont un RTO de 4 heures et un RPO de 1 heure. Ces objectifs sont contractualises avec les directions metier et verifies lors de l'exercice annuel de continuite d'activite.

## 5. Revision

Cette analyse de risques est revisee annuellement ou lors de tout changement majeur d'architecture.

## 6. Documents associes

- PR-EXM-MRD-014 - Plan de continuite d'activite

- PR-EXM-MRD-003 - Securite des systemes d'information et des postes de travail

- PR-ITS-MRD-016 - Gestion des incidents de securite informatique

## Historique des revisions

| Version | Date | Objet de la revision |
|---|---|---|
| V2 | 2025-03-12 | Reevaluation apres migration de l'hebergement, 29 risques identifies |
| V1 | 2023-07-19 | Creation, 24 risques identifies |

_Document fictif genere pour une demonstration technique. Meridian Labs est une organisation imaginaire._
