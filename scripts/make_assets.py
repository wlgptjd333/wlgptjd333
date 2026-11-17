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
def pose_card(t, x, y):
    """움직이는 자세 인식 카드: 가드 자세에서 오른손 펀치를 반복한다 (2.6초 주기)."""
    kt = 'keyTimes="0;0.42;0.5;0.74;0.84;1" dur="2.6s" repeatCount="indefinite"'

    def anim(attr, a, b):
        return f'<animate attributeName="{attr}" values="{a};{a};{b};{b};{a};{a}" {kt}/>'

    line = f'fill="none" stroke="{t["accent"]}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"'
    dot = f'fill="{t["text"]}"'
    return f'''<g transform="translate({x} {y})"><g class="up d3">
<rect width="272" height="250" rx="22" fill="{t["tile"]}" filter="url(#sh)"/>
<circle class="pulse" cx="24" cy="22" r="4" fill="#ff375f"/><circle cx="24" cy="22" r="4" fill="#ff375f"/>
<text x="36" y="26.5" font-size="12" font-weight="700" letter-spacing=".5" fill="{t["text"]}">LIVE</text>
<text x="256" y="26.5" text-anchor="end" font-size="12" fill="{t["muted"]}">webcam · 30 FPS</text>
<g transform="translate(16 40)">
<rect width="240" height="150" rx="14" fill="{t["card"]}"/>
<path d="M10 24V16a6 6 0 0 1 6-6h8M216 10h8a6 6 0 0 1 6 6v8M230 126v8a6 6 0 0 1-6 6h-8M24 140h-8a6 6 0 0 1-6-6v-8" fill="none" stroke="{t["muted"]}" stroke-width="1.6" stroke-linecap="round" opacity=".55"/>
<rect x="76" y="16" width="90" height="126" rx="6" fill="none" stroke="#ff9f0a" stroke-width="1.6" stroke-dasharray="5 4"/>
<rect x="76" y="2" width="98" height="16" rx="4" fill="#ff9f0a"/>
<text x="82" y="14" font-size="11" font-weight="700" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" fill="#1d1d1f">guard 0.94{anim("opacity", 1, 0)}</text>
<text x="82" y="14" font-size="11" font-weight="700" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" fill="#1d1d1f" opacity="0">punch_r 0.97{anim("opacity", 0, 1)}</text>
<g {line}>
<path d="M100 60H140M120 54V106M108 106H132M108 106L104 138M132 106L136 138M100 60L90 80L108 48"/>
<polyline points="140,60 150,80 132,48">{anim("points", "140,60 150,80 132,48", "140,60 147,72 135,64")}</polyline>
</g>
<circle cx="120" cy="38" r="11" fill="none" stroke="{t["accent"]}" stroke-width="3.2"/>
<g {dot}>
<circle cx="100" cy="60" r="3.6"/><circle cx="140" cy="60" r="3.6"/><circle cx="90" cy="80" r="3.6"/><circle cx="108" cy="48" r="4.4"/>
<circle cx="108" cy="106" r="3.6"/><circle cx="132" cy="106" r="3.6"/>
<circle cx="150" cy="80" r="3.6">{anim("cx", 150, 147)}{anim("cy", 80, 72)}</circle>
</g>
<circle cx="135" cy="64" r="19" fill="none" stroke="#ff375f" stroke-width="1.6" opacity="0">{anim("opacity", 0, 0.5)}</circle>
<circle cx="132" cy="48" r="5.2" fill="#ff375f">{anim("cx", 132, 135)}{anim("cy", 48, 64)}{anim("r", 5.2, 12.5)}</circle>
</g>
<text x="18" y="216" font-size="12.5" font-weight="700" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" fill="{t["text"]}">punch_r</text>
<rect x="82" y="207" width="172" height="8" rx="4" fill="{t["track"]}"/>
<rect x="82" y="207" width="12" height="8" rx="4" fill="url(#gt)">{anim("width", 12, 167)}</rect>
<text x="18" y="236" font-size="11.5" fill="{t["muted"]}">MediaPipe Pose → 1D-CNN → Godot</text>
</g></g>'''


