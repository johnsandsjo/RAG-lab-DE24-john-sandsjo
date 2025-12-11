from pydantic_ai import Agent
from data_models import RagResponse, MetadataResponse
from constants import VECTOR_DATABASE_PATH
import lancedb

vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)


def retrieve_matching_video(query: str):
    """
    Use vector search to find the closest matching Youtube video title to the query.
    """
    results = vector_db["transcriptions"].search(query=query).to_list()

    return f"""
        video title: {results[0]["video_title"]},
        content: {results[0]["content"]},
        video_link: {results[0]["video_link"]},
    """

def initialize_agent():
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
    tools=[retrieve_matching_video]
    )
    return rag_agent

def initialize_metadata_agent():
    rag_agent = Agent(
    model= "google-gla:gemini-2.5-flash",
    retries=2,
    system_prompt=(
        """
        You are an expert Data Engineering and AI Engineering.
        Always use the retrieved knowledge of the Youtube transcripts and video title from your tool to answer the question. 
        Generate a description and 20-40 keywords based on the transcript and the video title.
        Do add more flavor from your expertise about the subject.
        """
    ),
    output_type=MetadataResponse,
    tools=[retrieve_matching_video]
    )
    return rag_agent

if __name__ == "__main__":
    print(initialize_agent())
    # #setting inital state of history
    # current_history=None
    # print("--- First chat ---")
    # user_prompt_1 = "advanced sql"
    
    # output_1, current_history = agent_with_history(user_prompt_1, current_history=current_history)
    # print(output_1)
    
    # print("\n--- Second chat ---")
    # user_prompt_2 = "What was my previous question?"
    # time.sleep(30)
    # output_2, current_history = agent_with_history(user_prompt_2, current_history)
    # print(output_2)