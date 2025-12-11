# RAG lab DE24 John Sandsjö
### Search and generate content from Youtube channel

## How to get up and running
To test the prototype, simply [go to this link](https://yt-rag-web-b3enfze3f5dccncw.swedencentral-01.azurewebsites.net/ "Link to protytpe"). It is a Streamlit app deployed as Azure Web App. The frontend code is conatinerized in Docker and deployed to Azure container instance. The app speaks to the a FastAPI api also deployed to Azure as a Function App.

To test the endpoints, got to the Jupyter notebook called demo_endpoint.ipynb. The different endpoints to try:
- /rag/qyery - main endpint searching for a specifc subject and returns a video title, video link and agent answer.
- /rag/history - 
- /rag/description-gen - generate a video description on the closest matching video from the vector search
- /rag/keywords-gen - generate 20-40 keywords related to the closest matching video from the vector search

## Overview
Overview of the projects different pars:
![Project overview](/assets/images/overview.jpg "overview")

## Code highlights

### Vector DB
The vector database in Lance DB has the following columns; video_title, video_link, content and embedding.
The vector is created based on the the entire transcription (content). 

### Youtueb API
The *video links* are retrieved from using the Youtube API, see screenshot below. The upload_playlist_id is a specific Youtbe playlist all channels have with all their uploaded videos. This si retrieved from another endpoint, see explorations. ![Retriving better Youtube channel data](/assets/images/yt_data.jpg "function for Youtube API")

### Agent prompt and code
The agent prompt and code can be found below. Not the tool calling, this makes the actual RAG and searches the closest vector matching the user's query. The function *initialize_agent()* initalizes the agent which then can be used in other modules like this:

    CHAT_AGENT = initialize_agent()
![Agent code](/assets/images/agent_code.jpg "agent code")