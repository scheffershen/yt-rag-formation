# Ressources

Ces ressources ont été choisies pour ce cours parce qu'elles expliquent la qualité du RAG, la récupération, les citations et l'évaluation à partir de sources techniques primaires ou hautement fiables.

Disponible aussi en [anglais](RESOURCES.md) et en [chinois](RESOURCES_ZH.md).

## Ressources principales

1. [OpenAI — Optimizing LLM Accuracy](https://platform.openai.com/docs/guides/optimizing-llm-accuracy)
   - Pourquoi : distingue clairement la qualité de récupération de la qualité de génération, et explique le RAG comme « récupération + génération augmentée ».
   - Utilisé dans : Leçon 1.

2. [OpenAI — Evaluation Best Practices](https://platform.openai.com/docs/guides/evaluation-best-practices)
   - Pourquoi : explique pourquoi les applications d'IA non déterministes nécessitent des évaluations structurées, et comment les concevoir.
   - Utilisé dans : Leçons 1 et 4.

3. [Qdrant — Filtering](https://qdrant.tech/documentation/search/filtering)
   - Pourquoi : pertinent pour les limites d'accès aux documents, les libellés d'entreprise, les départements, les types de documents et la récupération de données réglementées.
   - Utilisé dans : Semaine 2.

4. [Qdrant — Hybrid Search](https://qdrant.tech/documentation/search/text-search/hybrid-search)
   - Pourquoi : explique comment combiner récupération sémantique et lexicale, ce qui correspond directement à la conception Qdrant + Meilisearch de la démo.
   - Utilisé dans : Semaine 2.

5. [Anthropic — RAG glossary entry](https://docs.anthropic.com/en/docs/resources/glossary)
   - Pourquoi : définition concise du RAG et de sa dépendance à la qualité et à la pertinence des connaissances récupérées.
   - Utilisé dans : Leçon 1.

6. [Anthropic — Search results with citations](https://docs.anthropic.com/en/docs/build-with-claude/search-results)
   - Pourquoi : référence utile pour traiter l'attribution des sources comme une capacité de réponse de premier ordre.
   - Utilisé dans : Semaine 3.

7. [RAGAS paper — Automated Evaluation of Retrieval Augmented Generation](https://arxiv.org/abs/2309.15217)
   - Pourquoi : référence fondatrice pour évaluer les systèmes de génération augmentée par récupération, plutôt que de juger uniquement le texte final.
   - Utilisé dans : Semaines 3 et 4.

## Ressources locales du projet

- [`demo/README.md`](../demo/README.md) — corpus de démonstration, pile isolée, méthodologie d'évaluation et limites des métriques.
- [`demo/eval.py`](../demo/eval.py) — implémentation du scoring.
- [`demo/eval_set.yaml`](../demo/eval_set.yaml) — jeu de vérité terrain de 65 questions.
- [`demo/reports/demo-fixed.md`](../demo/reports/demo-fixed.md) — un exemple de rapport de référence.
- [Aide-mémoire du chemin de requête](reference/fr/request-path-cheatsheet.html) — l'architecture du pipeline de requête (récupération hybride, assemblage du contexte, génération de réponse), étape par étape. L'implémentation (`api/`) est la version de référence payante, elle ne fait pas partie du cours gratuit — voir `rag-formation/CLAUDE.md`.
- [Glossaire terminologique](reference/fr/glossary-cheatsheet.html) — formulations EN/ZH figées pour le découpage, le reclassement, l'hallucination, l'ancrage et le refus ; chaque leçon, aide-mémoire et animation doit s'y conformer.
