# Условия перехода между нодами
Условные переходы, которые используется обычно в `goto` при обновлении состояния графа. Нужен в случае наличия развилки.

## 📁 Файловая структура
edges/\
└── [`conditions.py`](conditions.py) -- Основной класс с условиями.

## 🧩 Ключевые компоненты
- [`conditions.py`](conditions.py) -- Доступ через класс `ConditionHandler`. Доступ к роутеру через `ConditionHandler.evaluate_transition()`

## 🎨 Создание своего хэндлера с условными переходами
```python
#agents/chain/new_conditions.py
from agents.state_management import (
    NodeNames,
    SomeNodeModel
)

class ConditionHandler:
    @staticmethod # Создание обработчика
    def handle_some_node(decision: SomeNodeModel) -> NodeNames:
        next_node: str = decision.final_decision

        # Проверяем необходимые условия для переходов
        if next_node == NodeNames.SOME_NODE_2 and not decision.some_field:
            return NodeNames.SOME_NODE_3.value

        return next_node

    @classmethod # Главный роутер для обработки переходов между нодами
    def evaluate_transition(cls, source_node: NodeNames, result: object) -> NodeNames:

        if source_node == NodeNames.SOME: # Добавление условия в роутер

            if not isinstance(result, SomeNodeModel): # Проверка на соответствие типа вывода ожидаемому
                raise TypeError("SomeNode transition requires agents.state_management.some_node_model.SomeNodeModel output")

            return cls.handle_some_node(result)


        raise NotImplementedError(f"Transition from {source_node} not implemented")
```
## 🛠️ Использование
```python
#agents/nodes/some_node.py
#... some imports ...

class SomeNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.SOME.value)
        self.parser = PydanticOutputParser(pydantic_object=output_model)
        self.model = model(config=model_config())

    def execute(self, state: GlobalState) -> Command:
        ...

        chain = prompt | self.model | self.parser

        result = chain.invoke({...})

        return Command(
            update={...},
            goto = ConditionHandler.evaluate_transition(
                source_node=self.name,
                result=result
            )
        )
```

## 📋 Чеклисты условий перехода

**Добавление нового условия в существующий хэндлер:**
- [ ] Создать валидационную модель (pydantic)
  - [ ] Убедиться, что в модели есть поле final_decision или его аналог. [Подробнее о валидационных моделях](../state_management/README.md)
  - [ ] Занести модель в [`__init__.py`](../state_management/__init__.py)
- [ ] Убедиться в наличии нод, к которым нужно сделать переход. [Подробнее о нодах](../nodes/README.md#-чеклисты)
- [ ] Отредактировать `ConditionHandler`
  - [ ] Добавить условие в роутер `evaluate_transition()`
  - [ ] Добавить `@staticmethod`-обработчик
- [ ] Использовать условие в `Command(goto=ConditionHandler(...))` ноде
---

**Удаление условия:**
- [ ] Удалить все упоминания в `ConditionHandler`
- [ ] Удалить валидационную модель и упоминание в [`__init__.py`](../state_management/__init__.py)
- [ ] Удалить вызов в `Command(goto=ConditionHandler(...))` в ноде

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
