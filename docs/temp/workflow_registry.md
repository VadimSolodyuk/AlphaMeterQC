# Workflow registry
Реестр для отслеживания stage output.

| Stage Output | Наименование работ/модуля/фичи | Status |
|--------------|--------------------------------|--------|
| ext_alphaSrv | служба динамической оптимизации параметров опроса ТУ | A |


> Пояснения:
> Stage Output: имя файла, содержащего актуальную информацию о workflow, в формате `<module>[_<feature>].md`, который создается в `docs/temp/` по шаблону `docs/templates/stage-output-template.md`.
> Status: [`A` - active, `C` - completed].
> Создание: скопировать шаблон, заполнить заголовок, добавить строку в Registry со статусом A.