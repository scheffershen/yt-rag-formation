# RAG evaluation - demo-fixed

- run at: 2026-08-14T08:54:32+00:00
- api: `http://localhost:8000`
- workspace: `meridian_demo`
- eval set: `eval_set.yaml` (65 questions, 6 unanswerable)
- topk: 5, graph_topk: 20, similarity_threshold: 0.2
- judge: `gpt-4o-mini`

## Retrieval ablation

Share of answerable questions where **every** expected source document was retrieved. Matching is on result metadata only, never on chunk body text.

| Indexes enabled | Hit rate | Index alone |
|---|---|---|
| vector only | 86.4% | 86.4% |
| + fulltext | 86.4% | 28.8% |
| + summary | 91.5% | 86.4% |
| + graph (approx) | 100.0% | 100.0% |

> The graph column is approximate: LightRAG returns a flat context string, so a reference found there may originate from a cross-reference inside another document rather than from the document itself.

## Answer quality

| Metric | Value |
|---|---|
| Strict accuracy (judge = correct) | **70.8%** |
| Lenient accuracy (correct + partial) | 93.8% |
| Source hit rate (all expected docs cited) | 91.5% |
| Keyword coverage | 73.7% |
| Refusal accuracy on unanswerable | 100.0% |
| Hallucination rate on unanswerable | 0.0% |
| Latency p50 / p95 | 2.41s / 4.28s |

### By category

| Category | n | Correct | % |
|---|---|---|---|
| acronym | 3 | 3 | 100.0% |
| cross_lingual | 5 | 5 | 100.0% |
| factual | 35 | 21 | 60.0% |
| multi_hop | 9 | 6 | 66.7% |
| reference_lookup | 7 | 5 | 71.4% |
| unanswerable | 6 | 6 | 100.0% |

### Failures (19)

**q01 - partial** - Quel est le delai de cloture d'un plan d'action pour une non-conformite majeure ?

- judge: Missing validation requirement from the Responsible AQ and Direction.
- expected sources: PR-QA-MRD-009
- not retrieved: -
- answer: Le délai de clôture d'un plan d'action pour une non-conformité majeure est de 45 jours [Source: PR-QA-MRD-009.pdf].

**q07 - partial** - Quelle est la longueur minimale exigee pour un mot de passe ?

- judge: Missing details on rotation and MFA requirements.
- expected sources: PR-EXM-MRD-003
- not retrieved: -
- answer: La longueur minimale exigée pour un mot de passe est de 14 caractères [Source: PR-EXM-MRD-003.pdf].

**q09 - partial** - A quelle frequence la revue des habilitations est-elle realisee ?

- judge: Missing mention of application owners and RSSI control.
- expected sources: PR-ITS-MRD-004
- not retrieved: -
- answer: La revue des habilitations est réalisée tous les 6 mois [Source: PR-ITS-MRD-004.pdf].

**q10 - incorrect** - Quelle est la duree de retention des sauvegardes ?

- judge: Fails to provide any information about backup retention duration.
- expected sources: PR-EXM-MRD-003
- not retrieved: -
- answer: Je ne sais pas en me basant sur les données indexées.

**q11 - partial** - Sous quel delai un cas grave de pharmacovigilance doit-il etre transmis a l'autorite competente ?

- judge: Mentions correct 15 days but adds unnecessary detail about unexpected cases.
- expected sources: PR-PV-MRD-002
- not retrieved: -
- answer: Un cas grave de pharmacovigilance doit être transmis à l'autorité compétente dans un délai de 15 jours calendaires. Si le cas est à la fois grave et inattendu, le délai est réduit à 7 jours calendaires [Source: PR-PV-MRD-002.pdf].

**q13 - partial** - Qui est le lead developer de l'equipe Systemes d'Information ?

- judge: Missing mention of Ines Bouziane as supplante.
- expected sources: TEAM-ITS-MRD-001
- not retrieved: -
- answer: Le lead developer de l'équipe Systèmes d'Information est Camille Renard [Source: TEAM-ITS-MRD-001.pdf].

**q16 - partial** - Combien de risques ont ete identifies dans l'analyse de risques de MeridianCore, et combien sont majeurs ?

- judge: Missing mention of 7 non bloquants risques.
- expected sources: DR_RISKA-ITS-MRD-005
- not retrieved: -
- answer: Dans l'analyse de risques de MeridianCore, 29 risques ont été identifiés, dont 3 sont majeurs [Source: DR_RISKA-ITS-MRD-005.pdf].

**q17 - partial** - Quel volume horaire minimal de formation chaque collaborateur doit-il suivre chaque annee ?

- judge: Missing the detail about 7 hours for the quality system.
- expected sources: PR-RH-MRD-006
- not retrieved: -
- answer: Chaque collaborateur doit suivre un volume horaire minimal de 21 heures de formation par an [Source: PR-RH-MRD-006.pdf].

**q18 - partial** - Quelle quantite de memoire vive est requise au minimum pour un poste client MeridianCore ?

- judge: Missing the recommended 32 Go of mémoire vive.
- expected sources: FT-EXM-MRD-008
- not retrieved: -
- answer: La quantité de mémoire vive requise au minimum pour un poste client MeridianCore est de 16 Go [Source: FT-EXM-MRD-008.pdf].

