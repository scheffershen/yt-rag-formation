# RAG evaluation - demo-full

- run at: 2026-08-14T08:23:33+00:00
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
| + fulltext | 91.5% | 11.9% |
| + summary | 94.9% | 86.4% |
| + graph (approx) | 100.0% | 100.0% |

> The graph column is approximate: LightRAG returns a flat context string, so a reference found there may originate from a cross-reference inside another document rather than from the document itself.

## Answer quality

| Metric | Value |
|---|---|
| Strict accuracy (judge = correct) | **67.7%** |
| Lenient accuracy (correct + partial) | 90.8% |
| Source hit rate (all expected docs cited) | 91.5% |
| Keyword coverage | 75.4% |
| Refusal accuracy on unanswerable | 100.0% |
| Hallucination rate on unanswerable | 0.0% |
| Latency p50 / p95 | 2.52s / 4.8s |

### By category

| Category | n | Correct | % |
|---|---|---|---|
| acronym | 3 | 3 | 100.0% |
| cross_lingual | 5 | 5 | 100.0% |
| factual | 35 | 21 | 60.0% |
| multi_hop | 9 | 4 | 44.4% |
| reference_lookup | 7 | 5 | 71.4% |
| unanswerable | 6 | 6 | 100.0% |

### Failures (21)

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

- judge: Fails to provide the specified duration of retention.
- expected sources: PR-EXM-MRD-003
- not retrieved: -
- answer: La durée de conservation des sauvegardes n'est pas spécifiquement mentionnée dans le contexte fourni. Je ne sais pas en me basant sur les données indexées.

**q11 - partial** - Sous quel delai un cas grave de pharmacovigilance doit-il etre transmis a l'autorite competente ?

- judge: Correctly states 15 days but adds unnecessary detail about unexpected cases.
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

- judge: Missing detail about the 7 hours for quality system training.
- expected sources: PR-RH-MRD-006
- not retrieved: -
- answer: Chaque collaborateur doit suivre un volume horaire minimal de 21 heures de formation par an [Source: PR-RH-MRD-006.pdf].

**q18 - partial** - Quelle quantite de memoire vive est requise au minimum pour un poste client MeridianCore ?

- judge: Mentions minimum requirement but omits recommended 32 Go.
- expected sources: FT-EXM-MRD-008
- not retrieved: -
- answer: La quantité de mémoire vive requise au minimum pour un poste client MeridianCore est de 16 Go [Source: FT-EXM-MRD-008.pdf].

**q19 - partial** - Combien de temps un acces exceptionnel peut-il rester actif ?

- judge: Missing mention of revocation and validation by RSSI.
- expected sources: PR-ITS-MRD-004
- not retrieved: -
- answer: Un accès exceptionnel peut rester actif pendant 72 heures avec validation [Source: PR-ITS-MRD-004.pdf].

**q24 - incorrect** - Qu'est-ce qui a change entre la V3 et la V4 de PR-QA-MRD-009 ?

- judge: Fails to answer the question about changes between V3 and V4.
- expected sources: PR-QA-MRD-009
- not retrieved: -
- answer: Je ne sais pas basé sur les données indexées.

**q26 - partial** - Quelle est la duree de conservation des documents qualite, et celle des dossiers de formation d'un collaborateur ?

- judge: Missing detail about the 5-year retention after collaborator's departure.
- expected sources: PR-QA-MRD-001, PR-EXM-MRD-003
- not retrieved: -
- answer: La durée de conservation des documents qualité est de 10 ans à compter de leur date de retrait, avec une révision périodique tous les 3 ans [Source: PR-QA-MRD-001.pdf]. Les dossiers de formation des collaborateurs sont conservés pendant 5 ans [Source: PR-EXM-MRD-003.pdf].

**q28 - partial** - Une demande d'information medicale decrivant un effet indesirable - quel circuit suit-elle et sous quel delai ?

- judge: Missing specific mention of transmission to pharmacovigilance without delay.
- expected sources: PR-MI-MRD-001, PR-PV-MRD-002
- not retrieved: -
- answer: Une demande d'information médicale décrivant un effet indésirable suit le circuit de traitement des cas de pharmacovigilance, tel que décrit dans la procédure PR-PV-MRD-002. Lorsqu'un effet indésirable est signalé, il est transmis au service de pharmacovigilance et fait l'objet d'un accusé de réception adressé au notificateur dans un délai de 2 jours ouvrés. Les délais de transmission aux autorité

**q29 - incorrect** - Quelle mesure technique couvre le risque de perte de disponibilite de la base de donnees, et ou est-elle decrite ?

- judge: Incorrect document reference; does not mention test de restauration trimestriel.
- expected sources: DR_RISKA-ITS-MRD-005, PR-EXM-MRD-003
- not retrieved: -
- answer: La mesure technique qui couvre le risque de perte de disponibilité de la base de données est la réplication synchrone. Cette mesure est décrite dans le document d'analyse de risques de la plateforme MeridianCore, référencé sous DR_RISKA-ITS-MRD-005.pdf [Source: DR_RISKA-ITS-MRD-005.pdf].

**q30 - partial** - Un taux d'accuse de reception de 85 pour cent a la mise en activite - est-ce un probleme, et sous quel delai doit-il etre traite ?

- judge: Mentions a problem but lacks specific non-conformity classification and 90-day action plan.
- expected sources: PR-QA-MRD-001, PR-QA-MRD-009
- not retrieved: PR-QA-MRD-001
- answer: Un taux d'accusé de réception de 85 % à la mise en activité peut être considéré comme un problème, surtout si cela concerne des réclamations critiques, car le délai d'accusé de réception pour ces réclamations est de 4 heures. Pour les réclamations standard, le délai est de 2 jours ouvrés. Les réclamations doivent être traitées dans des délais spécifiques, et un suivi mensuel est effectué pour éval

**q31 - partial** - Quelles anomalies detectees lors de la revue des pistes d'audit doivent-elles etre traitees, et selon quelle procedure ?

- judge: Missing the specific mention of opening non-conformities.
- expected sources: SOP-QA-MRD-015, PR-QA-MRD-009
- not retrieved: SOP-QA-MRD-015
- answer: Les anomalies détectées lors de la revue des pistes d'audit doivent être traitées selon la procédure PR-QA-MRD-009. Cette procédure définit le traitement des non-conformités internes et externes, qui sont classées comme majeures ou mineures. Les non-conformités majeures doivent être clôturées dans un délai de 45 jours, tandis que les mineures ont un délai de 90 jours. Une vérification de l'efficac

**q51 - incorrect** - Combien de temps un compte-rendu d'audit interne est-il conserve ?

- judge: Fails to provide the requested information about the duration of retention.
- expected sources: PR-QA-MRD-017
- not retrieved: -
- answer: Je ne sais pas basé sur les données indexées.

**q52 - incorrect** - Quel est l'objectif de reprise (RTO) retenu pour la messagerie et les outils collaboratifs ?

- judge: States RTO as 4 heures instead of 8 heures.
- expected sources: PR-EXM-MRD-014
- not retrieved: -
- answer: L'objectif de reprise (RTO) retenu pour la messagerie et les outils collaboratifs est de 4 heures [Source: DR_RISKA-ITS-MRD-005.pdf].

**q56 - incorrect** - Combien de personnes composent l'equipe Assurance Qualite de Meridian Labs ?

- judge: Date in system answer is incorrect; reference states April 2025.
- expected sources: TEAM-QA-MRD-020
- not retrieved: -
- answer: L'équipe Assurance Qualité de Meridian Labs est composée de quatre collaborateurs [Source: TEAM-QA-MRD-020.pdf].

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

