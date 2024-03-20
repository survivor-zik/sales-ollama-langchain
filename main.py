import chainlit as cl
from chainlit.input_widget import TextInput
from langchain_core.runnables import RunnableConfig

from modules.data_process import if_exists, return_data
from modules.agents import Agents


@cl.on_chat_start
async def main():
    try:
        agent = Agents()
        subject = body = ""
        cl.user_session.set("agent", agent)
        name = await cl.AskUserMessage(content="Please Enter your Name", timeout=60).send()
        name = name['output']
        mess = cl.Message(content="")

        if name and if_exists(str(name)):
            data = return_data(str(name))
            async for chunk in agent.opener.astream(
                    {'input': f"{data[0]}"},
                    config=RunnableConfig(callbacks=[
                        cl.LangchainCallbackHandler(stream_final_answer=True,
                                                    answer_prefix_tokens=["FINAL", "ANSWER"])])):
                if "subject" in chunk:
                    subject += " " + chunk["subject"]
                    body += " " + chunk['body']
                    await mess.stream_token(chunk["subject"] + "\n" + chunk['body'])
                    agent.memory.save_context(inputs={"input": mess.content},
                                              outputs={"output": f"{subject}" + "\n" + f"{body}"})
            await cl.make_async(agent.get_summary)()
        else:
            await cl.Message(content="No name exists.").send()
    except Exception as e:
        print(e)
        await cl.Message(
            content=f"{e}",
        ).send()


#
#

@cl.on_message
async def on_message(message: cl.Message):
    try:
        agent = cl.user_session.get("agent")
        index = cl.user_session.get("index")
        mess = cl.Message(content="")
        response = lead_status = " "
        output=" "
        print(agent.summary)
        async for chunk in agent.escalator.astream(
                {'input': message.content,
                 'chat_history': agent.summary},
                config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)])):
            print("66", chunk, "66")
            if 'agent' in chunk:
                await mess.stream_token(chunk["agent"])
                response += " " + chunk["agent"]
                lead_status += " " + chunk["status"]
            else:
                await mess.stream_token(chunk['output'])
                output+=" "+chunk['output']
        await mess.send()
        agent.memory.save_context(inputs={"input": mess.content},
                                  outputs={"output": f"{response}" + "\n" + f"{lead_status}"})

        await cl.make_async(agent.get_summary)()
        add_value_to_column(column_name="lead_status", value=lead_status, index=index)
        if lead_status == "Escalated":
            add_value_to_column(column_name="agent_response", value=pd.NA, index=index)
            save_file()
        elif lead_status=="" and response=="":
            add_value_to_column(column_name="agent_response", value=response, index=index)
            save_file()
    except Exception as e:
        await cl.Message(
            content=f"{e}",
        ).send()
