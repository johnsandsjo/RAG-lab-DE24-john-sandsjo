from fastapi import FastAPI
from rag import rag_agent
from data_models import Prompt 

app = FastAPI()

@app.post("/rag/query")
async def query_videos(query: Prompt):
    result = await rag_agent.run(query.prompt)

    return result.output