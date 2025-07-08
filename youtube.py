from urllib.parse import urlparse, parse_qs
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

def extract_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    elif parsed.hostname in ('www.youtube.com', 'youtube.com'):
        query = parse_qs(parsed.query)
        return query.get('v', [None])[0]
    return None


def fetch_metadata(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    response = request.execute()
    if response['items']:
        snippet = response['items'][0]['snippet']
        thumbnails = snippet.get('thumbnails', {})
        thumbnail_url = (
            thumbnails.get('high', {}).get('url') or
            thumbnails.get('medium', {}).get('url') or
            thumbnails.get('default', {}).get('url') or
            ""
        )
        return {
            'title': snippet['title'],
            'description': snippet['description'],
            'tags': snippet.get('tags', []),
            'thumbnail_url': thumbnail_url
        }
    return None


def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([entry['text'] for entry in transcript])
        return text
    except:
        return ""
