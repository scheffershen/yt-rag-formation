# RAG evaluation - noise-a

- run at: 2026-08-14T09:22:08+00:00
- api: `http://localhost:8000`
- workspace: `meridian_demo`
- eval set: `eval_set.yaml` (65 questions, 6 unanswerable)
- topk: 5, graph_topk: 20, similarity_threshold: 0.2
- judge: `gpt-4o-mini`

## Answer quality

| Metric | Value |
|---|---|
| Strict accuracy (judge = correct) | **66.2%** |
| Lenient accuracy (correct + partial) | 92.3% |
| Source hit rate (all expected docs cited) | 91.5% |
| Keyword coverage | 75.4% |
| Refusal accuracy on unanswerable | 83.3% |
| Hallucination rate on unanswerable | 0.0% |
| Latency p50 / p95 | 6.17s / 10.16s |

### By category

| Category | n | Correct | % |
|---|---|---|---|
| acronym | 3 | 3 | 100.0% |
| cross_lingual | 5 | 5 | 100.0% |
| factual | 35 | 21 | 60.0% |
| multi_hop | 9 | 4 | 44.4% |
| reference_lookup | 7 | 5 | 71.4% |
| unanswerable | 6 | 5 | 83.3% |

### Failures (22)

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

- judge: Fails to provide the specified retention duration of 35 jours.
- expected sources: PR-EXM-MRD-003
- not retrieved: -
- answer: La durée de rétention des sauvegardes n'est pas spécifiquement mentionnée dans le contexte fourni. Je ne sais pas en me basant sur les données indexées.

**q11 - partial** - Sous quel delai un cas grave de pharmacovigilance doit-il etre transmis a l'autorite competente ?

- judge: Correctly states 15 days but adds unnecessary detail about unexpected cases.
- expected sources: PR-PV-MRD-002
- not retrieved: -
- answer: Un cas grave de pharmacovigilance doit être transmis à l'autorité compétente dans un délai de 15 jours calendaires. Si le cas est grave et inattendu, le délai est réduit à 7 jours calendaires [Source: PR-PV-MRD-002.pdf].

**q13 - partial** - Qui est le lead developer de l'equipe Systemes d'Information ?

- judge: Missing mention of Ines Bouziane as supplante.
- expected sources: TEAM-ITS-MRD-001
- not retrieved: -
- answer: Le lead developer de l'équipe Systèmes d'Information est Camille Renard [Source: TEAM-ITS-MRD-001.pdf].

**q16 - partial** - Combien de risques ont ete identifies dans l'analyse de risques de MeridianCore, et combien sont majeurs ?

- judge: Missing mention of 7 non bloquants risques.
- expected sources: DR_RISKA-ITS-MRD-005
- not retrieved: -
- answer: Dans l'analyse de risques de MeridianCore, 29 risques ont été identifiés, dont 3 sont considérés comme majeurs [Source: DR_RISKA-ITS-MRD-005.pdf].

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

**q28 - partial** - Une demande d'information medicale decrivant un effet indesirable - quel circuit suit-elle et sous quel delai ?

- judge: Missing specific mention of the service code PR-MI-MRD-001.
- expected sources: PR-MI-MRD-001, PR-PV-MRD-002
- not retrieved: -
- answer: Une demande d'information médicale décrivant un effet indésirable suit le circuit de traitement des cas de pharmacovigilance, tel que décrit dans la procédure PR-PV-MRD-002. Lorsqu'un effet indésirable est signalé, il est transmis au service de pharmacovigilance et fait l'objet d'un accusé de réception dans un délai de 2 jours ouvrés. Les délais de transmission aux autorités compétentes sont de 15

**q29 - partial** - Quelle mesure technique couvre le risque de perte de disponibilite de la base de donnees, et ou est-elle decrite ?

- judge: Mentions replication but fails to include quarterly restoration test and its document reference.
- expected sources: DR_RISKA-ITS-MRD-005, PR-EXM-MRD-003
- not retrieved: -
- answer: La mesure technique qui couvre le risque de perte de disponibilité de la base de données est la réplication synchrone. Cette mesure est décrite dans le document d'analyse de risques de la plateforme MeridianCore, référencé sous le nom DR_RISKA-ITS-MRD-005 [Source: DR_RISKA-ITS-MRD-005.pdf].