def header(t):
    h = 336
    defs = f'''<clipPath id="c"><rect width="{W}" height="{h}" rx="32"/></clipPath>
<filter id="b" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="55"/></filter>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000" flood-opacity=".12"/></filter>
<linearGradient id="gt" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="440" y2="0" spreadMethod="reflect">
<stop offset="0" stop-color="#2997ff"/><stop offset=".5" stop-color="#bf5af2"/><stop offset="1" stop-color="#ff375f"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="880 0" dur="9s" repeatCount="indefinite"/>
</linearGradient>'''
    body = f'''<g clip-path="url(#c)">
<rect width="{W}" height="{h}" fill="{t["card"]}"/>
<g filter="url(#b)" opacity="{t["blob"]}">
<circle class="drift" cx="60" cy="330" r="120" fill="#2997ff"/>
<circle class="drift2" cx="820" cy="30" r="120" fill="#bf5af2"/>
<circle class="drift" cx="560" cy="350" r="90" fill="#ff375f"/>
</g>
</g>
<g class="up">
<rect x="48" y="40" width="44" height="44" rx="12" fill="{t["text"]}"/>
<text x="70" y="70" text-anchor="middle" font-size="23" font-weight="800" fill="{t["card"]}">H</text>
</g>
<text class="up d1" x="48" y="124" font-size="15.5" font-weight="600" fill="{t["muted"]}">Vision AI · Model Serving · Real-time Apps</text>
<text class="up d2" x="44" y="194" font-size="74" font-weight="700" letter-spacing="-2.5" fill="{t["text"]}">Hyesung.</text>
<g class="up d3" font-size="21.5" font-weight="600" letter-spacing="-.3" fill="url(#gt)">
<text x="48" y="234">Building AI vision tools</text>
<text x="48" y="262">people can actually run.</text>
</g>
<g class="up d4" font-size="14" fill="{t["muted"]}">
<text x="48" y="294">머신비전 · 딥러닝 · AI 서비스 개발을 공부하며,</text>
<text x="48" y="315">직접 쓰고 싶은 앱과 게임을 만듭니다.</text>
</g>
{pose_card(t, 564, 43)}'''
    return svg(W, h, "Hyesung — Building AI vision tools people can actually run.", body, defs)


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


# ---------- 하이라이트: 프로젝트별 개선 전 → 후 ----------
HIGHLIGHTS = [  # 이모지, 프로젝트, 비교 조건, [(지표, 전, 후, 부연)]
    ("🥊", "Body Hero", "v1.0 → v1.1",
     [("어퍼컷 인식률", 37.3, 91.0, "실험자 1명의 플레이 기록 재생"), ("잘못 나간 공격", 24.8, 4.0, "낮을수록 좋음")]),
    ("🌱", "콩잎 질병 분류", "헤드만 학습 → 전체 Fine-tuning",
     [("Test 정확도", 71.9, 97.7, "Test 128장 중 125장"), ("녹병 재현율", 64.4, 95.6, "Validation 45장 중 43장")]),
]


def highlights(t):
    grad = ('<linearGradient id="gb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2997ff"/>'
            '<stop offset="1" stop-color="#bf5af2"/></linearGradient>')
    bw = 176
    parts = []
    for i, (em, name, cond, metrics) in enumerate(HIGHLIGHTS):
        cols = []
        for k, (label, before, after, note) in enumerate(metrics):
            x = 24 + k * 200
            cols.append(f'''<text x="{x}" y="86" font-size="13.5" font-weight="600" fill="{t["muted"]}">{escape(label)}</text>
<text x="{x - 1}" y="134" font-size="40" font-weight="700" letter-spacing="-1.5" fill="{t["text"]}">{after:.1f}<tspan font-size="20" font-weight="600" letter-spacing="0">%</tspan></text>
<text x="{x}" y="160" font-size="14" font-weight="600" fill="{t["accent"]}">{before:.1f}% → {after:.1f}%</text>
<rect x="{x}" y="174" width="{bw}" height="7" rx="3.5" fill="{t["track"]}"/>
<rect class="grow" x="{x}" y="174" width="{bw * after / 100:.0f}" height="7" rx="3.5" fill="url(#gb)"/>
<rect x="{x + bw * before / 100:.0f}" y="171" width="2" height="13" rx="1" fill="{t["muted"]}"/>
<text x="{x}" y="204" font-size="12.5" fill="{t["muted"]}">{escape(note)}</text>''')
        parts.append(f'''<g transform="translate({i * 450} 0)"><g class="up d{i + 1}">
<rect width="430" height="226" rx="24" fill="{t["card"]}"/>
{emoji(36, 46, 20, em)}
<text x="56" y="45" font-size="17" font-weight="700" letter-spacing="-.2" fill="{t["text"]}">{escape(name)}</text>
<text x="406" y="44" text-anchor="end" font-size="12.5" fill="{t["muted"]}">{escape(cond)}</text>
{chr(10).join(cols)}
</g></g>''')
    label = " / ".join(f"{h[1]}: " + ", ".join(f"{m[0]} {m[1]}% → {m[2]}%" for m in h[3]) for h in HIGHLIGHTS)
    return svg(W, 226, label, "\n".join(parts), grad)


