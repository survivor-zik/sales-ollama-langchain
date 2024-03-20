from operator import itemgetter
from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from modules.data_process import user_data, parse
from modules.prompt import OPENER, ESCALATOR, SUMMARY_PROMPT
from modules.response import Response, Response_Esc
from langchain_core.prompts import PromptTemplate
from langchain.agents.format_scratchpad import format_to_openai_function_messages


class Agents:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.2, streaming=True)
        self.summary = ""
        history = ChatMessageHistory()
        self.memory = ConversationSummaryMemory(llm=self.llm, return_messages=True)
        self.memory.prompt = PromptTemplate.from_template(SUMMARY_PROMPT)
        tool = user_data
        prompt = PromptTemplate.from_template(template=OPENER)
        llm_with_tools = self.llm.bind_functions([tool, Response])
        agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_function_messages(
                        x["intermediate_steps"]
                    ),
                }
                | prompt
                | llm_with_tools
                | parse
        )
        self.opener = AgentExecutor(agent=agent, tools=[],
                                    verbose=True)
        llm_with = self.llm.bind_functions([tool, Response_Esc])
        esc_prompt = PromptTemplate.from_template(ESCALATOR)
        esc_agent = (
                {
                    "input": lambda x: x["input"],
                    "chat_history": itemgetter("chat_history"),
                    "agent_scratchpad": lambda x: format_to_openai_function_messages(
                        x["intermediate_steps"]
                    ),
                }
                | esc_prompt
                | llm_with
                | parse
        )
        self.escalator = AgentExecutor(agent=esc_agent, tools=[], prompt=esc_prompt, verbose=True)

    def get_summary(self):
        messages = self.memory.chat_memory.messages
        self.summary = self.memory.predict_new_summary(messages, self.summary)
