# Ноды графа
Здесь хранятся все ноды, которые могут в дальнейшем быть использованы в [цепочках](../chains/)

## 📁 Файловая структура
nodes/\
├── [`base.py`](base.py) -- Абстракция для создания своих нод \
├── [`critique.py`](critique.py) -- Нода критика (хотя, скорее, валидатора) полноты ответа \
├── [`extract_conversation_style.py`](extract_conversation_style.py) -- Нода извлечения стиля общения с пользователем \
├── [`extract_faq.py`](extract_faq.py) -- Нода извлечения часто-задаваемых вопросов от пользователя \
├── [`finalize.py`](finalize.py) -- Собирает результат воедино из разных источников, применяя ограничения и манеру общения с пользователем \
├── [`first_step.py`](first_step.py) -- Нода, определяющая, нужен ли вообще поиск информации или можно ответить сразу \
├── [`get_memory_faq.py`](get_memory_faq.py) -- Нода, достающая из памяти вопросы, которые уже задавал пользователь \
├── [`get_memory_manner.py`](get_memory_manner.py) -- Нода, достающая из памяти манеру общения с пользователем  \
├── [`question_decomposition.py`](question_decomposition.py) -- Разбиение вопроса пользователя на подвопросы \
├── [`rag.py`](rag.py) -- Нода поиска по внутренней базе документов \
├── [`reason.py`](reason.py) -- Нода, решающая, какие шаги стоит предпринять для наилучшего решения вопроса \
├── [`search.py`](search.py) -- Нода поиска в интернете \
├── [`store_question.py`](store_question.py) -- Нода сохранения вопроса в БД \
├── [`write.py`](write.py) -- Нода, переформулирующая WEB- и RAG-поиск в человеко-читаемый текст \
├── [`write_faq.py`](write_faq.py) -- ??? \
└── [`write_manner_to_memory.py`](write_manner_to_memory.py) -- Нода сохранения манеры пользователя в БД  

## 🧩 Ключевые компоненты
- [`base.py`](base.py) -- Позволяет реализовывать свои ноды. Доступ через класс `BaseNode`. 
- [`question_decomposition.py`](question_decomposition.py) -- Первичный анализ вопроса. Доступ через класс `QuestionDecompositionNode`.
- [`first_step.py`](first_step.py) -- Выбор стратегии ответа. Доступ через класс `FirstStepNode`. 
- [`finalize.py`](finalize.py) -- Резюме всех размышлений. Доступ через класс `FinalizeNode`. 


## 🎨 Создание своей ноды
```python
#agents/nodes/new_node.py

from langgraph.types import Command
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from agents.nodes.base import BaseNode
from agents.state_management import GlobalState, NodeNames
from agents.state_management import CritiqueDecisionModel

from models import MistralLargeModel as model
from models.config import MistralLargeAPIConfig as model_config

from agents.prompts.base import PromptManager
from agents.edges.conditions import ConditionHandler

#ctrl + f и заменить все 'New' на нужное имя
class NewNode(BaseNode):
    def __init__(self):
        super().__init__(name=NodeNames.New.value)
        # Если валидатора выходных данных нет, то self.parser = StrOutputParser()
        self.parser = PydanticOutputParser(pydantic_object=NewModel)
        self.prompt_manager = PromptManager()
        self.prompt_template = "system/New.j2"
        self.model = model(config=model_config())

    def execute(self, state: GlobalState) -> Command:
        prompt = self.prompt_manager.create_chat_raw_prompt(self.prompt_template)
        chain = prompt | self.model | self.parser

        result = chain.invoke({})

        return Command(
            update={},
            # Только если в данной ноде есть ветвление
            goto=ConditionHandler.evaluate_transition(source_node=self.name, result=result),
        )

```
## 🛠️ Использование
```python
#agents/chains/some_chain.py

from .base import BaseChain
from typing import List
from agents import nodes


class SomeChain(BaseChain):
    """Цепочка выполнения с новой нодой"""

    def __init__(self):
        super().__init__()

        #Добавить в список нод
        node_list: List[nodes.BaseNode] = [
            nodes.NewNode,
            ...
        ]

        # Не забыть добавить связь
        edge_list = [
            (nodes.NewNode, nodes.SomeNode),
            ...
        ]

        ...
```
Подробнее смотри в [цепочках](../chains/README.md#-создание-своей-цепочки)

## 📋 Чеклисты

**Добавление новой ноды:**
- [ ] Зарегестрировать имя ноды в [`NodeNames`](../state_management/commands.py) 
  - [ ] Занести мета-данные для ноды в `NodesMeta`
- [ ] (опц.) Создать [валидационную модель](../state_management/validation_models/README.md#-создание-своей-модели)
- [ ] Создать [промпт](../prompts/README.md#-создание-своего-промпта)
- [ ] Создать класс ноды в папке [nodes](../nodes/)
  - [ ] Использовать в `def __init__()` имя созданной ноды
  - [ ] Использовать в `def __init__()` созданную модель
  - [ ] Использовать в `def __init__()` путь до созданного промпта
- [ ] Добавить ноду в [`__init__.py`](__init__.py)

**Удаление: TODO**
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
