import lancedb
from data_models import Transcript
import time
from constants import VECTOR_DATABASE_PATH
from data_preperations import ingest_markdowns_to_df, get_better_yt_data


def setup_vector_database(path):
    vector_db = lancedb.connect(uri = path)
    # mode="overwrite" makes it idempotent
    vector_db.create_table("transcriptions", schema=Transcript, exist_ok=True, mode="overwrite")

    return vector_db

def add_data_to_vector_db(table):
    l1 = ingest_markdowns_to_df()
    l2 = get_better_yt_data()
    link_lookup = {
        item["video_title"]: item["video_link"] 
        for item in l2
    }
    for record in l1:
        video_title = record["video_title"]
        
        video_link = link_lookup.get(video_title)

        # Only add if a corresponding link was found, else add the youtube channel start page
        if video_link: 
            table.add(
                [{
                    "video_title": video_title,
                    "content": record["content"],
                    "video_link" : video_link
                    }
                ]
            )
        else:
            table.add(
                [{
                    "video_title": video_title,
                    "content": record["content"],
                    "video_link" : "https://www.youtube.com/@AIgineer"
                    }
                ]
            ) 
        print(table.to_pandas().shape)
        print(table.to_pandas())
        #time.sleep(30)


if __name__ == "__main__":
    vector_db = setup_vector_database(VECTOR_DATABASE_PATH)
    add_data_to_vector_db(vector_db["transcriptions"])