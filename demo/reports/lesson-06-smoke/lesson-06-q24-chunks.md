# Chunk lab — q24

**Question:** Qu'est-ce qui a change entre la V3 et la V4 de PR-QA-MRD-009 ?

**Metric:** source-window proxy: windows containing both the source reference and every required fact term

**Limitation:** This inspects synthetic Markdown source windows. It does not query, change, or reindex the live demo stack.

Configuration: `280` characters per window, `40` overlap characters.

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

### Window 16 — required fact present

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
