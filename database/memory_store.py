import os

from langgraph.store.redis import RedisStore

from config import load_environment

load_environment()  # TODO: убрать после лепки

memory_store = None

with RedisStore.from_conn_string(os.getenv("REDIS_URL")) as ms:
  ms.setup()
  memory_store = ms