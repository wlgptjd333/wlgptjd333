"""프로필 README용 SVG를 만든다. 애플 사이트처럼 큰 글씨, 연회색 둥근 카드, 알약 버튼을 쓰고
가벼운 애니메이션을 더했다.

    python3 scripts/make_assets.py

assets/<내용 해시>/ 아래에 이미지마다 -light.svg, -dark.svg 두 개씩 만들고 README의 이미지 경로도 함께 바꾼다.
SVG를 직접 고치지 말고 이 파일의 문구와 숫자를 고친다. 숫자는 각 프로젝트 저장소 README에 적힌 값만 쓴다.
"""
import hashlib
import math
import re
import shutil
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets"
W = 880
FONT = ("-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Pretendard Variable', Pretendard, "
        "'Segoe UI', 'Apple SD Gothic Neo', 'Noto Sans KR', 'Malgun Gothic', sans-serif")
EMOJI = "'Apple Color Emoji', 'Segoe UI Emoji', 'Noto Color Emoji', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "light": dict(card="#f5f5f7", tile="#ffffff", text="#1d1d1f", muted="#6e6e73", accent="#0066cc",
                  blue="#0071e3", track="#e3e3e8", line="#e3e3e8", blob=0.30, shadow=0.10,
                  pink="#e0144c", green="#1d8a3a", orange="#c45500", indigo="#4f46d8", teal="#0b7a8a",
                  live="#1d8a3a"),
    "dark": dict(card="#1c1c1e", tile="#2c2c2e", text="#f5f5f7", muted="#98989d", accent="#2997ff",
                 blue="#0a84ff", track="#3a3a3c", line="#3a3a3c", blob=0.34, shadow=0.45,
                 pink="#ff375f", green="#30d158", orange="#ff9f0a", indigo="#7d7aff", teal="#40c8e0",
                 live="#30d158"),
}

STYLE = """<style>
.up{animation:up .9s cubic-bezier(.2,.7,.2,1) both}
.d1{animation-delay:.08s}.d2{animation-delay:.16s}.d3{animation-delay:.24s}.d4{animation-delay:.32s}
@keyframes up{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}
@keyframes pulse{from{transform:scale(1);opacity:.7}to{transform:scale(2.6);opacity:0}}
.drift{animation:drift 12s ease-in-out infinite alternate}
.drift2{animation:drift2 15s ease-in-out infinite alternate}
@keyframes drift{to{transform:translate(70px,26px)}}
@keyframes drift2{to{transform:translate(-80px,-20px)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
</style>"""


def text_width(s, size, bold=False):
    """글자 폭 어림값. 한글은 글자 크기만큼, 영문은 대략 절반으로 친다."""
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


def chips(items, x, y, t, max_x, size=13, h=28, pad=12, gap=7, row_gap=7, color=None):
    """알약 모양 태그. items는 글자 또는 (글자, 점 색)."""
    out, x0 = [], x
    for it in items:
        label, dot = (it, None) if isinstance(it, str) else it
        lead = 14 if dot else 0
        w = text_width(label, size) + pad * 2 + lead
        if x + w > max_x and x > x0:
            x, y = x0, y + h + row_gap
        out.append(f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="{h}" rx="{h / 2:.0f}" fill="{t["tile"]}"/>')
        if dot:
            out.append(f'<circle cx="{x + pad + 3.5:.1f}" cy="{y + h / 2}" r="4" fill="{dot}"/>')
        out.append(f'<text x="{x + (w + lead) / 2:.1f}" y="{y + h / 2 + size * 0.36:.1f}" text-anchor="middle" '
                   f'font-size="{size}" font-weight="500" fill="{color or t["muted"]}">{escape(label)}</text>')
        x += w + gap
    return "\n".join(out)


def big(value, unit, size, color, x, y):
    """큰 숫자. 단위(%, ms, FPS)는 작게 붙인다."""
    tail = ""
    if unit:
        us = round(size * (0.56 if unit == "%" else 0.44))
        dx = 2 if unit == "%" else round(size * 0.14)
        tail = f'<tspan dx="{dx}" font-size="{us}" font-weight="600" letter-spacing="0">{escape(unit)}</tspan>'
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="700" letter-spacing="{-size * 0.03:.1f}" '
            f'fill="{color}">{escape(value)}{tail}</text>')


