import chainlit as cl
from chainlit.input_widget import TextInput
from langchain_core.runnables import RunnableConfig

from modules.data_process import if_exists, return_data
from modules.agents import Agents


@cl.on_chat_start
async def main():
    try:
        agent = Agents()
        name = await cl.AskUserMessage(content="Please Enter your Name", timeout=60).send()
        name = name['output']
        mess = cl.Message(content="")
        if name and if_exists(str(name)):
            data = return_data(str(name))
            async for chunk in agent.opener_agent.astream({'input': f"{data[0]}"},
                                                          config=RunnableConfig(callbacks=[
                                                              cl.LangchainCallbackHandler(stream_final_answer=True)])):
                await mess.stream_token(chunk["email_subject"] + "\n" + chunk['email_body'])
        else:
            await cl.Message(content="No name exists.").send()
    except Exception as e:
        await cl.Message(
            content=f"{e}",
        ).send()

#
#

# @cl.on_chat_start
# async def start():
#     settings = await cl.ChatSettings(
#         [
#             TextInput(id="Email", label="Please Enter your Email.", initial="johndoe@gmail.com"),
#         ]
#     ).send()
#     email = settings["Email"]
#     print(email)
