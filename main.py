import chainlit as cl
from langchain_core.runnables import RunnableConfig
from modules.data_process import if_exists, return_data
from modules.agents import Agents


@cl.on_chat_start
async def main():
    try:
        subject = body = ""
        agent = Agents()
        cl.user_session.set("agent", agent)
        name = await cl.AskUserMessage(content="Please Enter your Name", timeout=60).send()
        name = name['output']
        mess = cl.Message(content="")
        if name and if_exists(str(name)):
            data = return_data(str(name))
            async for chunk in agent.opener_agent.astream(
                    {'input': f"{data[0]}"},
                    config=RunnableConfig(callbacks=[
                        cl.LangchainCallbackHandler(stream_final_answer=True)])):
                await mess.stream_token(chunk["email_subject"] + "\n" + chunk['email_body'])

                subject += " " + chunk["email_subject"]
                body += " " + chunk['email_body']
            print("Working")
            agent.memory.save_context(inputs={"input": f"{data[0]}"},
                                      outputs={"output": f"{subject}" + "\n" + f"{body}"})

            await mess.send()
            await cl.make_async(agent.generate_summary)()
        else:
            await cl.Message(content="No name exists.").send()
    except Exception as e:
        await cl.Message(
            content=f"{e}",
        ).send()


@cl.on_message
async def on_message(message: cl.Message):
    try:
        agent = cl.user_session.get("agent")
        mess = cl.Message(content="")
        response = lead_status = " "
        print(agent.summary)
        async for chunk in agent.escalator_agent.astream(
                {'input': message.content,
                 'chat_history': agent.summary},
                config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler(stream_final_answer=True)])):
            await mess.stream_token(chunk["agent_response"])
            response += " " + chunk["agent_response"]
            lead_status += " " + chunk["lead_status"]

        await mess.send()
        print(lead_status)
        agent.memory.save_context(inputs={"input": mess.content},
                                  outputs={"output": f"{response}" + "\n" + f"{lead_status}"})
        await cl.make_async(agent.generate_summary)()
    except Exception as e:
        await cl.Message(
            content=f"{e}",
        ).send()
