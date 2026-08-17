import json
from openai import OpenAI

SYSTEM = """너는 한국어 YouTube 트렌드 리서치 편집자다.
제공된 YouTube 영상의 제목/설명/자막을 근거로만 요약한다.
자막이 없으면 제목과 설명만 근거로 삼고, 실제 영상을 확인했다고 가장하지 않는다.
정치·사회 관련 주장은 사실로 단정하지 말고 '영상의 주장'과 '확인 필요한 내용'을 구분한다.
과장된 제목은 그대로 사실로 받아들이지 않는다.
한국어로 간결하지만 정보량 있게 작성한다.
"""

def summarize_video(client: OpenAI, video: dict) -> dict:
    source = f"""제목: {video['title']}
채널: {video['channel_title']}
업로드: {video['published_at']}
조회수: {video['view_count']:,}
분류: {video['category']}
설명:
{video.get('description','')[:7000]}

자막:
{video.get('transcript') or '(자막을 확보하지 못함)'}
"""
    prompt = f"""다음 영상에 대해 JSON으로 작성해라.

{source}

필드:
summary: 3~5문장 핵심 요약
key_points: 핵심 포인트 3개
why_popular: 조회수가 높은 이유에 대한 근거 있는 추정 2~3문장. 반드시 '추정'임을 드러낼 것.
fact_check_notes: 정치/사회적 주장, 수치, 사건 등이 있으면 확인이 필요한 부분. 없으면 빈 배열.
content_basis: '자막+메타데이터' 또는 '메타데이터만'
"""
    response = client.responses.create(
        model=video.get("_model", "gpt-5.5"),
        instructions=SYSTEM,
        input=prompt,
        text={"format": {"type": "json_object"}},
    )
    return json.loads(response.output_text)