# ---------- 프로젝트 카드 ----------
PROJECTS = [
    ("body-hero", "🥊", "GAME · 졸업작품", "Body Hero", "done",
     "웹캠 하나로 즐기는 2D 복싱 체감형 게임. 펀치 · 어퍼컷 · 가드 · 스쿼트로 몬스터와 싸웁니다.",
     ["Godot 4.6", "MediaPipe Pose", "TensorFlow · 1D-CNN", "Python"]),
    ("beans", "🌱", "VISION AI · API", "콩잎 질병 분류 Vision AI 서비스", "done",
     "ResNet-18을 Fine-tuning해 동기 · 비동기 API로 서빙합니다. Test 정확도 71.9% → 97.7%.",
     ["PyTorch", "FastAPI", "Celery", "Redis", "PostgreSQL", "Docker"]),
    ("coinfloat", "🪙", "ANDROID · WEB", "CoinFloat", "live",
     "다른 앱 위에 뜨는 초소형 실시간 시세 오버레이. 직접 쓰면서 계속 고쳐 배포하고 있습니다.",
     ["Kotlin", "JavaScript", "WebSocket", "Lightweight Charts"]),
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
STACK = [  # 위 프로젝트에서 실제로 쓴 것만 적는다.
    ("🤖", "AI · Vision", ["PyTorch", "TensorFlow · Keras", "MediaPipe", "YOLO Pose", "OpenCV"]),
    ("⚙️", "Serving", ["FastAPI", "Celery", "Redis", "PostgreSQL", "Docker Compose"]),
    ("🎮", "App · Game", ["Godot 4", "Kotlin", "JavaScript", "WebSocket"]),
]


def stack(t):
    parts = []
    for i, (em, title, items) in enumerate(STACK):
        parts.append(f'''<g transform="translate({i * 300} 0)"><g class="up d{i + 1}">
<rect width="280" height="170" rx="24" fill="{t["card"]}"/>
{emoji(36, 44, 20, em)}
<text x="56" y="43" font-size="17" font-weight="700" letter-spacing="-.2" fill="{t["text"]}">{escape(title)}</text>
{chips(items, 22, 62, t, 262)}
</g></g>''')
    return svg(W, 170, " / ".join(f"{s[1]}: {', '.join(s[2])}" for s in STACK), "\n".join(parts))


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
    # 맨 위 메뉴 (아이콘 없는 연회색 알약)
    ("nav-about", "About", None, "ghost"),
    ("nav-highlights", "Highlights", None, "ghost"),
    ("nav-projects", "Projects", None, "ghost"),
    ("nav-stack", "Tech Stack", None, "ghost"),
    ("nav-links", "Links", None, "ghost"),
]


def button(t, label, ico, kind):
    if kind == "ghost":
        w = round(text_width(label, 15, True) + 36)
        body = (f'<rect width="{w}" height="36" rx="18" fill="{t["card"]}"/>'
                f'<text x="{w / 2}" y="23.5" text-anchor="middle" font-size="15" font-weight="600" fill="{t["text"]}">{escape(label)}</text>')
        return svg(w, 36, label, body)
    fill, fg = (t["text"], t["card"]) if kind == "ink" else (t["blue"], "#ffffff")
    w = round(18 + 20 + 9 + text_width(label, 16, True) + 20)
    body = f'''<rect width="{w}" height="40" rx="20" fill="{fill}"/>
<g transform="translate(18 10)">{icon(ico, fg)}</g>
<text x="47" y="26" font-size="16" font-weight="600" fill="{fg}">{escape(label)}</text>'''
    return svg(w, 40, label, body)


def main():
    import hashlib
    import re
    import shutil

    files = {}
    for name, t in THEMES.items():
        files[f"header-{name}.svg"] = header(t)
        files[f"about-{name}.svg"] = about(t)
        files[f"highlights-{name}.svg"] = highlights(t)
        files[f"stack-{name}.svg"] = stack(t)
        for slug, *rest in PROJECTS:
            files[f"project-{slug}-{name}.svg"] = project(t, *rest)
        for slug, *rest in BUTTONS:
            files[f"btn-{slug}-{name}.svg"] = button(t, *rest)

    # 브라우저가 예전 이미지를 계속 보여 주지 않도록, 내용이 바뀌면 폴더 이름(해시)도 바뀌게 한다.
    version = hashlib.sha256("".join(files[k] for k in sorted(files)).encode()).hexdigest()[:8]
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / version).mkdir(parents=True)
    for fname, content in files.items():
        (OUT / version / fname).write_text(content, encoding="utf-8")

    readme = OUT.parent / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = re.sub(r"assets/(?:[0-9a-f]{8}/)?([a-z-]+\.svg)", rf"assets/{version}/\1", text)
    readme.write_text(text, encoding="utf-8")
    print(len(files), "files in", OUT / version)


if __name__ == "__main__":
    main()
