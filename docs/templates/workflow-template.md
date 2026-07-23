# Workflow: [Название фичи/модуля]
**Дата начала:** YYYY-MM-DD
**Статус:** [Не начато | В работе | Завершено]
**Связанная спецификация:** [Ссылка на концепцию или SRS]
**Версия спецификации:** [Текущая версия, например 1.0]

## Этапы

### 1. Business Analysis (BA)
- [ ] **Концепция** — `docs/specs/<module>/01-concept-<module>.md`
- [ ] **Use cases** — `docs/specs/<module>/02-use-cases-<module>.md` (минимум 1 UC)
- [ ] **SRS** — `docs/specs/<module>/04-srs-<module>.md` (если есть функциональные требования)
- [ ] **RTM** — `docs/specs/<module>/rtm.md` (обновляется при изменении требований)
- [ ] **Stage-output** — `docs/temp/<module>/<module>-ba-<дата>.md`
- [ ] UI-спецификация — `docs/specs/<module>/05-ui-<module>.md`
**Проверки:**
- [ ] Все обязательные артефакты созданы/обновлены
- [ ] Контекст передан Architect через `@context_transfer`

### 2. Architecture Design (Architect)
- [ ] **ADR** — `docs/adr/adr-<N>-<title>.md` (если есть архитектурное решение)
- [ ] **Доменная модель** — `docs/specs/<module>/03-domain-<module>.md` (если требуется)
- [ ] **Stage-output** — `docs/temp/<module>/<module>-arch-<дата>.md`
- [ ] Выбор паттернов, оценка влияния на NFR
**Проверки:**
- [ ] ADR согласован с BA и Developer
- [ ] Контекст передан Developer через `@context_transfer`

### 3. Implementation (Developer)
- [ ] **Код** — `src/<module>/` реализован согласно спецификациям
- [ ] **Unit-тесты** — `tests/<module>/` покрывают ≥80% новой логики
- [ ] **Stage-output** — `docs/temp/<module>/<module>-impl-<дата>.md`
- [ ] Интеграционные тесты
- [ ] Документация API (OpenAPI/gRPC)
**Проверки:**
- [ ] Код проходит линтеры и базовые проверки
- [ ] Контекст передан QA через `@context_transfer`

### 4. Quality Assurance (QA)
- [ ] **Stage-output** — `docs/temp/<module>/<module>-qa-<дата>.md` с описанием:
  - Результаты проверки уязвимостей (SAST, dependency scan)
  - Минимум 3 граничных случая
  - Покрытие тестами (≥80% новая логика, ≥60% изменённая)
- [ ] Нагрузочное тестирование
- [ ] Безопасность (DAST, пентест)
**Проверки:**
- [ ] Критических/высоких уязвимостей нет
- [ ] Контекст передан DevOps через `@context_transfer`

### 5. Documentation & Environment (DevOps)
- [ ] **README** — обновлён (инструкции по запуску/конфигурации)
- [ ] **env.example** — синхронизирован с реальными переменными
- [ ] **Stage-output** — `docs/temp/<module>/<module>-docs-<дата>.md`
- [ ] MkDocs — документация сгенерирована
- [ ] CI/CD — пайплайны проходят
- [ ] Dockerfile / docker-compose
**Проверки:**
- [ ] Все обязательные артефакты созданы/обновлены
- [ ] Контекст передан BA (для закрытия фичи)

## Итог
- [ ] Все этапы завершены
- [ ] Временные файлы архивированы/удалены
- [ ] Задача закрыта

## Заметки
[Свободное поле для заметок по ходу выполнения]