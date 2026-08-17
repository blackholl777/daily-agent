# Daily YouTube Trend Agent

매일 오전 6시(Asia/Seoul)에 최근 30일 이내 YouTube 영상을 검색하고, 전체 후보를 조회수 기준으로 정렬해 TOP 20 보고서를 생성합니다.

## 분야

한국 시니어 사연 / 해외감동사연 / 국뽕 / 우파 / 대륙 삼국 / 시니어 정보 / 요리 / 우파 정치 / 종합

## 설치

1. 이 프로젝트를 GitHub repository에 업로드
2. YouTube Data API v3 키 생성
3. OpenAI API 키 생성
4. GitHub repository의 Settings → Secrets and variables → Actions에서 다음 secrets 등록:
   - `YOUTUBE_API_KEY`
   - `OPENAI_API_KEY`
5. 선택적으로 Telegram:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
6. Actions → Daily YouTube Senior Trend Report → Run workflow로 테스트

## 자동 실행

`.github/workflows/daily.yml`이 `Asia/Seoul` 기준 매일 06:00에 실행합니다.

## 로컬 실행

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env
python main.py
```

## 결과

`reports/latest.md`와 날짜별 Markdown 파일에 저장됩니다.

## 중요한 한계

- YouTube API 검색 결과는 검색 시스템이 제공하는 후보 집합이므로 인터넷상의 모든 영상을 완벽하게 열거하는 절대 순위는 아닙니다.
- 조회수는 실행 시점 값입니다.
- 자막을 가져오지 못한 영상은 제목/설명만으로 요약합니다.
- 정치/사회 콘텐츠의 주장은 사실로 단정하지 않고 확인 필요 항목으로 분리합니다.
