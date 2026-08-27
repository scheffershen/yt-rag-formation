# PR-EXM-MRD-003 - Securite des systemes d'information et des postes de travail

| Champ | Valeur | Champ | Valeur |
|---|---|---|---|
| Reference | PR-EXM-MRD-003 | Version | V7 |
| Type | Procedure | Mise en activite | 2025-05-20 |
| Entite | Meridian Labs - Exploitation et Maintenance | Redacteur | Julien Kessler |
| Statut | En activite | Approbateur | Marc Villeneuve |

## 1. Objet

Cette procedure definit les mesures de securite applicables aux postes de travail et aux serveurs exploites par Meridian Labs.

## 2. Protection antivirale

L'ensemble du parc informatique est protege par la solution antivirus Bitdefender GravityZone, administree de facon centralisee par l'equipe Exploitation. Les signatures sont mises a jour automatiquement toutes les 4 heures. Aucun poste ne peut se connecter au reseau interne sans agent actif.

## 3. Politique de mot de passe

- longueur minimale de 14 caracteres ;
- rotation obligatoire tous les 12 mois ;
- authentification multifacteur obligatoire pour tous les acces distants ;
- verrouillage automatique de la session apres 5 minutes d'inactivite ;
- blocage du compte apres 5 tentatives infructueuses.

## 4. Sauvegardes

Les donnees de production font l'objet d'une sauvegarde quotidienne incrementale et d'une sauvegarde complete hebdomadaire. La retention des sauvegardes est de 35 jours. Un test de restauration est realise chaque trimestre et son resultat est consigne.

## 5. Conservation des dossiers de formation des collaborateurs

Les dossiers individuels de formation et d'habilitation des collaborateurs sont conserves 5 ans a compter de la date de depart du collaborateur. Cette regle est distincte de la conservation des documents qualite definie dans PR-QA-MRD-001.

## 6. Incidents de securite

Toute anomalie de securite constatee sur un poste de travail ou un serveur est traitee selon la procedure PR-ITS-MRD-016, y compris lorsqu'elle est detectee par l'agent antivirus ou lors d'un test de restauration.

## 7. Documents associes

- PR-ITS-MRD-016 - Gestion des incidents de securite informatique

- PR-EXM-MRD-014 - Plan de continuite d'activite

- PR-ITS-MRD-004 - Gestion des acces et des habilitations

## Historique des revisions

| Version | Date | Objet de la revision |
|---|---|---|
| V7 | 2025-05-20 | Longueur minimale de mot de passe portee a 14 caracteres |
| V6 | 2024-08-30 | Migration de l'antivirus vers Bitdefender GravityZone |
| V5 | 2023-10-02 | Ajout du test de restauration trimestriel |

_Document fictif genere pour une demonstration technique. Meridian Labs est une organisation imaginaire._
