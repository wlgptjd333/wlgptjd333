"""프로필 README용 SVG를 만든다. 애플 사이트 느낌(큰 제목, 연회색 둥근 카드, 알약 버튼)에
가벼운 CSS 애니메이션을 더했다.

    python3 scripts/make_assets.py

assets/ 아래에 이미지마다 -light.svg, -dark.svg 두 개씩 만든다. SVG를 직접 고치지 말고 이 파일을 고친다.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
W = 880
FONT = ("-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Pretendard Variable', Pretendard, "
        "'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif")
EMOJI = "'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif"

THEMES = {
    "light": dict(card="#f5f5f7", tile="#ffffff", text="#1d1d1f", muted="#6e6e73", accent="#0066cc",
                  blue="#0071e3", track="#e3e3e8", green="#34c759", blob=0.30,
                  live=("#248a3d", "#e3f5e8"), done=("#0066cc", "#e5f0fb"), wip=("#b25000", "#fdeed9")),
    "dark": dict(card="#1c1c1e", tile="#2c2c2e", text="#f5f5f7", muted="#98989d", accent="#2997ff",
                 blue="#0a84ff", track="#3a3a3c", green="#30d158", blob=0.34,
                 live=("#30d158", "#12331c"), done=("#64a8ff", "#14263d"), wip=("#ff9f0a", "#3a2a10")),
}
STATUS_LABEL = {"live": "Live", "wip": "In progress", "done": "Done"}

STYLE = """<style>
.up{animation:up .9s cubic-bezier(.2,.7,.2,1) both}
.d1{animation-delay:.1s}.d2{animation-delay:.2s}.d3{animation-delay:.3s}.d4{animation-delay:.4s}.d5{animation-delay:.5s}
@keyframes up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.grow{transform-box:fill-box;transform-origin:left center;animation:grow 1.5s cubic-bezier(.2,.7,.2,1) .5s both}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}
@keyframes pulse{from{transform:scale(1);opacity:.7}to{transform:scale(2.6);opacity:0}}
.drift{animation:drift 12s ease-in-out infinite alternate}
.drift2{animation:drift2 15s ease-in-out infinite alternate}
@keyframes drift{to{transform:translate(70px,26px)}}
@keyframes drift2{to{transform:translate(-80px,-20px)}}
.pop{animation:pop .4s ease both}
@keyframes pop{from{opacity:.12}to{opacity:1}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>"""


def text_width(s, size, bold=False):
    w = 0.0
    for ch in s:
        if ord(ch) > 0x2E80:
            w += 1.0
        elif ch in " il.,:;'|·":
            w += 0.28
        elif ch.isupper() or ch.isdigit() or ch in "mw@%":
            w += 0.64
        else:
            w += 0.54
    return w * size * (1.06 if bold else 1.0)


def svg(w, h, label, body, defs=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" '
            f'role="img" aria-label="{escape(label)}">\n<defs>{STYLE}{defs}</defs>\n'
            f'<g font-family="{FONT}">\n{body}\n</g>\n</svg>\n')


def emoji(x, y, size, ch):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" font-family="{EMOJI}">{ch}</text>'


def chips(items, x, y, t, max_x, size=13, h=28, pad=12, gap=7, row_gap=6):
    out, x0 = [], x
    for it in items:
        w = text_width(it, size) + pad * 2
        if x + w > max_x:
            x, y = x0, y + h + row_gap
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2:.0f}" fill="{t["tile"]}"/>'
                   f'<text x="{x + w / 2:.0f}" y="{y + h / 2 + size * 0.36:.0f}" text-anchor="middle" '
                   f'font-size="{size}" font-weight="500" fill="{t["muted"]}">{escape(it)}</text>')
        x += w + gap
    return "\n".join(out)


# ---------- 머리 배너 ----------
def header(t):
    h = 330
    defs = f'''<clipPath id="c"><rect width="{W}" height="{h}" rx="32"/></clipPath>
<filter id="b" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="55"/></filter>
<linearGradient id="gt" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="440" y2="0" spreadMethod="reflect">
<stop offset="0" stop-color="#2997ff"/><stop offset=".5" stop-color="#bf5af2"/><stop offset="1" stop-color="#ff375f"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="880 0" dur="9s" repeatCount="indefinite"/>
</linearGradient>'''
    body = f'''<g clip-path="url(#c)">
<rect width="{W}" height="{h}" fill="{t["card"]}"/>
<g filter="url(#b)" opacity="{t["blob"]}">
<circle class="drift" cx="90" cy="300" r="120" fill="#2997ff"/>
<circle class="drift2" cx="800" cy="40" r="120" fill="#bf5af2"/>
<circle class="drift" cx="700" cy="330" r="90" fill="#ff375f"/>
</g>
</g>
<g class="up">
<rect x="{W / 2 - 22}" y="40" width="44" height="44" rx="12" fill="{t["text"]}"/>
<text x="{W / 2}" y="70" text-anchor="middle" font-size="23" font-weight="800" fill="{t["card"]}">H</text>
</g>
<text class="up d1" x="{W / 2}" y="122" text-anchor="middle" font-size="16" font-weight="600" fill="{t["muted"]}">AI Vision · Apps · Games</text>
<text class="up d2" x="{W / 2}" y="200" text-anchor="middle" font-size="78" font-weight="700" letter-spacing="-2.5" fill="{t["text"]}">Hyesung.</text>
<text class="up d3" x="{W / 2}" y="246" text-anchor="middle" font-size="23" font-weight="600" letter-spacing="-.3" fill="url(#gt)">Building AI vision tools and apps, and writing down what I learn.</text>
<text class="up d4" x="{W / 2}" y="284" text-anchor="middle" font-size="14.5" fill="{t["muted"]}">머신비전 · 딥러닝 · AI 서비스 개발을 공부하며, 직접 쓰고 싶은 앱과 게임을 만듭니다.</text>'''
    return svg(W, h, "Hyesung — Building AI vision tools and apps, and writing down what I learn.", body, defs)


# ---------- 소개 카드 3개 ----------
ABOUT = [
    ("🥊", "Pose & Motion", ["웹캠 영상에서 관절 좌표를 뽑아", "동작을 실시간으로 인식하고", "게임 입력으로 연결합니다."]),
    ("⚙️", "Model to Service", ["Fine-tuning한 모델을 API로", "서빙하고, 응답 시간과 테스트", "결과를 숫자로 기록합니다."]),
    ("📱", "Real-time Apps", ["WebSocket 실시간 데이터로", "Android 오버레이 앱과 웹을", "직접 만들어 배포하고 고칩니다."]),
]


def about(t):
    parts = []
    for i, (em, title, lines) in enumerate(ABOUT):
        ls = "\n".join(f'<text x="24" y="{124 + j * 23}" font-size="15" fill="{t["muted"]}">{escape(l)}</text>'
                       for j, l in enumerate(lines))
        parts.append(f'''<g transform="translate({i * 300} 0)"><g class="up d{i + 1}">
<rect width="280" height="200" rx="24" fill="{t["card"]}"/>
{emoji(42, 58, 30, em)}
<text x="24" y="94" font-size="20" font-weight="700" letter-spacing="-.3" fill="{t["text"]}">{escape(title)}</text>
{ls}
</g></g>''')
    return svg(W, 200, " / ".join(f"{a[1]}: {' '.join(a[2])}" for a in ABOUT), "\n".join(parts))


# ---------- 숫자 카드 4개 ----------
def highlights(t):
    cw, inner = 205, 165
    grad = ('<linearGradient id="gb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2997ff"/>'
            '<stop offset="1" stop-color="#bf5af2"/></linearGradient>')

    def bar(to, mark):
        return (f'<rect x="20" y="146" width="{inner}" height="8" rx="4" fill="{t["track"]}"/>'
                f'<rect class="grow" x="20" y="146" width="{inner * to:.0f}" height="8" rx="4" fill="url(#gb)"/>'
                f'<rect x="{20 + inner * mark:.0f}" y="143" width="2" height="14" rx="1" fill="{t["muted"]}"/>')

    two = (f'<rect class="grow" x="20" y="142" width="{inner}" height="7" rx="3.5" fill="{t["track"]}"/>'
           f'<rect class="grow" x="20" y="154" width="{inner * 1.4 / 22:.0f}" height="7" rx="3.5" fill="url(#gb)"/>')
    dots = "".join(f'<circle class="pop" style="animation-delay:{0.5 + k * 0.07:.2f}s" cx="{24 + k * 9.2:.1f}" cy="150" r="3.3" fill="{t["green"]}"/>'
                   for k in range(18))
    cards = [
        ("어퍼컷 인식", "91.0", "%", "37.3% → 91.0%", bar(0.91, 0.373), "Body Hero · v1.0 → v1.1"),
        ("Test 정확도", "0.98", "", "0.72 → 0.98", bar(0.98, 0.72), "콩잎 분류 · 125 / 128장"),
        ("동기 응답", "22", " ms", "캐시 HIT 1.4 ms", two, "FastAPI · ResNet-18"),
        ("기능 테스트", "18 / 18", "", "실환경 PASS", dots, "동기 · 비동기 API"),
    ]
    parts = []
    for i, (label, num, unit, delta, viz, note) in enumerate(cards):
        parts.append(f'''<g transform="translate({i * 225} 0)"><g class="up d{i + 1}">
<rect width="{cw}" height="210" rx="24" fill="{t["card"]}"/>
<text x="20" y="40" font-size="14" font-weight="600" fill="{t["muted"]}">{escape(label)}</text>
<text x="19" y="94" font-size="42" font-weight="700" letter-spacing="-1.5" fill="{t["text"]}">{escape(num)}<tspan font-size="22" font-weight="600" letter-spacing="0">{escape(unit)}</tspan></text>
<text x="20" y="124" font-size="15" font-weight="600" fill="{t["accent"]}">{escape(delta)}</text>
{viz}
<text x="20" y="186" font-size="13" fill="{t["muted"]}">{escape(note)}</text>
</g></g>''')
    return svg(W, 210, "어퍼컷 인식 37.3% → 91.0% · Test 정확도 0.72 → 0.98 · 동기 응답 22 ms · 기능 테스트 18 / 18",
               "\n".join(parts), grad)


# ---------- 프로젝트 카드 ----------
PROJECTS = [
    ("body-hero", "🥊", "GAME · 졸업작품", "Body Hero", "done",
     "웹캠 하나로 즐기는 2D 복싱 체감형 게임. 펀치 · 어퍼컷 · 가드 · 스쿼트로 몬스터와 싸웁니다.",
     ["Godot 4.6", "MediaPipe Pose", "1D-CNN", "Python", "UDP"]),
    ("beans", "🌱", "VISION AI · API", "콩잎 질병 분류 Vision AI 서비스", "done",
     "ResNet-18을 Fine-tuning해 동기 · 비동기 API로 서빙합니다. Test 정확도 0.72 → 0.98.",
     ["PyTorch", "FastAPI", "Celery", "Redis", "PostgreSQL", "Docker"]),
    ("coinfloat", "🪙", "ANDROID · WEB", "CoinFloat", "live",
     "다른 앱 위에 뜨는 초소형 실시간 시세 오버레이. 웹 버전과 내장 차트도 있습니다.",
     ["Android", "WebSocket", "Lightweight Charts", "Pine Script"]),
    ("inklog", "📝", "OCR · 미니프로젝트", "InkLog", "wip",
     "종이 점검일지를 사진 한 장으로 칸별 데이터로 바꾸고, 범위를 벗어난 값은 바로 알려 줍니다.",
     ["OpenCV", "OCR", "Python", "FastAPI"]),
]


def project(t, em, eyebrow, title, status, summary, tags):
    fg, bg = t[status]
    label = STATUS_LABEL[status]
    sw = text_width(label, 13, True) + 36
    sx = W - 28 - sw
    pulse = f'<circle class="pulse" cx="{sx + 15:.0f}" cy="41" r="4" fill="{fg}"/>' if status == "live" else ""
    body = f'''<g class="up">
<rect width="{W}" height="172" rx="24" fill="{t["card"]}"/>
<rect x="28" y="28" width="60" height="60" rx="16" fill="{t["tile"]}"/>
{emoji(58, 69, 30, em)}
<text x="108" y="44" font-size="12.5" font-weight="700" letter-spacing=".6" fill="{t["accent"]}">{escape(eyebrow)}</text>
<text x="107" y="75" font-size="25" font-weight="700" letter-spacing="-.5" fill="{t["text"]}">{escape(title)}</text>
<text x="108" y="102" font-size="15" fill="{t["muted"]}">{escape(summary)}</text>
{chips(tags, 108, 120, t, W - 28)}
<rect x="{sx:.0f}" y="28" width="{sw:.0f}" height="26" rx="13" fill="{bg}"/>
{pulse}<circle cx="{sx + 15:.0f}" cy="41" r="4" fill="{fg}"/>
<text x="{sx + 25:.0f}" y="45.5" font-size="13" font-weight="700" fill="{fg}">{label}</text>
</g>'''
    return svg(W, 172, f"{title}: {summary}", body)


# ---------- 기술 스택 ----------
STACK = [
    ("🤖", "AI · Vision", ["PyTorch", "Transformers", "YOLO", "MediaPipe", "OpenCV"]),
    ("⚙️", "Serving", ["FastAPI", "Celery", "Redis", "PostgreSQL", "SQLAlchemy", "Docker Compose"]),
    ("🎮", "Game · App", ["Godot 4", "Android", "JavaScript", "WebSocket", "Three.js"]),
    ("🧰", "Tools", ["Git", "GitHub", "WSL2 (Ubuntu)", "uv", "Jekyll"]),
]


def stack(t):
    parts = []
    for i, (em, title, items) in enumerate(STACK):
        x, y = (i % 2) * 450, (i // 2) * 150
        parts.append(f'''<g transform="translate({x} {y})"><g class="up d{i + 1}">
<rect width="430" height="130" rx="24" fill="{t["card"]}"/>
{emoji(36, 44, 20, em)}
<text x="56" y="43" font-size="17" font-weight="700" letter-spacing="-.2" fill="{t["text"]}">{escape(title)}</text>
{chips(items, 22, 60, t, 410)}
</g></g>''')
    return svg(W, 280, " / ".join(f"{s[1]}: {', '.join(s[2])}" for s in STACK), "\n".join(parts))


# ---------- 알약 버튼 ----------
GH = ("M8 0c4.42 0 8 3.58 8 8a8.013 8.013 0 0 1-5.45 7.59c-.4.08-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 "
      "0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82"
      "-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 "
      "0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53"
      ".34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z")


def icon(kind, color):
    if kind == "github":
        return f'<path transform="scale(1.25)" fill="{color}" d="{GH}"/>'
    s = f'fill="none" stroke="{color}" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"'
    if kind == "download":
        return f'<path {s} d="M10 2.5v10.5M5.5 9l4.5 4.5L14.5 9M3.5 17.5h13"/>'
    if kind == "globe":
        return (f'<circle {s} cx="10" cy="10" r="8"/><ellipse {s} cx="10" cy="10" rx="3.4" ry="8"/>'
                f'<path {s} d="M2 10h16"/>')
    raise ValueError(kind)


BUTTONS = [  # 파일 이름, 글자, 아이콘, 종류
    ("github", "GitHub", "github", "ink"),
    ("download", "Download", "download", "blue"),
    ("website", "Website", "globe", "blue"),
    ("home", "byhyesung.com", "globe", "blue"),
    ("repos", "Repositories", "github", "ink"),
]


def button(t, label, ico, kind):
    fill, fg = (t["text"], t["card"]) if kind == "ink" else (t["blue"], "#ffffff")
    w = round(18 + 20 + 9 + text_width(label, 16, True) + 20)
    body = f'''<rect width="{w}" height="40" rx="20" fill="{fill}"/>
<g transform="translate(18 10)">{icon(ico, fg)}</g>
<text x="47" y="26" font-size="16" font-weight="600" fill="{fg}">{escape(label)}</text>'''
    return svg(w, 40, label, body)


def main():
    OUT.mkdir(exist_ok=True)
    for old in OUT.glob("*.svg"):
        old.unlink()
    for name, t in THEMES.items():
        files = {"header": header(t), "about": about(t), "highlights": highlights(t), "stack": stack(t)}
        for slug, *rest in PROJECTS:
            files[f"project-{slug}"] = project(t, *rest)
        for slug, *rest in BUTTONS:
            files[f"btn-{slug}"] = button(t, *rest)
        for key, content in files.items():
            (OUT / f"{key}-{name}.svg").write_text(content, encoding="utf-8")
    print(len(list(OUT.glob("*.svg"))), "files in", OUT)


if __name__ == "__main__":
    main()
