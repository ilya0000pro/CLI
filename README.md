# CLI
# Todo CLI

Одностраничный менеджер задач на Python (только стандартная библиотека).

## Запуск
python todo.py add "Купить молоко"
python todo.py list --pending
python todo.py done 1

## Как устроено
- `Task` (dataclass) — модель задачи
- `load_tasks/save_tasks` — работа с tasks.json
- `add_task/list_tasks/complete_task/delete_task` — бизнес-логика
- `cmd_*` + `argparse` — CLI-интерфейс

Данные хранятся в `tasks.json`.
