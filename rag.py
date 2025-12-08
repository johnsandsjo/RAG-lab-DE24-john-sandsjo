from pydantic_ai import Agent
from data_models import RagResponse
from constants import DATA_PATH, VECTOR_DATABASE_PATH
import lancedb

vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)

def retrieve_top_documents(query: str):
    """
    Use vector search to find the closest matching Youtube video title to the query.
    """
    results = vector_db["transcriptions"].search(query=query).to_list()

    return f"""
        Video title: {results[0]["video_title"]},

        Content: {results[0]["content"]}
    """

rag_agent = Agent(
    model= "google-gla:gemini-2.5-flash",
    retries=2, 
    system_prompt=(
        """
        You are an expert Youtuber in Data Engineering and AI Engineering.
        Always start with the greeting; "Ro Båt my friend!"
        Always use the retrieved knowledge of the Youtube transcripts from your tool to answer the question. 
        Always point to the video title you are referring to.
        But do add more flavor from your expertise about the subject, keep it brief.
        """
    ),
    output_type=RagResponse,
    tools=retrieve_top_documents
)