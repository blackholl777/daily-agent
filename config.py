import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    youtube_api_key: str
    openai_api_key: str
    openai_model: str = "gpt-5.5"
    top_n: int = 20
    candidates_per_category: int = 50
    lookback_days: int = 30
    exclude_shorts: bool = True
    max_transcript_chars: int = 18000
    timezone: str = "Asia/Seoul"
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

    @staticmethod
    def from_env():
        s = Settings(
            youtube_api_key=os.getenv("YOUTUBE_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-5.5"),
            top_n=int(os.getenv("TOP_N", "20")),
            candidates_per_category=int(os.getenv("CANDIDATES_PER_CATEGORY", "50")),
            lookback_days=int(os.getenv("LOOKBACK_DAYS", "30")),
            exclude_shorts=os.getenv("EXCLUDE_SHORTS", "true").lower() == "true",
            max_transcript_chars=int(os.getenv("MAX_TRANSCRIPT_CHARS", "18000")),
            timezone=os.getenv("TIMEZONE", "Asia/Seoul"),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN", ""),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID", ""),
        )
        missing = []
        if not s.youtube_api_key:
            missing.append("YOUTUBE_API_KEY")
        if not s.openai_api_key:
            missing.append("OPENAI_API_KEY")
        if missing:
            raise RuntimeError("Missing environment variables: " + ", ".join(missing))
        return s
