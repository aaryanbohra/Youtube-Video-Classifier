from mistralai import Mistral, UserMessage, SystemMessage

endpoint = "https://models.github.ai/inference"
model_name = "mistral-ai/Mistral-Large-2411"

def classify_video(metadata, transcript, github_token):
    client = Mistral(
        api_key=github_token,
        server_url=endpoint
    )

    prompt = f"""
You are a content classifier. Given a YouTube video's metadata and transcript, respond with ONE of the following categories and a confidence score from 0–100.

Categories:
Educational, Informational, Entertainment, News, Gaming, Music, Sports, DIY, Vlog, Review, Commentary.

Respond ONLY in this format:

<category> | Confidence: <confidence>
<br>
</br>
Explanation: <2-3 concise sentences>

Do not include any other formatting like <think> or HTML.

Title: {metadata['title']}
Description: {metadata['description']}
Tags: {', '.join(metadata['tags'])}
Transcript: {transcript[:300]}
"""

    response = client.chat.complete(
        model=model_name,
        messages=[
            SystemMessage(content="You are a helpful assistant."),
            UserMessage(content=prompt),
        ],
        temperature=0,
        max_tokens=512,
        top_p=1.0
    )

    return response.choices[0].message.content.strip()
