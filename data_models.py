#from pydantic import Field
from lancedb.pydantic import LanceModel, Vector
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from lancedb.embeddings import get_registry

load_dotenv()
embedding_model = get_registry().get("gemini-text").create(name="gemini-embedding-001")

embedding_dimension = 3072

class Transcript(LanceModel):
    video_title: str
    video_link: str
    content: str = embedding_model.SourceField()
    embedding: Vector(embedding_dimension) = embedding_model.VectorField()
    

class Prompt(BaseModel):
    prompt : str = Field(description= "prompt from user. If empty, consider it missing")

class RagResponse(BaseModel):
    video_title : str = Field(description = "Title of the transcribed Youtube video")
    answer : str = Field(description = "answer based on the video")