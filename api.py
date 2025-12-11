from fastapi import FastAPI
from rag_agent import initialize_agent, initialize_metadata_agent
from data_models import Prompt

app = FastAPI()

GLOBAL_CHAT_HISTORY = []
CHAT_AGENT = initialize_agent()
METADATA_AGENT = initialize_metadata_agent()

@app.get("/")
async def root():
    return {"message": "Youtube Channel API"}

@app.post("/rag/query")
async def agent_with_history(prompt: Prompt):
    
    global GLOBAL_CHAT_HISTORY
    user_prompt_string = prompt.prompt
    
    result= await CHAT_AGENT.run(user_prompt=user_prompt_string, message_history=GLOBAL_CHAT_HISTORY)
    GLOBAL_CHAT_HISTORY = result.all_messages()
    
    return {"user_query": user_prompt_string, "bot_response": result.output}


@app.get("/rag/history")
async def history_endpoint():
    
    #Make the history digestable
    readable_history = []
    for message in GLOBAL_CHAT_HISTORY:
        for part in message.parts:
            # Check if the object has an attribute named "content" and "part_kind"
            part_kind = getattr(part, 'part_kind', 'unknown')
            if hasattr(part, 'content'):
                content = part.content
                readable_history.append({
                "part_kind" : part_kind,
                "content" : content
                })
    return readable_history


@app.post("/rag/description-gen")
async def generate_description(prompt: Prompt):
    user_prompt_string = prompt.prompt
    result= await METADATA_AGENT.run(user_prompt=user_prompt_string)
    data_dict = result.output.model_dump()
    return {"description" : data_dict["description"]}

@app.post("/rag/keyword-gen")
async def generate_keywords(prompt: Prompt):
    user_prompt_string = prompt.prompt
    result= await METADATA_AGENT.run(user_prompt=user_prompt_string)
    data_dict = result.output.model_dump()
    return {"keywords" : ",".join(data_dict["keywords"])}


if __name__ == "__main__":
    print(GLOBAL_CHAT_HISTORY)