from datetime import datetime, timedelta, timezone
from typing import Iterable
import requests

BASE = "https://www.googleapis.com/youtube/v3"

CATEGORIES = {
    "한국 시니어 사연": ["한국 시니어 사연", "노인 사연", "시니어 사연"],
    "해외감동사연": ["해외 감동사연", "해외 감동 실화", "외국인 감동사연"],
    "국뽕": ["국뽕", "한국 자랑", "한국에 놀란 외국인"],
    "우파": ["우파", "보수", "보수 유튜브"],
    "대륙 삼국": ["대륙 삼국", "대륙 삼국지", "중국 삼국지"],
    "시니어 정보": ["시니어 정보", "노인 건강 정보", "50대 60대 70대 정보"],
    "요리": ["한국 요리", "집밥 레시피", "요리 레시피"],
    "우파 정치": ["우파 정치", "보수 정치", "한국 정치 보수"],
    "종합": ["시니어 사연 감동 정보", "한국 감동사연 시니어"],
}

class YouTubeClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()

    def _get(self, endpoint, params):
        params = {**params, "key": self.api_key}
        r = self.session.get(f"{BASE}/{endpoint}", params=params, timeout=30)
        r.raise_for_status()
        return r.json()

    def search(self, query, published_after, published_before, max_results=50):
        return self._get("search", {
            "part": "snippet",
            "q": query,
            "type": "video",
            "order": "viewCount",
            "publishedAfter": published_after,
            "publishedBefore": published_before,
            "maxResults": min(max_results, 50),
            "regionCode": "KR",
            "relevanceLanguage": "ko",
            "safeSearch": "none",
        }).get("items", [])

    def video_details(self, video_ids: Iterable[str]):
        ids = list(dict.fromkeys(video_ids))
        out = []
        for i in range(0, len(ids), 50):
            out.extend(self._get("videos", {
                "part": "snippet,contentDetails,statistics",
                "id": ",".join(ids[i:i+50]),
                "maxResults": 50,
            }).get("items", []))
        return out

def iso_now_minus_days(days):
    now = datetime.now(timezone.utc)
    return (now - timedelta(days=days)).isoformat().replace("+00:00", "Z")

def iso_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
