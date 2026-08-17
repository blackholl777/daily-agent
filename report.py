from pathlib import Path

def fmt_views(n):
    if n >= 100_000_000: return f"{n/100_000_000:.1f}억"
    if n >= 10_000: return f"{n/10_000:.1f}만"
    return f"{n:,}"

def build_report(videos, generated_at):
    lines = [
        f"# YouTube 최근 30일 인기 영상 TOP {len(videos)}",
        "",
        f"- 생성 시각: {generated_at}",
        "- 기준: 최근 30일 업로드 + 조회수 내림차순",
        "- 주의: 조회수는 실행 시점의 값이며 계속 변합니다.",
        "",
    ]
    for i, v in enumerate(videos, 1):
        lines += [
            f"## {i}. {v['title']}",
            f"**분야:** {v['category']}  ",
            f"**채널:** {v['channel_title']}  ",
            f"**조회수:** {fmt_views(v['view_count'])}  ",
            f"**업로드:** {v['published_at'][:10]}  ",
            f"**링크:** https://www.youtube.com/watch?v={v['video_id']}",
            "",
            f"**요약:** {v['summary']}",
            "",
            "**핵심 포인트:**",
        ]
        lines += [f"- {x}" for x in v["key_points"]]
        lines += ["", f"**인기 이유(추정):** {v['why_popular']}", ""]
        if v.get("fact_check_notes"):
            lines += ["**확인 필요:**"]
            lines += [f"- {x}" for x in v["fact_check_notes"]]
            lines += [""]
        lines += [f"**근거:** {v['content_basis']}", "", "---", ""]
    return "\n".join(lines)

def save_report(report, generated_at):
    Path("reports").mkdir(exist_ok=True)
    filename = f"reports/youtube-top20-{generated_at[:10]}.md"
    Path(filename).write_text(report, encoding="utf-8")
    Path("reports/latest.md").write_text(report, encoding="utf-8")
    return filename
