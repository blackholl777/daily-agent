from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(video_id: str, max_chars: int = 18000) -> str:
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(
            video_id,
            languages=["ko", "en", "ja", "zh-Hans", "zh"]
        )
        text = " ".join(snippet.text for snippet in transcript)
        return text[:max_chars]
    except Exception:
        return ""
