from pathlib import Path
import lancedb
from data_models import Transcript
import time
from constants import DATA_PATH, VECTOR_DATABASE_PATH
from data_preperations import ingest_markdowns_to_df, get_better_yt_data

def setup_vector_database(path):
    Path(path).mkdir(exist_ok=True) #idempotent
    vector_db = lancedb.connect(uri=path)
    vector_db.create_table("transcriptions", schema=Transcript, mode="overwrite")

    return vector_db

def merge_dataframes():
    df1 = ingest_markdowns_to_df()
    df2 = get_better_yt_data()
    merged_df = df1.merge(
        df2, 
        how='left', 
        on='video_title' 
    )
    return merged_df

def add_df_to_vector_db(table):
    df = merge_dataframes()
    # table.add(
    #             [{
    #                 "video_title": df["video_title"],
    #                 "content": df["content"],
    #                 "video_link" : df["video_link"] 
    #                 }
    #             ]
    #         )
    table.add(df)
    print(table.to_pandas()["video_title"])


if __name__ == "__main__":
    vector_db = setup_vector_database(VECTOR_DATABASE_PATH)
    add_df_to_vector_db(vector_db["transcriptions"])