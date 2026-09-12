# Programme du cours

## Construire un chatbot RAG QA d'entreprise fiable

**Format :** 16 leçons courtes, basées sur la pratique  
**Rythme :** À votre propre rythme. Commencez par n'importe quelle leçon, dans n'importe quel ordre, quand cela vous convient — aucun calendrier, et aucune progression ni date par apprenant n'est suivie dans ce dépôt.  
**Portée linguistique :** Anglais, français et chinois — voir [README.md](README.md) et [README_ZH.md](README_ZH.md)  
**Environnement d'apprentissage :** `rag-formation`  
**Environnement de démonstration :** `demo`

## Mission du cours

Construire un prototype technique fiable pour les employés, les équipes qualité et réglementaires, le support client, les fournisseurs et les auditeurs. Le prototype doit répondre aux questions sur les procédures et les politiques avec des citations, rechercher dans les questionnaires fournisseurs, et refuser de répondre aux questions non étayées par les documents indexés.

Ce chatbot est l'exemple d'application du cours, pas son public — le cours lui-même s'adresse à des débutants qui apprennent à construire des systèmes RAG de niveau entreprise.

## Comment fonctionne le cours

Chaque leçon est courte et produit un résultat concret :

1. N'apprendre que les concepts nécessaires à la tâche en cours.
2. Pratiquer avec le corpus de démonstration anonymisé de Meridian Labs.
3. Examiner les preuves et les résultats d'évaluation.
4. Appliquer l'enseignement tiré à la prochaine décision d'ingénierie.

Prenez vos propres notes au fil de l'eau, sous la forme qui vous convient — ce dépôt ne suit ni la progression par apprenant, ni les dates, ni l'état d'avancement ; rien ici ne suppose que vous êtes à une leçon précise à un moment précis.

Le cours évalue délibérément séparément la **récupération**, la **génération**, les **citations**, le **comportement de refus** et les **opérations**.

---

## Phase 1 — Fondations et mesure

### Leçon 1 — De la question de l'employé à la réponse citée

**Objectif :** Comprendre le RAG comme un pipeline et distinguer les échecs de récupération des échecs de génération.  
**Pratique :** Exécuter `eval.py verify` et `test_scoring.py` ; diagnostiquer q30 et q01.  
**Livrable :** Première leçon et aide-mémoire qualité.

### Leçon 2 — Suivre une question à travers le vrai code

**Objectif :** Suivre une question à travers l'API, les fonctions de recherche, l'assemblage du contexte, le prompt et la réponse.  
**Pratique :** Reconstituer la chaîne d'appels (`routes/qa.py` → `qa_service.py` → `search.py` → `utils.py`) à partir du schéma du chemin de requête, puis la vérifier sur l'API de démonstration en cours d'exécution.  
**Livrable :** Une traçabilité système d'une page pour une question.  
**Leçon :** [Ouvrir la leçon 2](lessons/fr/0002-trace-one-question.html)

### Leçon 3 — Construire un jeu d'évaluation fiable

**Objectif :** Comprendre la vérité terrain, les questions répondables versus non répondables, les sources attendues et les faits requis.  
**Pratique :** Examiner `eval_set.yaml` et expliquer pourquoi une correspondance de récupération basée uniquement sur les métadonnées évite les faux positifs de références croisées.  
**Livrable :** Liste de vérification de conception d'un jeu d'évaluation.  
**Leçon :** [Ouvrir la leçon 3](lessons/fr/0003-build-a-trustworthy-evaluation-set.html)

### Leçon 4 — Établir la base de référence du MVP

**Objectif :** Exécuter une évaluation en direct et lire le rapport en ingénieur.  
**Pratique :** Démarrer la pile de démonstration isolée, exécuter les évaluations de récupération et de réponse, et comparer les résultats à la base de référence historique.  
**Livrable :** Un rapport de référence actuel avec des cas d'échec connus.  
**Leçon :** [Ouvrir la leçon 4](lessons/fr/0004-establish-the-mvp-baseline.html)

**Jalon de la phase 1 :** Vous pouvez expliquer ce que fait le système et appuyer chaque affirmation de qualité sur une métrique.

---

## Phase 2 — Ingénierie de la récupération

### Leçon 5 — Recherche sémantique, recherche par mots-clés et récupération hybride

**Objectif :** Comprendre pourquoi les identifiants de procédures, les acronymes, les noms, les dates et les concepts nécessitent des signaux de récupération différents.  
**Pratique :** Comparer les résultats vectoriels de Qdrant aux résultats en texte intégral de Meilisearch en utilisant le mode de récupération.  
**Livrable :** Un tableau comparatif des méthodes de récupération.  
**Leçon :** [Ouvrir la leçon 5](lessons/fr/0005-semantic-keyword-and-hybrid-retrieval.html) · [Référence](reference/fr/semantic-keyword-and-hybrid-retrieval-cheatsheet.html)

### Leçon 6 — Découpage et structure des documents

