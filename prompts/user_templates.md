# User Templates

Example natural-language requests the agent understands. Pass them as a single
CLI argument, e.g.:

```bash
uv run python main.py "создай заявку: не работает VPN, приоритет высокий"
```

## Create a task

```text
создай заявку: не работает VPN, приоритет высокий
```

```text
create a task: printer is broken, priority normal
```

## Get a task

```text
покажи заявку 1
```

```text
get task 3
```

## Update status

```text
переведи заявку 1 в статус in_progress
```

```text
mark task 2 as resolved
```

## List tasks

```text
покажи все заявки
```

```text
list tasks with priority high
```

```text
покажи заявки со статусом new
```

## Get stats

```text
покажи статистику по заявкам
```

```text
show task stats
```

## Unsupported request

These are NOT task-API operations, so the agent returns `Status: error`:

```text
какая погода в Москве?
```

```text
tell me a joke
```
