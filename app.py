import streamlit as st
import youtube
import model
import api



st.title("YouTube Video Topic Classifier (DeepSeek)")

url = st.text_input("Enter YouTube Video URL:")

if url:
    video_id = youtube.extract_video_id(url)
    metadata = youtube.fetch_metadata(video_id, api.YT_API_KEY)

    if metadata is None:
        st.error("Could not fetch video metadata. Check the URL or API key.")
    else:
        transcript = youtube.fetch_transcript(video_id)
        category = model.classify_video(metadata, transcript)
        st.write(f"**Predicted Category:** {category}")