**Objectif :** Apprendre comment la taille des blocs, le chevauchement, les titres, les tableaux et les limites de documents affectent la récupération.  
**Pratique :** Examiner une question en échec et ses blocs indexés ; relier l'échec au pipeline d'ingestion.  
**Livrable :** Fiche de décision de découpage pour le corpus de démonstration.  
**Leçon :** [Ouvrir la leçon 6](lessons/fr/0006-chunking-and-document-structure.html) · [Référence](reference/fr/chunking-and-document-structure-cheatsheet.html)

### Leçon 7 — Métadonnées, filtres et limites d'accès

**Objectif :** Comprendre pourquoi les métadonnées d'entreprise, de département, de type de document, de classification, de version et de date d'effet sont essentielles pour un chatbot d'entreprise.  
**Pratique :** Cartographier les libellés actuels et concevoir des filtres pour les vues employé, fournisseur, qualité et audit.  
**Livrable :** Matrice de métadonnées et de contrôle d'accès.  
**Leçon :** [Ouvrir la leçon 7](lessons/fr/0007-metadata-filters-and-access-boundaries.html) · [Référence](reference/fr/metadata-filters-and-access-boundaries-cheatsheet.html)

### Leçon 8 — Traitement des requêtes et reclassement

**Objectif :** Améliorer les requêtes difficiles sans masquer les échecs de récupération derrière un `topk` plus large.  
**Pratique :** Tester la normalisation des requêtes, la recherche de références, la réécriture de requêtes, la déduplication des résultats et les hypothèses de reclassement.  
**Livrable :** Un petit plan d'expérimentation de récupération avec une hypothèse mesurable.  
**Leçon :** [Ouvrir la leçon 8](lessons/fr/0008-query-handling-and-reranking.html) · [Référence](reference/fr/query-handling-and-reranking-cheatsheet.html)

**Jalon de la phase 2 :** Vous pouvez expliquer pourquoi une source a été ou n'a pas été récupérée, et choisir une amélioration de récupération ciblée.

---

## Phase 3 — Génération de réponses fondées sur des preuves

### Leçon 9 — Assemblage du contexte et budgets de preuves

**Objectif :** Comprendre comment les résultats récupérés deviennent le contexte du modèle et comment la troncature peut supprimer des preuves.  
**Pratique :** Examiner `build_context()`, la survie des sources, l'ordonnancement et `max_context_chars`.  
**Livrable :** Schéma d'assemblage du contexte et recommandation de budget de preuves.  
**Leçon :** [Ouvrir la leçon 9](lessons/fr/0009-context-assembly-and-evidence-budgets.html) · [Référence](reference/fr/context-assembly-and-evidence-budgets-cheatsheet.html)

### Leçon 10 — Des prompts qui répondent uniquement à partir des preuves

**Objectif :** Concevoir des instructions pour des réponses fondées, la gestion de l'incertitude, des réponses concises et un refus explicite.  
**Pratique :** Comparer un prompt de référence à un prompt de réponse structurée sur le jeu d'évaluation.  
**Livrable :** Spécification versionnée du prompt QA.  
**Leçon :** [Ouvrir la leçon 10](lessons/fr/0010-prompts-that-answer-only-from-evidence.html) · [Référence](reference/fr/prompts-that-answer-only-from-evidence-cheatsheet.html)

### Leçon 11 — Conception des citations et fidélité aux sources

**Objectif :** Rendre les citations utiles, stables et liées aux preuves réellement montrées au modèle.  
**Pratique :** Vérifier l'identité des documents, l'identité des blocs, la déduplication des sources et les réponses multi-documents.  
**Livrable :** Contrat de citation pour le MVP.  
**Leçon :** [Ouvrir la leçon 11](lessons/fr/0011-citation-design-and-source-fidelity.html) · [Référence](reference/fr/citation-design-and-source-fidelity-cheatsheet.html)

### Leçon 12 — Refus, incertitude et contrôle des hallucinations

**Objectif :** Construire un comportement adapté aux scénarios de qualité, de réglementation et d'audit lorsque le corpus ne contient pas de réponse.  
**Pratique :** Analyser les six questions sans réponse et tester la formulation du refus, les seuils de preuve et les affirmations non étayées.  
**Livrable :** Politique de refus et cas de test de sécurité.  
**Leçon :** [Ouvrir la leçon 12](lessons/fr/0012-refusal-uncertainty-and-hallucination-control.html) · [Référence](reference/fr/refusal-uncertainty-and-hallucination-control-cheatsheet.html)

**Jalon de la phase 3 :** Vous pouvez produire une réponse concise, fondée, citée et appropriément incertaine.

---

## Phase 4 — Fiabilité et préparation au produit

### Leçon 13 — Isolation des pannes et dégradation gracieuse

**Objectif :** Comprendre ce qui devrait se passer en cas de panne de Qdrant, Meilisearch, LightRAG, des embeddings ou du LLM.  
**Pratique :** Tracer les chemins actuels de gestion des exceptions et classer les comportements de service partiel acceptables.  
**Livrable :** Matrice des pannes de dépendances.  
**Leçon :** [Ouvrir la leçon 13](lessons/fr/0013-failure-isolation-and-graceful-degradation.html) · [Référence](reference/fr/failure-isolation-and-graceful-degradation-cheatsheet.html)

