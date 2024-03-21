import chainlit as cl
import pandas as pd
from langchain_core.runnables import RunnableConfig
from modules.data_process import (if_exists, return_data, return_model,
                                  find_index_by_name, add_value_to_column,
                                  save_file)
from modules.agents import Agents


@cl.on_chat_start
async def main():
    try:
        subject = body = ""
        model, temperature, opener, escalator = return_model()
        agent = Agents(model=model, temperature=temperature, prompt_opener=opener, prompt_escalator=escalator)
        cl.user_session.set("agent", agent)
        name = await cl.AskUserMessage(content="Please Enter your Name", timeout=60).send()
        name = name['output']
        mess = cl.Message(content="")
        if name and if_exists(str(name)):
            index = find_index_by_name(str(name))
            print(index)
            cl.user_session.set("index", index)
            data = return_data(str(name))
            async for chunk in agent.opener_agent.astream(
                    {'input': f"{data[0]}"},
                    config=RunnableConfig(callbacks=[
                        cl.LangchainCallbackHandler(stream_final_answer=True)])):
                await mess.stream_token(chunk["email_subject"] + "\n" + chunk['email_body'])

                subject += " " + chunk["email_subject"]
                body += " " + chunk['email_body']
            agent.memory.save_context(inputs={"input": f"{data[0]}"},
                                      outputs={"output": f"{subject}" + "\n" + f"{body}"})

            await mess.send()
            await cl.make_async(agent.generate_summary)()
            add_value_to_column(column_name="email_body", value=body, index=index)
            add_value_to_column(column_name="email_subject", value=subject, index=index)
        else:
            await cl.Message(content="No name exists.").send()
    except Exception as e:
        print(e)
        await cl.Message(
            content=f"{e}",
        ).send()


@cl.on_message
async def on_message(message: cl.Message):
    try:
        agent = cl.user_session.get("agent")
        index = cl.user_session.get("index")
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
        agent.memory.save_context(inputs={"input": mess.content},
                                  outputs={"output": f"{response}" + "\n" + f"{lead_status}"})

        await cl.make_async(agent.generate_summary)()
        add_value_to_column(column_name="lead_status", value=lead_status, index=index)
        if lead_status == "Escalated":
            add_value_to_column(column_name="agent_response", value=pd.NA, index=index)
            save_file()
        else:
            add_value_to_column(column_name="agent_response", value=response, index=index)
            save_file()
    except Exception as e:
        await cl.Message(
            content=f"{e}",
        ).send()
