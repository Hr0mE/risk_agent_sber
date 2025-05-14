# Цепочки выполнения нод
Набор нод и последовательность их исполнения. Некоторая часть переходов (через goto) указана в [условных переходах](../edges/README.md)

## Файловая структура
chains/                      
├── [`base.py`](base.py)                 -- Абстракция для построения цепочек (базовый класс)\
├── [`faq_chain.py`](faq_chain.py)            -- Цепочка извлечения частозадаваемых вопросов\
├── [`full_chain.py`](full_chain.py)           -- Цепочка из подграфа манеры, FAQ, веб- и rag-поиска\
├── [`manner_chain.py`](manner_chain.py)         -- Цепочка извлечения манеры общения пользователя\
├── [`only_memory_chain.py`](only_memory_chain.py)    -- Цепочка из подграфа манеры и FAQ\
├── [`only_search_chain.py`](only_search_chain.py)    -- Цепочка из подграфа веб- и rag-поиска\
└── [`rag_chain.py`](rag_chain.py)            -- Цепочка из подграфа rag-поиска

## 🧩 Ключевые компоненты
- `base.py`                 -- Доступ через класс `BaseChain`
- `full_chain.py`           -- Доступ через класс `FullExecutionChain`