### Leçon 14 — Latence, coût et observabilité

**Objectif :** Équilibrer la qualité des réponses avec le temps de réponse, le coût en tokens, les appels au graphe et la visibilité opérationnelle.  
**Pratique :** Lire les latences p50/p95, le nombre d'appels aux backends, la taille du contexte et les statistiques du modèle à partir des rapports d'évaluation.  
**Livrable :** Budget de performance du MVP et liste de vérification de télémétrie.  
**Leçon :** [Ouvrir la leçon 14](lessons/fr/0014-latency-cost-and-observability.html) · [Référence](reference/fr/latency-cost-and-observability-cheatsheet.html)

### Leçon 15 — Sécurité, permissions et limites de déploiement

**Objectif :** Empêcher le chatbot d'exposer des documents aux mauvais utilisateurs ou de divulguer des secrets et des données clients.  
**Pratique :** Revoir les libellés de locataires, les limites de l'API, le CORS, les fichiers d'environnement, la journalisation et l'isolation démo/production.  
**Livrable :** Liste de vérification des menaces et des permissions du MVP.  
**Leçon :** [Ouvrir la leçon 15](lessons/fr/0015-security-permissions-and-deployment-boundaries.html) · [Référence](reference/fr/security-permissions-and-deployment-boundaries-cheatsheet.html)

### Leçon 16 — Bilan du pilote et plan de mise en œuvre à 30 jours

**Objectif :** Transformer les preuves d'évaluation en un backlog de mise en œuvre priorisé et un plan de pilote.  
**Pratique :** Sélectionner les corrections à plus forte valeur, relancer l'évaluation, documenter les limites, et définir les critères de décision go/no-go.  
**Livrable :** Rapport de préparation du prototype et feuille de route des 30 prochains jours.  
**Leçon :** [Ouvrir la leçon 16](lessons/fr/0016-pilot-review-and-30-day-implementation-plan.html) · [Référence](reference/fr/pilot-review-and-30-day-implementation-plan-cheatsheet.html)

**Jalon de la phase 4 :** Vous disposez d'un plan de prototype défendable, de critères d'acceptation mesurables et d'un chemin priorisé vers la fiabilité en production.

---

## Ordre recommandé

Les quatre phases s'appuient conceptuellement les unes sur les autres, donc suivre 1 → 16 dans l'ordre est le chemin le plus simple la première fois. Mais rien ne l'impose : chaque leçon relie ce qu'elle suppose acquis au contenu antérieur, donc il est tout à fait possible de sauter directement à celle dont vous avez besoin — pour chercher une information, reprendre le cours en cours de route, ou passer directement à un sujet qui vous intéresse.

| Phase | Leçons | Objectif |
|---|---:|---|
| 1 | 1–4 | Fondations et référence |
| 2 | 5–8 | Récupération |
| 3 | 9–12 | Réponses fondées et citations |
| 4 | 13–16 | Fiabilité, sécurité et pilote |

Il n'y a pas de rythme attendu — une leçon en un après-midi ou une par mois fonctionnent aussi bien l'une que l'autre.

## Critères de réussite

Le cours est terminé lorsque vous pouvez :

- Expliquer le chemin complet d'une requête RAG.
- Diagnostiquer les échecs de récupération par rapport aux échecs de génération.
- Exécuter le harnais d'évaluation et lui faire confiance.
- Rendre compte séparément de la précision stricte, du taux de succès des sources, de la précision des refus, du taux d'hallucination et de la latence.
- Expliquer comment le découpage, les métadonnées, la recherche hybride, l'assemblage du contexte et le prompting affectent la qualité.
- Définir le comportement de citation et de refus pour le cas d'usage de l'entreprise.
- Produire un backlog MVP priorisé fondé sur des échecs mesurés.

## Formation continue (hors programme des 16 leçons)

### Leçon 17 — Ce qui vient après le pilote

**Objectif :** Savoir où aller une fois qu'un pilote tourne et que de vrais utilisateurs, retours et échecs commencent à apparaître.  
**Pratique :** Faire correspondre le point le plus faible de votre propre pilote au bon chapitre de `rag-formation-continue`, une série de tutoriels distincte et gratuite, écrite à partir d'une véritable expérience de production.  
**Livrable :** Un changement de préparation à la production que vous feriez ensuite, relié à une lacune précise de votre propre feuille de travail de la Leçon 16.  
**Leçon :** [Ouvrir la leçon 17](lessons/fr/0017-what-comes-after-the-pilot.html) · [rag-formation-continue sur GitHub](https://github.com/scheffershen/rag-formation-continue)

Cette leçon n'est pas numérotée dans les phases 1 à 4 ci-dessus et n'est pas requise pour les critères de réussite ci-dessous — c'est un panneau indicateur pour savoir quoi lire ensuite une fois le cours terminé, pas une étape notée de plus.

## Fichiers de référence principaux

- [Ressources](RESOURCES_FR.md)
- [Aide-mémoire qualité RAG](reference/fr/rag-quality-cheatsheet.html)
- [Leçon 1](lessons/fr/0001-from-question-to-cited-answer.html)
- [README du harnais de démonstration](../demo/README.md)
