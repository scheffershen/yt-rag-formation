# Chunk lab — q30

**Question:** Un taux d'accuse de reception de 85 pour cent a la mise en activite - est-ce un probleme, et sous quel delai doit-il etre traite ?

**Metric:** source-window proxy: windows containing both the source reference and every required fact term

**Limitation:** This inspects synthetic Markdown source windows. It does not query, change, or reindex the live demo stack.

Configuration: `280` characters per window, `40` overlap characters.

## PR-QA-MRD-001

- Windows: 21
- Evidence-and-identity windows: none
- Evidence-and-identity rate: 0.0%

### Window 1 — required fact absent

```text
# PR-QA-MRD-001 - Gestion documentaire du systeme qualite
```

### Window 2 — required fact absent

```text
| Champ | Valeur | Champ | Valeur |
|---|---|---|---|
| Reference | PR-QA-MRD-001 | Version | V6 |
| Type | Procedure | Mise en activite | 2025-02-10 |
| Entite | Meridian Labs - Assurance Qualite | Redacteur | Sarah Delaunay |
| Statut | En activite | Approbateur | Marc Villeneu
```

### Window 3 — required fact absent

```text
n activite | Approbateur | Marc Villeneuve |
```

### Window 4 — required fact absent

```text
## 1. Objet et domaine d'application
```

### Window 5 — required fact absent

```text
La presente procedure decrit le cycle de vie des documents du systeme qualite de Meridian Labs : redaction, verification, approbation, diffusion, revision et archivage. Elle s'applique a l'ensemble des collaborateurs, y compris les prestataires intervenant sur les processus quali
```

### Window 6 — required fact absent

```text
ires intervenant sur les processus qualite.
```

### Window 7 — required fact absent

```text
## 2. Responsabilites
```

### Window 8 — required fact absent

```text
- Le redacteur produit la version de travail et renseigne le tableau de revisions.
- Le verificateur controle la coherence technique et les references croisees.
- Le Responsable Assurance Qualite approuve le document et declenche sa mise en activite.
- Chaque manager s'assure de 
```

### Window 9 — required fact absent

```text
 activite.
- Chaque manager s'assure de l'accuse de reception de ses collaborateurs.
```

### Window 10 — required fact absent

```text
## 3. Circuit d'approbation

Aucun document ne peut etre mis en activite sans l'approbation du Responsable Assurance Qualite. L'approbation est tracee electroniquement dans l'outil de gestion documentaire, avec horodatage et identite de l'approbateur.
```

### Window 11 — required fact absent

```text
horodatage et identite de l'approbateur.

## 4. Auto-formation et accuse de reception
```

### Window 12 — required fact absent

```text
4. Auto-formation et accuse de reception

Apres approbation, le document est diffuse aux collaborateurs concernes. Ceux-ci disposent d'un delai d'auto-formation de 15 jours ouvres pour prendre connaissance du document et accuser reception avant sa mise en activite.
```

### Window 13 — required fact absent

```text
ser reception avant sa mise en activite.

Passe ce delai, le manager relance nominativement les collaborateurs n'ayant pas accuse reception. Un taux d'accuse de reception inferieur a 90 pour cent a la date de mise en activite constitue une non-conformite mineure au sens de la procedure PR-QA-MRD-009.
```

### Window 14 — required fact absent

```text
e au sens de la procedure PR-QA-MRD-009.

## 5. Revision periodique

Chaque document du systeme qualite fait l'objet d'une revision periodique tous les 3 ans, ou de facon anticipee en cas d'evolution reglementaire, de reorganisation, ou a la suite d'une action corrective.
```

### Window 15 — required fact absent

```text
, ou a la suite d'une action corrective.

## 6. Archivage et conservation

Les documents qualite approuves sont archives pendant 10 ans a compter de leur date de retrait. L'archivage est electronique, sur le coffre-fort documentaire decrit dans la procedure PR-ITS-MRD-004.
```

### Window 16 — required fact absent

```text
decrit dans la procedure PR-ITS-MRD-004.

La conservation des dossiers individuels de formation des collaborateurs releve de la procedure PR-EXM-MRD-003 et suit une regle distincte.

## 7. Documents externes
```

### Window 17 — required fact absent

```text
Un document externe (norme, texte reglementaire, exigence client) est enregistre dans le meme referentiel documentaire que les documents internes, avec mention de sa source et de sa date de derniere verification aupres de l'emetteur. Sa revision n'est pas planifiee : elle est dec
```

### Window 18 — required fact absent

```text
ision n'est pas planifiee : elle est declenchee par la publication d'une nouvelle version par l'emetteur.
```

### Window 19 — required fact absent

```text
## 8. Documents associes

- PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)

- PR-QA-MRD-012 - Maitrise du changement

- PR-QA-MRD-017 - Maitrise des enregistrements qualite

## Historique des revisions
```

### Window 20 — required fact absent