# ---------- 머리 배너 ----------
HEAD = dict(
    name="지혜성", en="Hyesung Ji",
    line="사람의 동작을 인식하는 비전 AI를 만듭니다.",
    chips=["Pose Estimation", "Action Recognition", "Model Serving"],
)


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
<text x="82" y="14" font-size="11" font-weight="700" font-family="{MONO}" fill="#1d1d1f">guard 0.94{anim("opacity", 1, 0)}</text>
<text x="82" y="14" font-size="11" font-weight="700" font-family="{MONO}" fill="#1d1d1f" opacity="0">punch_r 0.97{anim("opacity", 0, 1)}</text>
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
<text x="18" y="216" font-size="12.5" font-weight="700" font-family="{MONO}" fill="{t["text"]}">punch_r</text>
<rect x="82" y="207" width="172" height="8" rx="4" fill="{t["track"]}"/>
<rect x="82" y="207" width="12" height="8" rx="4" fill="url(#gt)">{anim("width", 12, 167)}</rect>
<text x="18" y="236" font-size="11.5" fill="{t["muted"]}">MediaPipe Pose → 1D-CNN → Godot</text>
</g></g>'''


def header(t):
    h = 300
    defs = f'''<clipPath id="c"><rect width="{W}" height="{h}" rx="32"/></clipPath>
<filter id="b" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="55"/></filter>
<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="14" flood-color="#000" flood-opacity="{t["shadow"]}"/></filter>
<linearGradient id="gt" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="440" y2="0" spreadMethod="reflect">
<stop offset="0" stop-color="#2997ff"/><stop offset=".5" stop-color="#bf5af2"/><stop offset="1" stop-color="#ff375f"/>
<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="880 0" dur="9s" repeatCount="indefinite"/>
</linearGradient>'''
    cs, cx = [], 48
    for i, label in enumerate(HEAD["chips"]):
        w = text_width(label, 14, True) + 30
        fill, fg, weight = ("url(#gt)", "#ffffff", 700) if i == 0 else (t["tile"], t["text"], 600)
        cs.append(f'<rect x="{cx:.0f}" y="196" width="{w:.0f}" height="34" rx="17" fill="{fill}"/>'
                  f'<text x="{cx + w / 2:.0f}" y="218" text-anchor="middle" font-size="14" font-weight="{weight}" '
                  f'fill="{fg}">{escape(label)}</text>')
        cx += w + 8
    body = f'''<g clip-path="url(#c)">
<rect width="{W}" height="{h}" fill="{t["card"]}"/>
<g filter="url(#b)" opacity="{t["blob"]}">
<circle class="drift" cx="60" cy="300" r="120" fill="#2997ff"/>
<circle class="drift2" cx="820" cy="30" r="120" fill="#bf5af2"/>
<circle class="drift" cx="560" cy="330" r="90" fill="#ff375f"/>
</g>
</g>
<text class="up d1" x="46" y="122"><tspan font-size="66" font-weight="800" letter-spacing="-1.5" fill="{t["text"]}">{HEAD["name"]}</tspan><tspan dx="14" font-size="26" font-weight="600" letter-spacing="-.3" fill="{t["muted"]}">{HEAD["en"]}</tspan></text>
<text class="up d2" x="48" y="170" font-size="21" font-weight="600" letter-spacing="-.3" fill="{t["text"]}">{escape(HEAD["line"])}</text>
<g class="up d3">
{chr(10).join(cs)}
</g>
{pose_card(t, 564, 25)}'''
    label = f'{HEAD["name"]} {HEAD["en"]} — {HEAD["line"]} ' + " · ".join(HEAD["chips"])
    return svg(W, h, label, body, defs)


# ---------- 대표 프로젝트 카드 ----------
PROJECTS = [
    dict(slug="body-hero", no="01", emoji="🥊", color="pink", eyebrow="POSE ESTIMATION · GAME",
         title="Body Hero", badges=["팀장", "졸업작품"],
         lines=["웹캠 하나로 펀치 · 어퍼컷 · 가드 · 스쿼트를 인식해", "몬스터와 싸우는 2D 복싱 게임입니다."],
         tags=["MediaPipe Pose", "1D-CNN", "TensorFlow", "Godot 4.6"],
         stats=[("99.0", "%", "동작 7가지 분류 정확도"), ("30", "FPS", "GPU 없이 실시간 인식")]),
    dict(slug="beans", no="02", emoji="🌱", color="green", eyebrow="VISION AI · MODEL SERVING",
         title="콩잎 질병 분류 API", badges=[],
         lines=["콩잎 사진을 정상 · 각진잎반점병 · 녹병으로 나누는", "ResNet-18을 FastAPI 동기 · 비동기 API로 서빙합니다."],
         tags=["PyTorch", "FastAPI", "Celery", "Redis", "PostgreSQL"],
         stats=[("97.7", "%", "Test 정확도 · 기준선 71.9%"), ("22", "ms", "동기 API 응답 시간")]),
    dict(slug="coinfloat", no="03", emoji="🪙", color="orange", eyebrow="ANDROID · WEB",
         title="CoinFloat", badges=[],
         lines=["다른 앱 위에 떠 있는 작은 실시간 시세 창입니다.", "직접 쓰면서 계속 고쳐 배포하고 있습니다."],
         tags=["Kotlin", "JavaScript", "WebSocket", "Lightweight Charts"],
         stats=None),
]


def live_chart(t, c, x, y, w, h):
    """CoinFloat 오른쪽 칸: 움직이는 시세 선 그림 (실제 가격이 아니라 그림이라 숫자는 넣지 않는다)."""
    vals = [.28, .34, .31, .40, .36, .45, .42, .38, .49, .46, .55, .51, .60, .56, .64, .61, .70, .66, .75, .80]
    x0, x1 = x + 22, x + w - 22
    top, bot = y + 52, y + h - 40
    pts = [(x0 + (x1 - x0) * i / (len(vals) - 1), bot - (bot - top) * v) for i, v in enumerate(vals)]
    d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
    length = sum(math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1))
    area = d + f" L{x1:.1f} {bot:.1f} L{x0:.1f} {bot:.1f} Z"
    lx, ly = pts[-1]
    return f'''<defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{c}" stop-opacity=".26"/><stop offset="1" stop-color="{c}" stop-opacity="0"/></linearGradient></defs>