**q30 - partial** - Un taux d'accuse de reception de 85 pour cent a la mise en activite - est-ce un probleme, et sous quel delai doit-il etre traite ?

- judge: Missing specific non-conformity classification and 90-day action closure requirement.
- expected sources: PR-QA-MRD-001, PR-QA-MRD-009
- not retrieved: PR-QA-MRD-001
- answer: Un taux d'accusé de réception de 85 pour cent à la mise en activité peut être considéré comme un problème, car il est en dessous du seuil de conformité de 90 pour cent requis pour la mise en activité des documents. Ce taux doit être traité rapidement, et des mesures de réduction du risque, comme le contrôle automatisé du taux d'accusé de réception, devraient être mises en place. L'analyse des risq

**q31 - partial** - Quelles anomalies detectees lors de la revue des pistes d'audit doivent-elles etre traitees, et selon quelle procedure ?

- judge: Correct procedure mentioned, but additional details make it incomplete compared to the reference.
- expected sources: SOP-QA-MRD-015, PR-QA-MRD-009
- not retrieved: SOP-QA-MRD-015
- answer: Les anomalies détectées lors de la revue des pistes d'audit doivent être traitées en ouvrant une non-conformité, qui peut être classée comme majeure ou mineure. La procédure PR-QA-MRD-009 définit que toute non-conformité doit être classée par le Responsable Assurance Qualité dans les deux jours ouvrés suivant sa détection. Les non-conformités majeures doivent être traitées dans un délai de 45 jour

**q41 - partial** - Quelle est la procedure de rappel de lot en cas de defaut produit ?

- judge: Provides related procedures but does not directly answer the recall process.
- expected sources: (none)
- not retrieved: -
- answer: La procédure de rappel de lot en cas de défaut produit n'est pas spécifiquement décrite dans les documents fournis. Cependant, il est mentionné que les réclamations clients concernant la qualité du service sont traitées selon la procédure PR-CLI-MRD-013, et que les non-conformités, qu'elles soient internes ou externes, sont gérées selon la procédure PR-QA-MRD-009. En cas de non-conformité majeure,

**q46 - incorrect** - Sous quel delai un fournisseur critique doit-il notifier un incident de securite a Meridian Labs ?

- judge: States 24 hours instead of the correct 48 hours.
- expected sources: PR-ACH-MRD-007
- not retrieved: -
- answer: Un fournisseur critique doit notifier un incident de sécurité à Meridian Labs dans un délai de 24 heures [Source: PR-ITS-MRD-016.pdf].

**q52 - incorrect** - Quel est l'objectif de reprise (RTO) retenu pour la messagerie et les outils collaboratifs ?

- judge: RTO stated as 4 hours instead of the correct 8 hours.
- expected sources: PR-EXM-MRD-014
- not retrieved: -
- answer: L'objectif de reprise (RTO) retenu pour la messagerie et les outils collaboratifs est fixé à 4 heures [Source: DR_RISKA-ITS-MRD-005.pdf].

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

- judge: Missing mention of classification in the answer.
- expected sources: PR-QA-MRD-012
- not retrieved: -
- answer: La procédure PR-QA-MRD-012 couvre l'analyse d'impact et le circuit de validation pour tout changement affectant les processus, systèmes ou organisation de Meridian Labs, en mettant l'accent sur leur impact sur la qualité et la conformité. Les changements sont classés en mineurs, majeurs et urgents, chacun ayant des exigences spécifiques de validation et d'analyse d'impact, avec une vérification po

**q63 - partial** - Une reclamation client critique donne-t-elle lieu a une non-conformite, et sous quel delai le client recoit-il une reponse ?

- judge: Missing specific reference to non-conformity code PR-QA-MRD-009.
- expected sources: PR-CLI-MRD-013, PR-QA-MRD-009
- not retrieved: -
- answer: Oui, une réclamation client critique peut donner lieu à une non-conformité. Le client reçoit une réponse formelle dans un délai de 10 jours ouvrés pour une réclamation critique [Source: PR-CLI-MRD-013.pdf].