```text
nts qualite

## Historique des revisions

| Version | Date | Objet de la revision |
|---|---|---|
| V6 | 2025-02-10 | Delai d'auto-formation porte de 10 a 15 jours ouvres |
| V5 | 2024-04-22 | Ajout du seuil de 90 pour cent d'accuse de reception |
| V4 | 2023-01-30 | Revision periodique alignee sur 3 ans |
```

### Window 21 — required fact absent

```text
 Revision periodique alignee sur 3 ans |

_Document fictif genere pour une demonstration technique. Meridian Labs est une organisation imaginaire._
```

## PR-QA-MRD-009

- Windows: 17
- Evidence-and-identity windows: none
- Evidence-and-identity rate: 0.0%

### Window 1 — required fact absent

```text
# PR-QA-MRD-009 - Gestion des non-conformites et des actions correctives (CAPA)
```

### Window 2 — required fact absent

```text
| Champ | Valeur | Champ | Valeur |
|---|---|---|---|
| Reference | PR-QA-MRD-009 | Version | V4 |
| Type | Procedure | Mise en activite | 2025-03-03 |
| Entite | Meridian Labs - Assurance Qualite | Redacteur | Sarah Delaunay |
| Statut | En activite | Approbateur | Marc Villeneu
```

### Window 3 — required fact absent

```text
n activite | Approbateur | Marc Villeneuve |
```

### Window 4 — required fact absent

```text
## 1. Objet

Cette procedure definit le traitement des non-conformites detectees en interne ou signalees par un client, ainsi que la conduite des plans d'action correctifs et preventifs.

## 2. Classification
```

### Window 5 — required fact absent

```text
ifs et preventifs.

## 2. Classification

Toute non-conformite est classee majeure ou mineure par le Responsable Assurance Qualite dans les 2 jours ouvres suivant sa detection. Les criteres de classification sont definis dans l'annexe AN-QA-MRD-000.

## 3. Information du client
```

### Window 6 — required fact absent

```text
QA-MRD-000.

## 3. Information du client

En cas de non-conformite majeure, le client concerne est informe dans un delai maximum de 24 heures apres la classification. L'information est transmise par ecrit et tracee dans le dossier de la non-conformite.
```

### Window 7 — required fact absent

```text
ee dans le dossier de la non-conformite.

Pour une non-conformite mineure, l'information du client est realisee dans le cadre du reporting mensuel.

## 4. Delais de cloture des plans d'action
```

### Window 8 — required fact present

```text
 4. Delais de cloture des plans d'action

| Classification | Delai de cloture | Validation |
|---|---|---|
| Non-conformite majeure | 45 jours calendaires | Responsable AQ + Direction |
| Non-conformite mineure | 90 jours calendaires | Responsable AQ |
| Observation | Sans delai contraignant | Pilote de processus |
```

### Window 9 — required fact absent

```text
lai contraignant | Pilote de processus |

Tout depassement de delai fait l'objet d'une demande de prolongation motivee, soumise au Responsable Assurance Qualite avant l'echeance initiale.

## 5. Verification d'efficacite
```

### Window 10 — required fact absent

```text
itiale.

## 5. Verification d'efficacite

L'efficacite de chaque action corrective est verifiee 3 mois apres la cloture du plan d'action. Une action jugee inefficace donne lieu a la reouverture de la non-conformite.

## 6. Escalade
```

### Window 11 — required fact absent

```text
re de la non-conformite.

## 6. Escalade

La survenue de plus de 2 non-conformites majeures sur un meme trimestre pour un meme processus declenche une revue exceptionnelle par la Direction et l'ouverture d'un audit interne cible selon PR-QA-MRD-010.
```

### Window 12 — required fact absent

```text
audit interne cible selon PR-QA-MRD-010.

## 7. Non-conformites d'origine externe
```

### Window 13 — required fact absent

```text
Une non-conformite peut etre ouverte a partir d'une reclamation client qualifiee selon PR-CLI-MRD-013, d'un ecart releve lors d'un audit fournisseur conduit selon PR-ACH-MRD-007, ou d'une anomalie detectee lors d'une revue de pistes d'audit selon SOP-QA-MRD-015. Le circuit de cla
```

### Window 14 — required fact absent

```text
 selon SOP-QA-MRD-015. Le circuit de classification et de cloture reste identique quelle que soit son origine.
```

### Window 15 — required fact absent

```text
## 8. Documents associes

- PR-QA-MRD-010 - Programme d'audits internes

- PR-CLI-MRD-013 - Gestion des reclamations clients

- PR-QA-MRD-011 - Revue de direction

## Historique des revisions
```

### Window 16 — required fact absent

```text
e direction

## Historique des revisions

| Version | Date | Objet de la revision |
|---|---|---|
| V4 | 2025-03-03 | Delai de cloture majeur ramene de 60 a 45 jours calendaires |
| V3 | 2024-02-19 | Ajout de la verification d'efficacite a 3 mois |
| V2 | 2022-11-08 | Ajout du critere d'escalade trimestriel |
```

### Window 17 — required fact absent

```text
jout du critere d'escalade trimestriel |

_Document fictif genere pour une demonstration technique. Meridian Labs est une organisation imaginaire._
```
