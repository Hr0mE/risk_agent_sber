# Цепочки выполнения нод
Набор нод и последовательность их исполнения. Некоторая часть переходов (через goto) указана в [условных переходах](../edges/README.md)

## 📁 Файловая структура
chains/                      
├── [`base.py`](base.py)                 -- Абстракция для построения цепочек (базовый класс)\
├── [`faq_chain.py`](faq_chain.py)            -- Цепочка извлечения частозадаваемых вопросов\
├── [`full_chain.py`](full_chain.py)           -- Цепочка из подграфа манеры, FAQ, веб- и rag-поиска\
├── [`manner_chain.py`](manner_chain.py)         -- Цепочка извлечения манеры общения пользователя\
├── [`only_memory_chain.py`](only_memory_chain.py)    -- Цепочка из подграфа манеры и FAQ\
├── [`only_search_chain.py`](only_search_chain.py)    -- Цепочка из подграфа веб- и rag-поиска\
└── [`rag_chain.py`](rag_chain.py)            -- Цепочка из подграфа rag-поиска

## 🧩 Ключевые компоненты
- [`base.py`](base.py)                 -- Доступ через класс `BaseChain`
- [`full_chain.py`](full_chain.py)           -- Доступ через класс `FullExecutionChain`

## 🎨 Создание своей цепочки
```python
from typing import List

from agents import nodes
from .base import BaseChain


class NewChain(BaseChain):
    """Новая цепочка выполнения с некоторыми нодами"""
    
    def __init__(self):
        super().__init__()
        
        # Перечисление всех используемых нод
        node_list: List[nodes.BaseNode] = [
            nodes.SomeNode1,
            nodes.SomeNode2,
            nodes.SomeNode3
        ]
        
        # Связи между нодами в формате (откуда, куда)
        edge_list = [
            (nodes.SomeNode1, nodes.SomeNode2),
            (nodes.SomeNode2, nodes.SomeNode3)
        ]

        # Регистрация нод
        for node in node_list:
            self.add_node(name=node().get_name(), node=node().execute)
        
        # Определение связей
        for (source_edge, target_edge) in edge_list:
            self.add_edge(source_edge().get_name(), target_edge().get_name())
     
        # Настройка точек входа/выхода
        self.set_entry_point(nodes.SomeNode1().get_name())
        self.set_exit_point(nodes.SomeNode3().get_name())
```

## 📋 Чеклисты цепочек

**Создание цепочки:**
- [ ] Создать класс
  - [ ] Указать все необходимые ноды
  - [ ] Указать все связи
  - [ ] Настроить точку входа/выхода
- [ ] Экспортировать цепочку в [`__init__.py`](./__init__.py)
  - [ ] Добавить `from .new_chain.py import NewChain `
  - [ ] Добавить `"NewChain"` в список `__all__`

**Удаление цепочки:**
- [ ] Удалить файл цепочки `new_chain.py`
- [ ] Удалить цепочку из [`__init__.py`](./__init__.py)
  - [ ] Стереть `from .new_chain.py import NewChain `
  - [ ] Стереть `"NewChain"` из списка `__all__`
- [ ] Проверить, что цепочка не используется в [`base_agent.py`](../base_agent.py)

## ⚠️ Возможные ошибки

```bash
AttributeError: module 'agents.nodes' has no attribute 'SomeOtherNode'
```
_Причина:_ не найдено ноды `SomeOtherNode`

_Решение:_ 
- [ ] Проверить наличие ноды `SomeOtherNode` в [`nodes/__init__.py`](../nodes/__init__.py)
- [ ] Проверить наличие регистрации ноды `SomeOtherNode` в `NodeNames` в [`state_management/commands.py`](../state_management/commands.py)
---
```bash
ValueError: Node 'SomeNode' not registered
```
_Причина:_ Попытка использовать ноду, которая не внесена в `node_list` цепочки

_Решение:_ 
- [ ] Проверить наличие ноды `SomeNode` в `node_list`
- [ ] Проверить корректность работы `BaseChain.add_node()`
- [ ] Проверить корректность работы `BaseChain.set_entry_point()`
- [ ] Проверить корректность работы `BaseChain.set_exit_point()`
---
```bash
ValueError: Entry point must be defined
```
_Причина:_ Не установлена входная точка в граф

_Решение:_ 
- [ ] Проверить наличие `self.set_entry_point(nodes.QuestionDecompositionNode().get_name())` в классе цепочки `NewChain`
- [ ] Проверить корректность работы `BaseNode.set_entry_point()`
- [ ] Проверить корректность работы `BaseNode._validate()`
---
```bash
ValueError: Exit point must be defined
```
_Причина:_ Не установлена выходная точка из графа

_Решение:_ 
- [ ] Проверить наличие `self.set_exit_point(nodes.SomeNode().get_name())` в классе цепочки `NewChain`
- [ ] Проверить корректность работы `BaseNode.set_exit_point()`
- [ ] Проверить корректность работы `BaseNode._validate()`