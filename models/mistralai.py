from huggingface_hub.hf_api import HfFolder
from typing import List
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from .base import BaseAPIModel, BaseAPIEmbedModel
from .config.models import MistralLargeAPIConfig, MistralEmbedAPIConfig
from time import sleep
import os

class MistralLargeModel(BaseAPIModel):    
    # В reason вылетает ошибка, т.к. __init__ принимает config в self.chain. С другим именем работает
    def __init__(self, config: MistralLargeAPIConfig):
        super().__init__(config)
    
    def _initialize(self):
        print(self.config.api_key)
        self.model = ChatMistralAI(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens,
            mistral_api_key=self.config.api_key,
        )

    
    def invoke(self, prompt: str) -> str:
        # Потому что мистраль выдаёт 429 ошибку при частых запросах
        sleep(1)

        response = self.model.invoke(prompt)
        return response.content

    def stream(self, prompt: str):
        for chunk in self.model.stream(prompt):
            yield chunk.content


class MistralEmbedModel(BaseAPIEmbedModel):    
    def __init__(self, config: MistralEmbedAPIConfig):
        HfFolder.save_token(os.environ['HF_TOKEN'])
        super().__init__(config)
        self.config = config
    
    def _initialize(self):
        self.model = MistralAIEmbeddings(
            api_key=self.config.api_key, 
            wait_time=1
        )