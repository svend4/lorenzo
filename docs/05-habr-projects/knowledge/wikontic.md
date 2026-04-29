# Wikontic: семантический граф

<!-- summary -->
> Wikontic — Алла Чепурова (AIRI, лаборатория Cognitive AI Systems) https://habr.com/ru/companies/airi/articles/1000720/ И её более ранняя статья: https://habr.com/ru/companies/airi/articles/855128/ Пай
**Проекты:** Wikontic

---



Wikontic — Алла Чепурова (AIRI, лаборатория Cognitive AI Systems) https://habr.com/ru/companies/airi/articles/1000720/ И её более ранняя статья: https://habr.com/ru/companies/airi/articles/855128/ Пайплайн построения графов знаний из текста с использованием онтологии Wikidata, дедупликацией и типизацией сущностей. Решает буквально тот же класс проблем, что у Чуяна на слое 3 (нормализация — kubernetes / k8s / кубер → одна сущность), но не через ручной skills_synonyms.yml , а через автоматическую сверку с онтологией. У Чуяна — справочник на сотню строк, который он дополняет вручную; Алла построила то, что делает это автоматически.
3.
