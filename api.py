from fastapi import FastAPI
from rag import rag_agent
from data_models import Prompt

app = FastAPI()

#Initializes and returns the core chat agent.
chat_agent = rag_agent

@app.post("/rag/query")
async def query_videos(query: Prompt):
    result = await chat_agent.run(query.prompt)

    return result.output


# @app.get("/rag/history")
# async def query_videos(query, result):
#     message_history = result.all_messages() if result else None
#     result = await rag_agent.run(query.prompt, message_history=message_history)
#     return result.output