#!/usr/bin/env python3
import argparse
import json
import os
import sys
from dataclasses import dataclass, asdict
from datetime import datetime

DATA_FILE = "tasks.json"


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    created_at: str = ""

    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat(timespec="seconds")



def load_tasks() -> list[Task]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Task(**item) for item in raw]
    except (json.JSONDecodeError, KeyError, TypeError):
        return []


def save_tasks(tasks: list[Task]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([asdict(t) for t in tasks], f, ensure_ascii=False, indent=2)

def add_task(title: str) -> Task:
    tasks = load_tasks()
    new_id = max((t.id for t in tasks), default=0) + 1
    task = Task(id=new_id, title=title)
    tasks.append(task)
    save_tasks(tasks)
    return task


def list_tasks(pending_only: bool = False) -> list[Task]:
    tasks = load_tasks()
    if pending_only:
        return [t for t in tasks if not t.done]
    return tasks


def complete_task(task_id: int) -> bool:
    tasks = load_tasks()
    for t in tasks:
        if t.id == task_id:
            t.done = True
            save_tasks(tasks)
            return True
    return False


def delete_task(task_id: int) -> bool:
    tasks = load_tasks()
    filtered = [t for t in tasks if t.id != task_id]
    if len(filtered) == len(tasks):
        return False
    save_tasks(filtered)
    return True


def cmd_add(args):
    task = add_task(args.title)
    print(f"✅ Добавлено: [{task.id}] {task.title}")


def cmd_list(args):
    tasks = list_tasks(pending_only=args.pending)
    if not tasks:
        print("📭 Задач нет")
        return
    for t in tasks:
        mark = "✔" if t.done else " "
        print(f"[{mark}] #{t.id} {t.title}  ({t.created_at})")


def cmd_done(args):
    if complete_task(args.id):
        print(f"✅ Задача #{args.id} выполнена")
    else:
        print(f"❌ Задача #{args.id} не найдена")
        sys.exit(1)


def cmd_delete(args):
    if delete_task(args.id):
        print(f"🗑 Задача #{args.id} удалена")
    else:
        print(f"❌ Задача #{args.id} не найдена")
        sys.exit(1)



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="todo", description="Менеджер задач")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="добавить задачу")
    p_add.add_argument("title")
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="показать задачи")
    p_list.add_argument("--pending", action="store_true", help="только невыполненные")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="отметить выполненной")
    p_done.add_argument("id", type=int)
    p_done.set_defaults(func=cmd_done)

    p_del = sub.add_parser("delete", help="удалить задачу")
    p_del.add_argument("id", type=int)
    p_del.set_defaults(func=cmd_delete)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()