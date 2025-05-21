# Стейты и инфа о нодах
В этой дирректории хранятся все стейты, а также вся мета-инфа о нодах, нужная для унификации пользованием.

## 📁 Файловая структура
state_management\
├── [`validation_models`](../agents/state_management/validation_models/) -- Валидационные модели Pydantic \
├── [`global_state.py`](global_state.py) -- единственный стейт (пожалуйста, декомпозируйте кто-нибудь его) \
└── [`commands.py`](commands.py) -- хранение мета-инфы по нодам, в том числе названия

## 🧩 Ключевые компоненты
- [`global_state.py`](global_state.py) -- хранение всей-всей информации о графе. Доступ через `GlobalState`
- [`commands.py`](commands.py) -- доступ к `Enum` через `NodeNames`.

## 🎨 Создание своего стейта
```python
#agents/state_management/new_state.py

from typing import Dict, List
from langgraph.graph import MessagesState
from .validation_models import MannerInfo, FAQData, Question


class GlobalState(MessagesState):
    field_1: List[str]  # Можно хранить список
    field_2: str # Можно строку
    field_3: dict # Можно словарь. Много чего можно
```
## 🛠️ Использование
```python
#agents/nodes/some_mode.py

class NewNode(BaseNode):
    def __init__(self):
        ...

    def execute(self, state: GlobalState) -> Command:
        ...

        result = chain.invoke({
            "field_1": somevalue1,
            "field_2": state.get(somevalue2, ""), # достаём значения из стейта через get()
            "field_3": somevalue3,
        })

        return Command(
            # Обновляем все необходимые поля
            update={ 
                "field_1": result.field_1
            }
        )
```

## 📋 Чеклисты

**Добавление: TODO**
- [ ]
- [ ]

**Удаление:**
- [ ]
- [ ]

## ⚠️ Возможные ошибки

```bash

```
_Причина:_

_Решение:_
- [ ]
- [ ]
---

```bash

```
_Причина:_

_Решение:_
- [ ]
- [ ]
---