<circle class="pulse" cx="{x + 28}" cy="{y + 26}" r="4" fill="{t["live"]}"/><circle cx="{x + 28}" cy="{y + 26}" r="4" fill="{t["live"]}"/>
<text x="{x + 40}" y="{y + 30.5}" font-size="12" font-weight="700" letter-spacing=".5" fill="{t["text"]}">LIVE</text>
<text x="{x + w - 22}" y="{y + 30.5}" text-anchor="end" font-size="12.5" fill="{t["muted"]}">Android · Web</text>
<path d="{area}" fill="url(#fade)"><animate attributeName="opacity" values="0;0;1" keyTimes="0;.55;1" dur="2.4s"/></path>
<path d="{d}" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="{length:.0f}" stroke-dashoffset="0"><animate attributeName="stroke-dashoffset" values="{length:.0f};0" keyTimes="0;1" calcMode="spline" keySplines=".2 .7 .2 1" dur="1.8s"/></path>
<circle class="pulse" cx="{lx:.1f}" cy="{ly:.1f}" r="4.5" fill="{c}"/><circle cx="{lx:.1f}" cy="{ly:.1f}" r="4.5" fill="{c}"/>
<text x="{x + 22}" y="{y + h - 16}" font-size="12.5" fill="{t["muted"]}">WebSocket으로 받는 실시간 체결가</text>'''


def project(t, p):
    c, h = t[p["color"]], 220
    px, pw = 600, 252
    out = [f'<rect width="{W}" height="{h}" rx="28" fill="{t["card"]}"/>',
           '<g class="up d1">',
           f'<rect x="28" y="28" width="64" height="64" rx="18" fill="{t["tile"]}"/>',
           emoji(60, 71, 32, p["emoji"]),
           f'<text x="112" y="45" font-size="12.5" font-weight="700" letter-spacing=".9" fill="{c}">'
           f'{p["no"]}  ·  {escape(p["eyebrow"])}</text>',
           f'<text x="111" y="82" font-size="30" font-weight="700" letter-spacing="-.6" fill="{t["text"]}">'
           f'{escape(p["title"])}</text>']
    bx = 112 + text_width(p["title"], 30, True) + 10
    for b in p["badges"]:
        bw = text_width(b, 13, True) + 22
        out.append(f'<rect x="{bx:.0f}" y="61" width="{bw:.0f}" height="26" rx="13" fill="{c}" fill-opacity=".14"/>'
                   f'<text x="{bx + bw / 2:.0f}" y="78.5" text-anchor="middle" font-size="13" font-weight="700" '
                   f'fill="{c}">{escape(b)}</text>')
        bx += bw + 6
    for i, line in enumerate(p["lines"]):
        out.append(f'<text x="112" y="{120 + i * 23}" font-size="15.5" fill="{t["muted"]}">{escape(line)}</text>')
    out.append(chips(p["tags"], 112, 164, t, px - 20))
    out.append('</g>\n<g class="up d2">')
    out.append(f'<rect x="{px}" y="20" width="{pw}" height="{h - 40}" rx="22" fill="{t["tile"]}"/>')
    if p["stats"]:
        (v1, u1, l1), (v2, u2, l2) = p["stats"]
        out += [big(v1, u1, 46, c, px + 24, 80),
                f'<text x="{px + 25}" y="104" font-size="13.5" font-weight="500" fill="{t["muted"]}">{escape(l1)}</text>',
                f'<rect x="{px + 24}" y="122" width="{pw - 48}" height="1" fill="{t["line"]}"/>',
                big(v2, u2, 30, t["text"], px + 24, 162),
                f'<text x="{px + 25}" y="185" font-size="13.5" font-weight="500" fill="{t["muted"]}">{escape(l2)}</text>']
        stat_alt = f' {l1} {v1}{u1}, {l2} {v2} {u2}'
    else:
        out.append(live_chart(t, c, px, 20, pw, h - 40))
        stat_alt = ""
    out.append('</g>')
    badges = f' ({" · ".join(p["badges"])})' if p["badges"] else ""
    alt = f'{p["no"]} {p["title"]}{badges}: {" ".join(p["lines"])}{stat_alt}'
    return svg(W, h, alt, "\n".join(out))


# ---------- 그 밖의 프로젝트 (반쪽 카드 두 장을 나란히) ----------
OTHERS = [
    dict(slug="kimchi", emoji="🥬", color="teal", title="조각김치 이물 검출", status="팀 프로젝트 · 완료", live=False,
         lines=["직접 만든 라벨링 도구로 사진 900장을", "교차검수하고 YOLO11 검출 성능을 높였습니다."],
         stat=("0.470 → 0.749", "Validation mAP50–95")),
    dict(slug="store", emoji="🏪", color="indigo", title="무인 상점 이상행동 인식", status="팀 프로젝트 · 진행 중",
         live=True,
         lines=["CCTV를 가정해 사람의 2D 자세 시퀀스로", "기물 파손 · 폭력 · 쓰러짐 같은 동작을 구분합니다."],
         stat=("17가지", "YOLO Pose로 구분할 동작")),
]
OW = 430


def other(t, o):
    c, h = t[o["color"]], 206
    dot = t["live"] if o["live"] else t["muted"]
    out = [f'<rect width="{OW}" height="{h}" rx="26" fill="{t["card"]}"/>',
           '<g class="up d1">',
           f'<rect x="24" y="24" width="54" height="54" rx="16" fill="{t["tile"]}"/>',
           emoji(51, 60, 27, o["emoji"]),
           f'<text x="94" y="47" font-size="20" font-weight="700" letter-spacing="-.4" fill="{t["text"]}">'
           f'{escape(o["title"])}</text>']
    if o["live"]:
        out.append(f'<circle class="pulse" cx="98" cy="66" r="3.5" fill="{dot}"/>')
    out.append(f'<circle cx="98" cy="66" r="3.5" fill="{dot}"/>'
               f'<text x="108" y="70.5" font-size="13" font-weight="500" fill="{t["muted"]}">{escape(o["status"])}</text>')
    for i, line in enumerate(o["lines"]):
        out.append(f'<text x="24" y="{114 + i * 23}" font-size="15" fill="{t["muted"]}">{escape(line)}</text>')
    v, label = o["stat"]
    out.append(f'<text x="24" y="182" font-size="22" font-weight="700" letter-spacing="-.4" fill="{c}">{escape(v)}'
               f'<tspan dx="10" font-size="13" font-weight="500" letter-spacing="0" fill="{t["muted"]}">'
               f'{escape(label)}</tspan></text>')
    out.append('</g>')
    alt = f'{o["title"]} ({o["status"]}): {" ".join(o["lines"])} {label} {v}'
    return svg(OW, h, alt, "\n".join(out))


# ---------- 기술 스택 (프로젝트에서 실제로 쓴 것만) ----------
STACK = [
    ("AI · Vision", [("Python", "#3776ab"), ("PyTorch", "#ee4c2c"), ("TensorFlow", "#ff8f00"),
                     ("MediaPipe", "#0097a7"), ("YOLO Pose", "#7b61ff"), ("OpenCV", "#5c3ee8")]),
    ("Serving", [("FastAPI", "#009688"), ("Celery", "#37814a"), ("Redis", "#dc382d"),
                 ("PostgreSQL", "#4169e1"), ("Docker", "#2496ed")]),
    ("App · Game", [("Godot 4", "#478cbf"), ("Kotlin", "#7f52ff"), ("JavaScript", "#e2b800"),
                    ("WebSocket", "#8e8e93")]),
]


def stack(t):
    h = 198
    out = [f'<rect width="{W}" height="{h}" rx="28" fill="{t["card"]}"/>']
    for i, (label, items) in enumerate(STACK):
        y = 24 + i * 58
        out.append(f'<g class="up d{i + 1}">')
        out.append(f'<text x="32" y="{y + 22}" font-size="15.5" font-weight="700" fill="{t["text"]}">{escape(label)}</text>')
        out.append(chips(items, 160, y + 1, t, W - 28, size=13.5, h=32, gap=8, color=t["text"]))
        out.append('</g>')
        if i < len(STACK) - 1:
            out.append(f'<rect x="32" y="{y + 45}" width="{W - 64}" height="1" fill="{t["line"]}"/>')
    alt = " / ".join(f"{s[0]}: {', '.join(n for n, _ in s[1])}" for s in STACK)
    return svg(W, h, alt, "\n".join(out))


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


BUTTONS = [  # 파일 이름, 글자, 아이콘, 종류 (ink 검정 · blue 파랑 · ghost 연회색 메뉴)
    ("github", "GitHub", "github", "ink"),
    ("download", "Download", "download", "blue"),
    ("website", "Website", "globe", "blue"),
    ("home", "byhyesung.com", "globe", "blue"),
    ("nav-projects", "Projects", None, "ghost"),
    ("nav-stack", "Tech Stack", None, "ghost"),
]


def button(t, label, ico, kind):
    if kind == "ghost":
        w = round(text_width(label, 16, True) + 40)
        body = (f'<rect width="{w}" height="40" rx="20" fill="{t["card"]}"/>'
                f'<text x="{w / 2}" y="26" text-anchor="middle" font-size="16" font-weight="600" '
                f'fill="{t["text"]}">{escape(label)}</text>')
        return svg(w, 40, label, body)
    fill, fg = (t["text"], t["card"]) if kind == "ink" else (t["blue"], "#ffffff")
    w = round(18 + 20 + 9 + text_width(label, 16, True) + 20)
    body = f'''<rect width="{w}" height="40" rx="20" fill="{fill}"/>
