# Utils
Вспомогательные скрипты для работы основного агента (не тулзы)

## 📁 Файловая структура
utils/\
├── [`actualize_rag_db.py`](./actualize_rag_db.py) -- Создаёт индекс документов для последующего RAG. \
├── [`similarity_of_topics.py`](./similarity_of_topics.py) -- Поиск схожей темы по смыслу среди существующих тем \
├── [`cache.py`](./cache.py) -- (не реализовано) Кэширование часто задаваемых вопросов. \
├── [`logger.py`](./logger.py) -- (не реализовано) Логирование всего-всего. \
└── [`prompt_loader.py`](./prompt_loader.py) -- (не реализовано) Загрузка промптов из файлов.

## 🧩 Ключевые компоненты
- [`actualize_rag_db.py`](./actualize_rag_db.py) -- Запускается вручную. \
- [`similarity_of_topics.py`](./similarity_of_topics.py) -- Используется в какой-то ноде)) \