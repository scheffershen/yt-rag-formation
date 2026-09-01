# RAG evaluation - lesson-4-answer

- run at: 2026-08-15T19:28:55+00:00
- api: `http://localhost:8000`
- workspace: `meridian_demo`
- eval set: `eval_set.yaml` (65 questions, 6 unanswerable)
- topk: 5, graph_topk: 20, similarity_threshold: 0.2
- judge: `gpt-4o-mini`

## Answer quality

| Metric | Value |
|---|---|
| Strict accuracy (judge = correct) | **66.2%** |
| Lenient accuracy (correct + partial) | 89.2% |
| Source hit rate (all expected docs cited) | 91.5% |
| Keyword coverage | 72.0% |
| Refusal accuracy on unanswerable | 83.3% |
| Hallucination rate on unanswerable | 16.7% |
| Latency p50 / p95 | 3.41s / 4.95s |

### By category

| Category | n | Correct | % |
|---|---|---|---|
| acronym | 3 | 3 | 100.0% |
| cross_lingual | 5 | 5 | 100.0% |
| factual | 35 | 22 | 62.9% |
| multi_hop | 9 | 3 | 33.3% |
| reference_lookup | 7 | 5 | 71.4% |
| unanswerable | 6 | 5 | 83.3% |

### Failures (22)

**q01 - partial** - Quel est le delai de cloture d'un plan d'action pour une non-conformite majeure ?

- judge: Missing validation requirement from the Responsible AQ and Direction.
- expected sources: PR-QA-MRD-009
- not retrieved: -
- answer: Le délai de clôture d'un plan d'action pour une non-conformité majeure est de 45 jours calendaires [Source: PR-QA-MRD-009.pdf].

**q06 - partial** - Quels sont les indicateurs de performance du processus d'information medicale ?

- judge: Missing satisfaction score of 4.2 on 5.
- expected sources: PR-MI-MRD-001
- not retrieved: -
- answer: Les indicateurs de performance du processus d'information médicale chez Meridian Labs incluent :

1. Taux de réponse sous 24 heures : supérieur ou égal à 95 %.
2. Délai moyen de réponse : inférieur ou égal à 8 heures.
3. Taux de réclamation : inférieur à 2 %.
4. Taux de traçabilité des demandes : 100 %.
5. Satisfaction déclarée des demandeurs : à évaluer.

Ces indicateurs sont revus mensuellement

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

- judge: Does not provide the specified duration of retention.
- expected sources: PR-EXM-MRD-003
- not retrieved: -
- answer: La durée de conservation des enregistrements qualité de Meridian Labs est spécifiée dans la procédure PR-QA-MRD-017, mais le contexte ne fournit pas de détails précis sur cette durée. Je ne sais pas basée sur les données indexées.

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

**q18 - partial** - Quelle quantite de memoire vive est requise au minimum pour un poste client MeridianCore ?

- judge: Missing the recommended 32 Go of mémoire vive.
- expected sources: FT-EXM-MRD-008
- not retrieved: -
- answer: La quantité de mémoire vive requise au minimum pour un poste client MeridianCore est de 16 Go [Source: FT-EXM-MRD-008.pdf].

**q19 - partial** - Combien de temps un acces exceptionnel peut-il rester actif ?

- judge: Missing mention of automatic revocation after expiration.
- expected sources: PR-ITS-MRD-004
- not retrieved: -
- answer: Un accès exceptionnel peut rester actif pendant 72 heures avec validation du RSSI [Source: PR-ITS-MRD-004.pdf].

**q24 - incorrect** - Qu'est-ce qui a change entre la V3 et la V4 de PR-QA-MRD-009 ?

- judge: Fails to provide any relevant information about the changes.
- expected sources: PR-QA-MRD-009
- not retrieved: -
- answer: Je ne sais pas basé sur les données indexées.

**q27 - partial** - Que se passe-t-il si un meme processus accumule plus de deux non-conformites majeures dans un trimestre ?

- judge: Missing mention of the internal audit target opening.
- expected sources: PR-QA-MRD-009, PR-QA-MRD-010
- not retrieved: PR-QA-MRD-010
- answer: Si un même processus accumule plus de deux non-conformités majeures dans un trimestre, cela déclenche une revue exceptionnelle par la Direction [Source: PR-QA-MRD-009.pdf].

**q28 - partial** - Une demande d'information medicale decrivant un effet indesirable - quel circuit suit-elle et sous quel delai ?

- judge: Missing mention of transmission to pharmacovigilance without delay.
- expected sources: PR-MI-MRD-001, PR-PV-MRD-002
- not retrieved: -
- answer: Une demande d'information médicale décrivant un effet indésirable suit le circuit de traitement des cas de pharmacovigilance, tel que décrit dans la procédure PR-PV-MRD-002. Lorsqu'un effet indésirable est signalé, il fait l'objet d'un accusé de réception envoyé au notificateur dans un délai de 2 jours ouvrés. Ensuite, les délais de transmission aux autorités compétentes sont de 15 jours calendair

**q29 - incorrect** - Quelle mesure technique couvre le risque de perte de disponibilite de la base de donnees, et ou est-elle decrite ?

