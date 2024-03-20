from langchain_openai.chat_models import ChatOpenAI
from langchain.agents import AgentExecutor, initialize_agent, create_react_agent
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from modules.data_process import user_data, parse
from modules.prompt import OPENER
from modules.response import Response
from langchain_core.prompts import PromptTemplate
from langchain.agents.format_scratchpad import format_to_openai_function_messages
from

class Agents:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.2)
        # self.llm=self.llm.bind_tools([user_data])
        self.summary = ""
        history = ChatMessageHistory()
        self.memory = ConversationSummaryMemory(llm=self.llm, return_messages=True)
        tool = user_data
        self.prompt = PromptTemplate.from_template(template=OPENER)
        llm_with_tools = self.llm.bind_functions([tool, Response])
        agent = (
                {
                    "input": lambda x: x["input"],
                    "agent_scratchpad": lambda x: format_to_openai_function_messages(
                        x["intermediate_steps"]
                    ),
                }
                | self.prompt
                | llm_with_tools
                | parse
        )
        self.opener = AgentExecutor(agent=agent, tools=[user_data], prompt=self.prompt, verbose=True,
                                    handle_parsing_errors=True, max_iterations=5)
        esc_agent=agent = (
                {
                    "input": lambda x: x["input"],

                    "agent_scratchpad": lambda x: format_to_openai_function_messages(
                        x["intermediate_steps"]
                    ),
                }
                | self.prompt
                | llm_with_tools
                | parse
        )


    def get_summary(self):
        messages = self.memory.chat_memory.messages
        self.summary = self.memory.predict_new_summary(messages, self.summary)
