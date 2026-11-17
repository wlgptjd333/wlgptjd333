"""프로필 README용 SVG를 만든다. byhyesung.com의 색·모양(assets/css/style.css)을 따른다.

    python3 scripts/make_assets.py

assets/ 아래에 이미지마다 -light.svg, -dark.svg 두 개씩 만든다.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
FONT = ("'Pretendard Variable', Pretendard, -apple-system, BlinkMacSystemFont, 'Segoe UI', "
        "'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif")

THEMES = {
    "light": dict(bg="#f7f6f3", surface="#ffffff", surface2="#f0eee9", text="#1d1d1f", muted="#6b6a66",
                  line="#e4e1da", accent="#3b6cf6",
                  live=("#1f8a4c", "#e3f5ea"), wip=("#a1580d", "#fdf0dd"), done=("#4b5bb8", "#e9ecfb")),
    "dark": dict(bg="#121214", surface="#1b1b1e", surface2="#232327", text="#ececef", muted="#9c9ca4",
                 line="#2e2e33", accent="#7c9cff",
                 live=("#6fd39a", "#183325"), wip=("#f2b56b", "#3a2a15"), done=("#a3afff", "#252a4a")),
}
STATUS_LABEL = {"live": "Live", "wip": "In progress", "done": "Done"}


def text_width(s, size, bold=False):
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += 1.0
        elif ch == " ":
            w += 0.28
        elif ch in "il.,:;'|·":
            w += 0.28
        elif ch.isupper() or ch.isdigit() or ch in "mw@%":
            w += 0.64
        else:
            w += 0.54
    return w * size * (1.06 if bold else 1.0)


def svg(w, h, label, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(label)}">\n<g font-family="{FONT}">\n{body}\n</g>\n</svg>\n')


def chips(items, x, y, t, size=17, h=34, pad=13, gap=8):
    out = []
    for it in items:
        w = text_width(it, size) + pad * 2
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="8" fill="{t["surface2"]}"/>'
                   f'<text x="{x + w / 2:.0f}" y="{y + h / 2 + size * 0.35:.0f}" text-anchor="middle" '
                   f'font-size="{size}" fill="{t["muted"]}">{escape(it)}</text>')
        x += w + gap
    return "\n".join(out)


def header(t):
    pills = []
    x = 1144
    for name in reversed(["AI Vision", "Apps", "Games"]):
        w = text_width(name, 18, True) + 32
        x -= w
        pills.append(f'<rect x="{x:.0f}" y="38" width="{w:.0f}" height="40" rx="20" fill="{t["surface"]}" stroke="{t["line"]}"/>'
                     f'<text x="{x + w / 2:.0f}" y="64" text-anchor="middle" font-size="18" font-weight="600" fill="{t["text"]}">{name}</text>')
        x -= 10
    body = f'''<rect x="0.5" y="0.5" width="1199" height="329" rx="20" fill="{t["bg"]}" stroke="{t["line"]}"/>
<rect x="56" y="36" width="44" height="44" rx="12" fill="{t["text"]}"/>
<text x="78" y="67" text-anchor="middle" font-size="23" font-weight="800" fill="{t["bg"]}">H</text>
<text x="114" y="66" font-size="24" font-weight="700" fill="{t["text"]}">byhyesung</text>
{chr(10).join(pills)}
<text x="56" y="146" font-size="21" font-weight="500" fill="{t["muted"]}">@wlgptjd333</text>
<text x="54" y="208" font-size="60" font-weight="800" letter-spacing="-1" fill="{t["text"]}">Hyesung</text>
<text x="56" y="252" font-size="26" font-weight="600" fill="{t["text"]}">Building AI vision tools and apps, and writing down what I learn.</text>
<text x="56" y="292" font-size="19" fill="{t["muted"]}">Vision AI 과정에서 머신비전 · 딥러닝 · AI 서비스 개발을 공부하며, 직접 쓰고 싶은 앱과 게임을 만듭니다.</text>'''
    return svg(1200, 330, "Hyesung (@wlgptjd333) — Building AI vision tools and apps, and writing down what I learn.", body)


HIGHLIGHTS = [
    ("Body Hero · 어퍼컷 인식", "91.0", "%", "37.3% → 91.0%", "같은 플레이 기록 재생 기준"),
    ("콩잎 분류 · Test 정확도", "0.98", "", "0.72 → 0.98", "125 / 128장 · Test 1회 평가"),
    ("FastAPI 동기 응답", "22", " ms", "캐시 HIT 1.4 ms", "ResNet-18 · 로컬 측정"),
    ("기능 테스트", "18 / 18", "", "실환경 PASS", "동기 · 비동기 API"),
]


def highlights(t):
    parts = []
    for i, (label, num, unit, delta, note) in enumerate(HIGHLIGHTS):
        x = i * 305
        parts.append(f'''<g transform="translate({x} 0)">
<rect x="0.5" y="0.5" width="284" height="199" rx="16" fill="{t["surface"]}" stroke="{t["line"]}"/>
<text x="24" y="46" font-size="17" font-weight="600" fill="{t["muted"]}">{escape(label)}</text>
<text x="24" y="112" font-size="50" font-weight="800" letter-spacing="-1" fill="{t["text"]}">{escape(num)}<tspan font-size="26" font-weight="700">{escape(unit)}</tspan></text>
<text x="24" y="146" font-size="18" font-weight="700" fill="{t["accent"]}">{escape(delta)}</text>
<text x="24" y="174" font-size="16" fill="{t["muted"]}">{escape(note)}</text>
</g>''')
    return svg(1200, 200, "어퍼컷 인식 37.3% → 91.0% · Test 정확도 0.72 → 0.98 · 동기 응답 22 ms · 기능 테스트 18 / 18",
               "\n".join(parts))


PROJECTS = [
    ("body-hero", "🥊", "Body Hero", "done", "웹캠 하나로 즐기는 2D 복싱 체감형 게임 — 펀치 · 어퍼컷 · 가드 · 스쿼트로 몬스터와 싸웁니다.",
     ["Godot", "MediaPipe Pose", "1D-CNN", "졸업작품"]),
    ("beans", "🌱", "콩잎 질병 분류 Vision AI 서비스", "done", "ResNet-18을 Fine-tuning해 동기 · 비동기 API로 서빙합니다. Test 정확도 0.72 → 0.98.",
     ["PyTorch", "FastAPI", "Celery", "Redis", "PostgreSQL", "Docker"]),
    ("coinfloat", "🪙", "CoinFloat", "live", "다른 앱 위에 뜨는 초소형 실시간 시세 오버레이. 웹 버전과 내장 차트도 있습니다.",
     ["Android", "WebSocket", "Lightweight Charts", "Pine Script"]),
    ("inklog", "📝", "InkLog", "wip", "종이 점검일지를 사진 한 장으로 칸별 데이터로 바꾸고, 범위를 벗어난 값은 바로 알려 줍니다.",
     ["OpenCV", "OCR", "Python"]),
]


def project(t, emoji, title, status, summary, tags):
    fg, bg = t[status]
    label = STATUS_LABEL[status]
    sw = text_width(label, 16, True) + 28
    body = f'''<rect x="0.5" y="0.5" width="1199" height="189" rx="16" fill="{t["surface"]}" stroke="{t["line"]}"/>
<rect x="32" y="32" width="64" height="64" rx="16" fill="{t["surface2"]}"/>
<text x="64" y="76" text-anchor="middle" font-size="32">{emoji}</text>
<text x="120" y="62" font-size="27" font-weight="750" fill="{t["text"]}">{escape(title)}</text>
<text x="120" y="96" font-size="19" fill="{t["muted"]}">{escape(summary)}</text>
<rect x="{1168 - sw:.0f}" y="32" width="{sw:.0f}" height="32" rx="16" fill="{bg}"/>
<text x="{1168 - sw / 2:.0f}" y="54" text-anchor="middle" font-size="16" font-weight="700" fill="{fg}">{label}</text>
{chips(tags, 120, 124, t)}'''
    return svg(1200, 190, f"{title}: {summary}", body)


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for name, t in THEMES.items():
        (OUT / f"header-{name}.svg").write_text(header(t), encoding="utf-8")
        (OUT / f"highlights-{name}.svg").write_text(highlights(t), encoding="utf-8")
        for slug, *rest in PROJECTS:
            (OUT / f"project-{slug}-{name}.svg").write_text(project(t, *rest), encoding="utf-8")
    print(len(list(OUT.glob("*.svg"))), "files in", OUT)


if __name__ == "__main__":
    main()
