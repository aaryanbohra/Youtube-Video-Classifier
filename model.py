import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
import api

#api_key="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"
endpoint = "https://models.github.ai/inference"
model = "deepseek/DeepSeek-V3-0324"


client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(api.token),
)

def classify_video(metadata, transcript):
    prompt = f"""
You are a content classifier. Given a YouTube video's metadata and transcript, categorize it into ONE of the following categories:
Educational, Informational, Entertainment, News, Gaming, Music, Sports, DIY, Vlog, Review, Commentary.
Also give Confidence: <0-100> right after giving category
Keep your explanation concise (no more than 2–3 sentences).
Title: {metadata['title']}
Description: {metadata['description']}
Tags: {', '.join(metadata['tags'])}
Transcript: {transcript[:1000]}

Category:
"""
    response = client.complete(
        messages=[
            SystemMessage("You are a helpful assistant."),
            UserMessage(prompt),
        ],
        temperature=0,
        top_p=1.0,
        max_tokens=512,
        model=model,
    )

    return response.choices[0].message.content.strip()