<g transform="translate(18 10)">{icon(ico, fg)}</g>
<text x="47" y="26" font-size="16" font-weight="600" fill="{fg}">{escape(label)}</text>'''
    return svg(w, 40, label, body)


def main():
    files = {}
    for name, t in THEMES.items():
        files[f"header-{name}.svg"] = header(t)
        files[f"stack-{name}.svg"] = stack(t)
        for p in PROJECTS:
            files[f"project-{p['slug']}-{name}.svg"] = project(t, p)
        for o in OTHERS:
            files[f"other-{o['slug']}-{name}.svg"] = other(t, o)
        for slug, *rest in BUTTONS:
            files[f"btn-{slug}-{name}.svg"] = button(t, *rest)

    # 브라우저가 예전 이미지를 계속 보여 주지 않도록, 내용이 바뀌면 폴더 이름(해시)도 바뀌게 한다.
    version = hashlib.sha256("".join(files[k] for k in sorted(files)).encode()).hexdigest()[:8]
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / version).mkdir(parents=True)
    for fname, content in files.items():
        (OUT / version / fname).write_text(content, encoding="utf-8")

    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = re.sub(r"assets/(?:[0-9a-f]{8}/)?([a-z-]+\.svg)", rf"assets/{version}/\1", text)
    readme.write_text(text, encoding="utf-8")
    missing = sorted(set(re.findall(rf"assets/{version}/([a-z-]+\.svg)", text)) - set(files))
    if missing:
        raise SystemExit(f"README에 있는데 만들지 않은 이미지: {missing}")
    print(len(files), "files in", OUT / version)


if __name__ == "__main__":
    main()
