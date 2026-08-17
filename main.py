from datetime import datetime
from isodate import parse_duration
from openai import OpenAI

from config import Settings
from youtube_client import YouTubeClient, CATEGORIES, iso_now, iso_now_minus_days
from transcript import get_transcript
from summarizer import summarize_video
from report import build_report, save_report
from notify import send_telegram

def duration_seconds(value):
    try:
        return int(parse_duration(value).total_seconds())
    except Exception:
        return 0

def collect(settings, yt):
    after = iso_now_minus_days(settings.lookback_days)
    before = iso_now()
    candidates = {}

    for category, queries in CATEGORIES.items():
        for query in queries:
            for item in yt.search(query, after, before, settings.candidates_per_category):
                video_id = item["id"]["videoId"]
                candidates.setdefault(video_id, {
                    "video_id": video_id,
                    "title": item["snippet"]["title"],
                    "description": item["snippet"].get("description", ""),
                    "channel_title": item["snippet"]["channelTitle"],
                    "published_at": item["snippet"]["publishedAt"],
                    "category": category,
                })

    for detail in yt.video_details(candidates.keys()):
        video_id = detail["id"]
        if video_id not in candidates:
            continue
        stats = detail.get("statistics", {})
        candidates[video_id]["view_count"] = int(stats.get("viewCount", 0))
        candidates[video_id]["duration_seconds"] = duration_seconds(
            detail.get("contentDetails", {}).get("duration", "PT0S")
        )

    videos = list(candidates.values())
    if settings.exclude_shorts:
        videos = [v for v in videos if v["duration_seconds"] >= 60]

    videos.sort(key=lambda x: x["view_count"], reverse=True)
    return videos[:settings.top_n]

def main():
    settings = Settings.from_env()
    yt = YouTubeClient(settings.youtube_api_key)
    ai = OpenAI(api_key=settings.openai_api_key)

    top = collect(settings, yt)
    enriched = []

    for video in top:
        video["transcript"] = get_transcript(
            video["video_id"], settings.max_transcript_chars
        )
        video["_model"] = settings.openai_model
        video.update(summarize_video(ai, video))
        enriched.append(video)

    generated_at = datetime.now().astimezone().isoformat()
    report = build_report(enriched, generated_at)
    path = save_report(report, generated_at)

    if settings.telegram_bot_token and settings.telegram_chat_id:
        send_telegram(
            settings.telegram_bot_token,
            settings.telegram_chat_id,
            report[:15000],
        )

    print(f"Completed: {path}; videos={len(enriched)}")

if __name__ == "__main__":
    main()
