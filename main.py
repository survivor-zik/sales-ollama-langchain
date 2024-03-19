import chainlit as cl
from chainlit.input_widget import TextInput
from modules.data_process import if_exists, return_data
from modules.agents import Agents


@cl.on_chat_start
async def main():
    try:
        agent = Agents()
        name = await cl.AskUserMessage(content="Please Enter your Name", timeout=60).send()
        name = name['output']
        if name and if_exists(str(name)):
            data = return_data(str(name))
            print(f"Data is {return_data(str(name))[0]}")

            res = agent.opener.invoke({'input': f"{data[0]}"}, return_only_outputs=True)
            print(res)
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
