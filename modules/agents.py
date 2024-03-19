from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, initialize_agent, create_react_agent
from langchain.agents.agent_types import AgentType
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from modules.data_process import user_data, parse
from modules.prompt import OPENER
from modules.response import Response
from langchain_core.prompts import PromptTemplate
from langchain.agents.format_scratchpad import format_to_openai_function_messages


class Agents:
    def __init__(self):
        max_tokens = 8192
        self.llm = ChatOllama(
            model="gemma:7b-instruct-q5_K_M",
            temperature=0.0,
            num_ctx=max_tokens,
            num_gpu=29,
            repeat_penalty=1.0)
        # self.llm=self.llm.bind_tools([user_data])
        self.summary = ""
        history = ChatMessageHistory()
        self.memory = ConversationSummaryMemory(llm=self.llm, return_messages=True)
        tool = user_data
        self.prompt = PromptTemplate.from_template(template=OPENER)
        opener = create_react_agent(llm=self.llm, tools=[user_data], prompt=self.prompt)
        self.opener = AgentExecutor(agent=opener, tools=[user_data], prompt=self.prompt, verbose=True,
                                    handle_parsing_errors=True, max_iterations=5)
        # llm_with_tools = self.llm.bind([[user_data], Response])
        # agent = (
        #         {
        #             "input": lambda x: x["input"],
        #             "agent_scratchpad": lambda x: format_to_openai_function_messages(
        #                 x["intermediate_steps"]
        #             ),
        #         }
        #         | self.prompt
        #         | llm_with_tools
        #         | parse
        # )
        # self.opener = AgentExecutor(agent=agent, tools=[user_data], prompt=self.prompt, verbose=True,
        #                             handle_parsing_errors=True, max_iterations=5)
        # self.escalator=self.opener = initialize_agent(
        #     agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        #     llm=self.llm,
        #     tools=tool,
        #     agent_kwargs={
        #         'prefix': OPENER_PRE,
        #         'format_instructions': "",
        #         'suffix': OPENER_SUFF
        #     },
        #     verbose=True,
        #     max_iterations=3,
        #     early_stopping_method="force"
        # )

    def get_summary(self):
        messages = self.memory.chat_memory.messages
        self.summary = self.memory.predict_new_summary(messages, self.summary)
        return self.summary