**q19 - partial** - Combien de temps un acces exceptionnel peut-il rester actif ?

- judge: Missing mention of revocation and validation by RSSI.
- expected sources: PR-ITS-MRD-004
- not retrieved: -
- answer: Un accès exceptionnel peut rester actif pendant 72 heures avec validation [Source: PR-ITS-MRD-004.pdf].

**q24 - incorrect** - Qu'est-ce qui a change entre la V3 et la V4 de PR-QA-MRD-009 ?

- judge: Fails to provide any relevant information about the changes.
- expected sources: PR-QA-MRD-009
- not retrieved: -
- answer: Je ne sais pas basé sur les données indexées.

**q28 - partial** - Une demande d'information medicale decrivant un effet indesirable - quel circuit suit-elle et sous quel delai ?

- judge: Missing specific mention of the service code PR-MI-MRD-001.
- expected sources: PR-MI-MRD-001, PR-PV-MRD-002
- not retrieved: -
- answer: Une demande d'information médicale décrivant un effet indésirable suit le circuit de traitement des cas de pharmacovigilance, tel que décrit dans la procédure PR-PV-MRD-002. Lorsqu'un effet indésirable est signalé, la demande est transmise au service de pharmacovigilance. Un accusé de réception est envoyé au notificateur dans un délai de 2 jours ouvrés. Les délais de transmission aux autorités com

**q29 - partial** - Quelle mesure technique couvre le risque de perte de disponibilite de la base de donnees, et ou est-elle decrite ?

- judge: Mentions replication but fails to include quarterly restoration test and its document reference.
- expected sources: DR_RISKA-ITS-MRD-005, PR-EXM-MRD-003
- not retrieved: -
- answer: La mesure technique qui couvre le risque de perte de disponibilité de la base de données est la réplication synchrone. Cette mesure est décrite dans le document d'analyse de risques de la plateforme MeridianCore, référencé sous le nom DR_RISKA-ITS-MRD-005 [Source: DR_RISKA-ITS-MRD-005.pdf].

**q30 - partial** - Un taux d'accuse de reception de 85 pour cent a la mise en activite - est-ce un probleme, et sous quel delai doit-il etre traite ?

- judge: Missing specific non-conformity classification and 90-day action closure requirement.
- expected sources: PR-QA-MRD-001, PR-QA-MRD-009
- not retrieved: PR-QA-MRD-001
- answer: Un taux d'accusé de réception de 85 pour cent à la mise en activité peut être considéré comme un problème, car il est en dessous du seuil de conformité de 90 pour cent requis pour la mise en activité des documents. Ce taux doit être traité rapidement, et des mesures de réduction du risque, comme le contrôle automatisé du taux d'accusé de réception, devraient être mises en œuvre. L'analyse des risq

**q46 - incorrect** - Sous quel delai un fournisseur critique doit-il notifier un incident de securite a Meridian Labs ?

- judge: States 24 hours instead of the required 48 hours.
- expected sources: PR-ACH-MRD-007
- not retrieved: -
- answer: Un fournisseur critique doit notifier un incident de sécurité à Meridian Labs dans un délai de 24 heures [Source: PR-ITS-MRD-016.pdf].

**q51 - partial** - Combien de temps un compte-rendu d'audit interne est-il conserve ?

- judge: Does not provide the specific duration of 10 years.
- expected sources: PR-QA-MRD-017
- not retrieved: -
- answer: La durée de conservation d'un compte-rendu d'audit interne n'est pas spécifiquement mentionnée dans le contexte fourni. Cependant, il est indiqué que les enregistrements qualité, qui incluent les compte-rendus d'audit, doivent être conservés électroniquement avec des durées de conservation spécifiques selon leur type, mais ces durées ne sont pas détaillées dans les documents référencés [Source: PR

**q52 - incorrect** - Quel est l'objectif de reprise (RTO) retenu pour la messagerie et les outils collaboratifs ?

- judge: RTO stated as 4 hours instead of the correct 8 hours.
- expected sources: PR-EXM-MRD-014
- not retrieved: -
- answer: L'objectif de reprise (RTO) retenu pour la messagerie et les outils collaboratifs est fixé à 4 heures [Source: DR_RISKA-ITS-MRD-005.pdf].

**q58 - partial** - Combien de risques ont ete identifies dans l'analyse de risques du processus de gestion documentaire ?

- judge: Missing mention of the 2 majeurs risks identified.
- expected sources: DR_RISKA-QA-MRD-022
- not retrieved: -
- answer: Quatorze risques ont été identifiés dans l'analyse de risques du processus de gestion documentaire [Source: DR_RISKA-QA-MRD-022.pdf].

**q60 - partial** - Que couvre la procedure PR-QA-MRD-012 ?

- judge: Missing mention of classification in the system answer.
- expected sources: PR-QA-MRD-012
- not retrieved: -
- answer: La procédure PR-QA-MRD-012 couvre l'analyse d'impact et le circuit de validation pour tout changement affectant les processus, systèmes ou organisation de Meridian Labs, en mettant l'accent sur leur impact sur la qualité et la conformité. Les changements sont classés en mineurs, majeurs et urgents, chacun ayant des exigences spécifiques de validation et d'analyse d'impact, avec une vérification po

