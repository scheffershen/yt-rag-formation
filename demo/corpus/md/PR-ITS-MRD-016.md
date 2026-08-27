# PR-ITS-MRD-016 - Gestion des incidents de securite informatique

| Champ | Valeur | Champ | Valeur |
|---|---|---|---|
| Reference | PR-ITS-MRD-016 | Version | V2 |
| Type | Procedure | Mise en activite | 2025-05-30 |
| Entite | Meridian Labs - Systemes d'Information | Redacteur | Julien Kessler |
| Statut | En activite | Approbateur | Marc Villeneuve |

## 1. Objet

Cette procedure decrit la detection, la qualification et le traitement des incidents de securite informatique susceptibles d'affecter la confidentialite, l'integrite ou la disponibilite des systemes de Meridian Labs.

## 2. Classification des incidents

| Niveau | Exemple | Delai de prise en charge |
|---|---|---|
| Critique | Compromission averee, fuite de donnees personnelles | 1 heure |
| Majeur | Activite suspecte confirmee, indisponibilite de service | 4 heures |
| Mineur | Tentative bloquee, anomalie sans impact confirme | 2 jours ouvres |

## 3. Detection et remontee

Tout collaborateur suspectant un incident de securite le signale sans delai a l'equipe Systemes d'Information par le canal d'astreinte decrit dans TEAM-ITS-MRD-001. Les alertes automatiques des outils de supervision sont qualifiees par l'equipe Infrastructure dans le delai fixe par le niveau presume.

## 4. Confinement et eradication

Le RSSI coordonne les mesures de confinement (isolement reseau, revocation d'acces, changement d'identifiants) puis l'eradication de la cause identifiee, en s'appuyant si necessaire sur la procedure d'acces exceptionnel de PR-ITS-MRD-004.

## 5. Notification

Un incident critique impliquant des donnees a caractere personnel est notifie au Delegue a la Protection des Donnees dans un delai de 24 heures, en vue d'une eventuelle notification a l'autorite de controle dans le delai reglementaire de 72 heures.

## 6. Retour d'experience

Tout incident critique ou majeur donne lieu a un retour d'experience formalise sous 10 jours ouvres apres cloture, et a l'ouverture d'une non-conformite selon PR-QA-MRD-009 lorsque l'incident revele une defaillance de controle.

## 7. Documents associes

- PR-ITS-MRD-004 - Gestion des acces et des habilitations

- PR-EXM-MRD-003 - Securite des systemes d'information et des postes de travail

- PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)

## Historique des revisions

| Version | Date | Objet de la revision |
|---|---|---|
| V2 | 2025-05-30 | Ajout du delai de notification DPO a 24 heures |
| V1 | 2024-02-05 | Creation |

_Document fictif genere pour une demonstration technique. Meridian Labs est une organisation imaginaire._
