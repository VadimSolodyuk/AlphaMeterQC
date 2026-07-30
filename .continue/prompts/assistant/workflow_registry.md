---
name: workflow_registry
description: Реестр для отслеживания стадий вывода (stage output) модулей и фич.
invokable: true
---

| Stage Output | Status |
|--------------|--------|

> Пояснения:
> Stage Output: имя файла в формате `<module>[_<feature>].md`, который создается в `docs/temp/` по шаблону `docs/templates/stage-output-template.md`.
> Status: [`A` - active, `C` - completed].
> Создание: скопировать шаблон, заполнить заголовок, добавить строку в Registry со статусом A. Если задача затрагивает несколько ролей, в Stage Output сразу перечислить все ожидаемые артефакты или укажи Примечания со статусом `P`.
> Завершение: когда workflow полностью реализован — изменить статус в Registry на C (предлагать пользователю удалить запись и файл).