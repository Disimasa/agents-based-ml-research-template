# Research

Ваши артефакты — то, что агент пишет **для вас**, а не служебные файлы pipeline.

| Путь | Для кого | Содержание |
|------|----------|------------|
| `methodology.md` | **Вы** | План методологии |
| `decision_log.md` | **Вы** | Журнал решений |
| `literature/` | **Вы** | Карточки статей (`results/*.json`), сводки |
| `to_human/` | **Вы** | Краткие отчёты (autonomous) |
| `manuscript/draft.md` | **Вы** | Черновик статьи |

Служебное состояние pipeline — `runtime/state/` (YAML, benchmark JSON, literature outlines, revision log). Шаблоны — `runtime/templates/`.

Код обучения — `src/`, конфиги — `configs/`. Агенты: [AGENTS.md](../AGENTS.md).
