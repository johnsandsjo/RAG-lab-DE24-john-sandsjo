import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()
testing_url = "http://127.0.0.1:8000/rag/query"
az_func_url = "http://127.0.0.1:7071/rag/query"
url = f"https://rag-youtube.azurewebsites.net/rag/query?code={os.getenv('FUNCTION_APP_API')}"


def layout():
    st.markdown("# Youtube kanalbåt")
    st.markdown("Search for content mentioned in the Youtube channel")
    # Initialize chat history    
    if "messages" not in st.session_state:
        st.session_state.messages = []


    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask away"):
        with st.chat_message("user"):
            st.markdown(prompt)

        st.session_state.messages.append({"role": "user", "content": prompt})

        response = requests.post(
            url = url,
            json={"prompt": prompt}
        )
        data = response.json()

        with st.chat_message("assistant"):
            st.markdown(f"Youtube kanalbåt: {data["bot_response"]["answer"]}")
            st.markdown(f"Name of video: {data["bot_response"]["video_title"]}")
            st.markdown(f"[Link to video]({data["bot_response"]["video_link"]})")

        st.session_state.messages.append({"role": "assistant", "content": data["bot_response"]["answer"]})

if __name__ == "__main__":
    layout()


# docker buildx build \
#   --platform linux/arm64,linux/amd64 \
#   -t crragyoutube.azurecr.io/streamlit-yt-rag:latest \
#   --push .