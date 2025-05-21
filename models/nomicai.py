from langchain_nomic import NomicEmbeddings
from .base import BaseAPIEmbedModel
from .config import NomicEmbedAPIConfig


class NomicEmbedModel(BaseAPIEmbedModel):
    def __init__(self, config: NomicEmbedAPIConfig):
        super().__init__(config)
        self.config = config

    def _initialize(self):
        self.model = NomicEmbeddings(model="nomic-embed-text-v1.5", nomic_api_key=self.config.api_key)
