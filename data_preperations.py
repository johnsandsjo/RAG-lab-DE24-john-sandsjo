from constants import DATA_PATH
import requests
import os


def ingest_markdowns_to_df():
    data_records = []
    for file in DATA_PATH.glob(pattern='*.md'):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            video_title = file.stem.casefold()

            data_records.append({
                "video_title" :  video_title.strip(),
                "content" : content
                })
    
    return data_records

def get_better_yt_data(): 
    api_key = os.environ.get('YOUTUBE_API_KEY')

    base_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    upload_playlist_id = 'UUWP1PQqdZyWlBq1V1r71aRg'

    all_videos = []
    next_page_token = None

    while True:
        params = {
            'part': 'snippet',
            'playlistId': upload_playlist_id,
            'key': api_key,
            'maxResults': 50,
            'pageToken': next_page_token
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        for item in data.get('items'):
            snippet = item['snippet']
            video_id = snippet['resourceId']['videoId']
            all_videos.append({
                    'video_title': snippet['title'].strip().casefold(),
                    'video_link': f"https://www.youtube.com/watch?v={video_id}"
                })

        #Check for the next page token or exit the loop if there are no more pages
        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return all_videos


if __name__ == "__main__":
    print(len(ingest_markdowns_to_df()))
    print(len(get_better_yt_data()))