- judge: Mentions a different measure and source, contradicting the reference answer.
- expected sources: DR_RISKA-ITS-MRD-005, PR-EXM-MRD-003
- not retrieved: -
- answer: La mesure technique qui couvre le risque de perte de disponibilité de la base de données est la réplication synchrone. Cette mesure est décrite dans le dossier d'analyse de risques de la plateforme MeridianCore, référencé sous DR_RISKA-ITS-MRD-005 [Source: DR_RISKA-ITS-MRD-005.pdf].

**q30 - partial** - Un taux d'accuse de reception de 85 pour cent a la mise en activite - est-ce un probleme, et sous quel delai doit-il etre traite ?

- judge: Mentions a problem but lacks specific non-conformity classification and 90-day action plan.
- expected sources: PR-QA-MRD-001, PR-QA-MRD-009
- not retrieved: PR-QA-MRD-001
- answer: Un taux d'accusé de réception de 85 % à la mise en activité peut être considéré comme un problème, surtout si cela affecte la qualité du service rendu. Selon la procédure PR-CLI-MRD-013, les réclamations doivent être traitées dans des délais spécifiques, avec une réponse formelle fournie dans les 10 à 20 jours ouvrés selon la criticité de la réclamation [Source: PR-CLI-MRD-013.pdf]. Il est donc im

**q31 - partial** - Quelles anomalies detectees lors de la revue des pistes d'audit doivent-elles etre traitees, et selon quelle procedure ?

- judge: Mentions procedure but lacks the specific opening of non-conformity.
- expected sources: SOP-QA-MRD-015, PR-QA-MRD-009
- not retrieved: SOP-QA-MRD-015
- answer: Les anomalies détectées lors de la revue des pistes d'audit doivent être traitées selon la procédure PR-QA-MRD-009, qui définit le traitement des non-conformités détectées en interne ou signalées par un client. Ces non-conformités sont classées comme majeures ou mineures, avec des délais de clôture respectifs de 45 jours pour les majeures et 90 jours pour les mineures. Une vérification de l'effica

**q41 - incorrect** - Quelle est la procedure de rappel de lot en cas de defaut produit ?

- judge: The answer provides details not found in the indexed documents.
- expected sources: (none)
- not retrieved: -
- answer: La procédure de rappel de lot en cas de défaut produit est définie dans la procédure PR-QA-MRD-009, qui traite des non-conformités détectées en interne ou signalées par un client. En cas de non-conformité majeure, le client concerné est informé dans un délai maximum de 24 heures après la classification. Les non-conformités sont classées majeures ou mineures, avec des délais de clôture respectifs d

**q46 - incorrect** - Sous quel delai un fournisseur critique doit-il notifier un incident de securite a Meridian Labs ?

- judge: States 24 hours instead of the correct 48 hours.
- expected sources: PR-ACH-MRD-007
- not retrieved: -
- answer: Un fournisseur critique doit notifier un incident de sécurité à Meridian Labs dans un délai de 24 heures [Source: PR-ITS-MRD-016.pdf].

**q51 - incorrect** - Combien de temps un compte-rendu d'audit interne est-il conserve ?

- judge: Fails to provide the requested fact about the duration of retention.
- expected sources: PR-QA-MRD-017
- not retrieved: -
- answer: Je ne sais pas en fonction des données indexées.

**q52 - incorrect** - Quel est l'objectif de reprise (RTO) retenu pour la messagerie et les outils collaboratifs ?

- judge: RTO stated as 4 hours instead of 8 hours.
- expected sources: PR-EXM-MRD-014
- not retrieved: -
- answer: L'objectif de reprise (RTO) retenu pour la messagerie et les outils collaboratifs est de 4 heures, avec un objectif de point de reprise (RPO) de 1 heure, vérifiés annuellement [Source: DR_RISKA-ITS-MRD-005.pdf].

**q58 - partial** - Combien de risques ont ete identifies dans l'analyse de risques du processus de gestion documentaire ?

- judge: Missing mention of the 2 majeurs risks identified.
- expected sources: DR_RISKA-QA-MRD-022
- not retrieved: -
- answer: Quatorze risques ont été identifiés dans l'analyse de risques du processus de gestion documentaire [Source: DR_RISKA-QA-MRD-022.pdf].

**q60 - partial** - Que couvre la procedure PR-QA-MRD-012 ?

- judge: Missing mention of classification in the system answer.
- expected sources: PR-QA-MRD-012
- not retrieved: -
- answer: La procédure PR-QA-MRD-012 couvre l'analyse d'impact et le circuit de validation pour tout changement affectant les processus, systèmes ou organisation de Meridian Labs, en mettant l'accent sur la qualité et la conformité. Les changements sont classés en mineurs, majeurs et urgents, chacun ayant des exigences spécifiques de validation et d'analyse d'impact, avec une vérification post-implémentatio

**q63 - partial** - Une reclamation client critique donne-t-elle lieu a une non-conformite, et sous quel delai le client recoit-il une reponse ?

- judge: Missing explicit mention of non-conformity opening and lacks clarity on the procedure reference.
- expected sources: PR-CLI-MRD-013, PR-QA-MRD-009
- not retrieved: -
- answer: Une réclamation client critique peut donner lieu à une non-conformité si elle révèle une défaillance de contrôle, selon la procédure PR-QA-MRD-009. Le client reçoit une réponse formelle dans un délai de 10 jours ouvrés pour une réclamation critique [Source: PR-CLI-MRD-013.pdf].

