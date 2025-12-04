import streamlit as st
import requests
from pathlib import Path

def layout():
    st.markdown("# Youtube channel search")
    st.markdown("Search for content mentioned in the Youtube channel")
    text_input = st.text_input(label="What do you want to know?")

    if st.button("Send") and text_input.strip() != "":
        response = requests.post(
            url = "http://127.0.0.1:8000/rag/query",
            json={"prompt": text_input}
            )
        data = response.json()
        st.markdown("## Question:")
        st.markdown(text_input)
        
        st.markdown("## Answer:")
        st.markdown(data["answer"])
        
        st.markdown(f"Video title: {data["video_title"]}")
    


if __name__ == "__main__":
    layout()