from uuid import uuid4

from pydantic import BaseModel, Field

# from agents.chains import OnlySearchChain as chain
# from agents.chains import FullExecutionChain as chain
from agents.chains import OnlyMemoryChain as chain

# from agents.chains import OnlyMemoryChain as chain
from agents.state_management import GlobalState as state
from config import load_environment, validate_environment

load_environment()
validate_environment()


class MetadataConfig(BaseModel):
    user_uuid: str = Field(default_factory=lambda: str(uuid4()))
    memory_uuid: str = Field(default_factory=lambda: str(uuid4()))


generated_user = str(uuid4())
generated_memory = str(uuid4())

graph = (
    chain()
    .build(state, name="Risk agent with memory")
    .with_config({"metadata": {"user_uuid": generated_user, "memory_uuid": generated_memory}})
)
