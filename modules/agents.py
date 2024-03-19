from langchain_community.chat_models import ChatOllama
from langchain.memory import ConversationSummaryMemory, ChatMessageHistory
from modules.prompt import OPENER, ESCALATOR
from langchain_core.prompts import PromptTemplate
from operator import itemgetter
from langchain.output_parsers import ResponseSchema, StructuredOutputParser


class Agents:
    def __init__(self):
        max_tokens = 8192
        self.llm = ChatOllama(
            model="gemma:7b-instruct-q5_K_M",
            temperature=0.3,
            num_ctx=max_tokens,
            num_gpu=29,
            repeat_penalty=1.0)
        response_schemas = [
            ResponseSchema(name="email_subject", description="Subject of the email"),
            ResponseSchema(
                name="email_body",
                description="The Body of the email which is supposed to be sent to the user.",
            ),
        ]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
        format_instructions = output_parser.get_format_instructions()
        self.summary = ""
        history = ChatMessageHistory()
        self.memory = ConversationSummaryMemory(llm=self.llm, return_messages=True)
        self.prompt = PromptTemplate(template=OPENER, input_variables=["input"],
                                     partial_variables={"format_instructions": format_instructions})
        self.opener_agent = ({"input": itemgetter("input"),
                              }
                             | self.prompt
                             | self.llm
                             | output_parser
                             )

        response_schemas_esc = [
            ResponseSchema(name="lead_status", description="""Explains whether the lead has escalated or not.
            (Only 2 options Escalated or Not Escalated)"""),
            ResponseSchema(
                name="agent_response",
                description="The sales representative interacts with the user",
            ),
        ]
        output_parser = StructuredOutputParser.from_response_schemas(response_schemas_esc)
        format_instructions = output_parser.get_format_instructions()
        self.escalator_prompt = PromptTemplate(template=ESCALATOR, input_variables=["input", "chat_history"],
                                               partial_variables={"format_instructions": format_instructions})
        self.escalator_agent = ({
                                    "input": itemgetter("input"),
                                    "chat_history": itemgetter("chat_history"),
                                }
                                | self.escalator_prompt
                                | self.llm
                                | output_parser
                                )

    def generate_summary(self):
        messages = self.memory.chat_memory.messages
        self.summary = self.memory.predict_new_summary(messages, self.summary)
