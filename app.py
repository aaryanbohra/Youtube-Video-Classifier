import streamlit as st
import youtube
import model

headers = {
    "github_auth": st.secrets["token"],
    "yt_api_key": st.secrets["YT_API_KEY"]
}

st.title("YouTube Video Topic Classifier")

url = st.text_input("Enter YouTube Video URL:")

if url:
    video_id = youtube.extract_video_id(url)
    metadata = youtube.fetch_metadata(video_id, headers["yt_api_key"])

    if metadata is None:
        st.error("Could not fetch video metadata. Check the URL or API key.")
    else:
        transcript = youtube.fetch_transcript(video_id)
        category = model.classify_video(metadata, transcript, headers["github_auth"])
        st.write(f"**Predicted Category:** {category}")
