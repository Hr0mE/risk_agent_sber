# Модели
Тут хранятся все обёртки для используемых моделей. От LLM до эмбеддеров. Были бы классические ML-модели, тоже тут лежали бы.

## 📁 Файловая структура
models/\
├── [`config/`](./config/) -- Хранение конфигов для моделей. \
├── [`base.py`](base.py) -- Абстракция для добавления моделей. \
├── [`nomicai.py`](nomicai.py) -- Подключение модели nomic для эмбеддингов. \
└── [`mistralai.py`](mistralai.py) -- Подключение модели от Mistral в качестве основной LLM. 

## 🧩 Ключевые компоненты
- [`base.py`](base.py) -- Доступ через класс `BaseAPIModel` или `BaseAPIEmbedModel`. Для добавления локальной модельки, нужно писать собственную абстракцию.

## 🎨 Добавление новой модели
```python
#models/new_model.py

from typing import List
from langchain_newmodelai import ChatNewModelAI, NewModelAIEmbeddings
from .base import BaseAPIModel, BaseAPIEmbedModel
from .config.models import NewModelAPIConfig, NewModelEmbedAPIConfig
from time import sleep
import os


class NewModel(BaseAPIModel):
    def __init__(self, config: NewModelAPIConfig):
        super().__init__(config)

    def _initialize(self):
        self.model = ChatNewModelAI(
            model=self.config.model_name,
            ...
            mistral_api_key=self.config.api_key,
        )

    def invoke(self, prompt: str) -> str:
        response = self.model.invoke(prompt)
        return response.content

    def stream(self, prompt: str):
        for chunk in self.model.stream(prompt):
            yield chunk.content


class NewModelEmbedModel(BaseAPIEmbedModel):
    def __init__(self, config: NewModelEmbedAPIConfig):
        super().__init__(config)
        self.config = config

    def _initialize(self):
        self.model = NewModelAIEmbeddings(api_key=self.config.api_key)
```

## 🛠️ Использование
```python
#agents/nodes/new_node.py

... #some imports here
from models import NewModel as model
from models.config import NewModelAPIConfig as model_config


class NewNode(BaseNode):
    def __init__(self):
        ...
        self.model = model(config=model_config()) # Ничего не трогаем, вся магия в импортах

    def execute(self, state: GlobalState) -> Command:
        ...
        return Command(...)

```

## 📋 Чеклисты

**Добавление:**
- [ ] Убедиться в добавленнии [переменной окружения](../config/README.md#-чеклисты)
- [ ] Создать [конфиг для модели](./config/README.md#-добавление-нового-конфига)

**Удаление:**
- [ ] ctrl+f по проекту с именем класса с последующим удалением. Скорее всего, все воспоминания будут в нодах и один-два в конфигах
