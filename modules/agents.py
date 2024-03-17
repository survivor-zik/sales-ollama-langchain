from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor
from langchain.agents.agent_types import AgentType

class _Agents:
    def __init__(self):
        max_tokens = 8192
        self.llm = ChatOllama(
            model="gemma:7b-instruct-q5_K_M",
            temperature=0.0,
            num_ctx=max_tokens,
            num_gpu=29,
            repeat_penalty=1.0)

