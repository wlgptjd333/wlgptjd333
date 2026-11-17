<!-- GitHub Profile README | wlgptjd333/wlgptjd333 -->
<a id="top"></a>

<div align="center">

<img src="assets/header.svg" width="100%" alt="Hyesung · Vision AI · Apps · Games — Vision AI를 직접 써 볼 수 있는 게임 · 앱 · API로 만듭니다."/>

<br/>

[![About](https://img.shields.io/badge/About-16233A?style=for-the-badge)](#-about)
[![Highlights](https://img.shields.io/badge/Highlights-24426B?style=for-the-badge)](#-highlights)
[![Projects](https://img.shields.io/badge/Projects-3A6EA5?style=for-the-badge)](#-projects)
[![Stack](https://img.shields.io/badge/Tech_Stack-5D728F?style=for-the-badge)](#-tech-stack)
[![Links](https://img.shields.io/badge/Links-F2A541?style=for-the-badge)](#-links)

</div>

<br/>

## 👋 About

> **모델을 학습시키는 데서 끝내지 않고, 누군가 실제로 실행해 볼 수 있는 형태까지 만듭니다.**

<table>
<tr>
<td width="33%" valign="top">

**🥊 Pose & Motion**

웹캠 영상에서 관절 좌표를 뽑아 **동작을 실시간으로 인식**하고, 그 결과를 게임 입력으로 연결합니다.

</td>
<td width="33%" valign="top">

**⚙️ Model to Service**

Fine-tuning한 모델을 **FastAPI · Celery · Redis · PostgreSQL**로 서빙하고, 응답 시간과 테스트 결과를 기록합니다.

</td>
<td width="33%" valign="top">

**📱 Real-time Apps**

WebSocket 실시간 데이터를 다루는 **Android 오버레이 앱과 웹 버전**을 직접 만들어 배포하고 계속 고칩니다.

</td>
</tr>
</table>

<br/>

## 📊 Highlights

<img src="assets/highlights.svg" width="100%" alt="어퍼컷 인식 37.3% → 91.0% · 콩잎 질병 분류 Test 정확도 0.72 → 0.98 · 동기 API 응답 22 ms · 기능 테스트 18 / 18"/>

<sub>※ 각 수치는 아래 프로젝트 저장소의 README에 기록된 결과입니다.</sub>

<div align="right"><a href="#top"><sub><b>↑ 맨 위로</b></sub></a></div>

<br/>

## 🚀 Projects

<sub>카드를 누르면 저장소로 이동합니다.</sub>

<a href="https://github.com/wlgptjd333/body-hero"><img src="assets/project-01.svg" width="100%" alt="01 Body Hero: 웹캠 하나로 즐기는 2D 복싱 체감형 게임"/></a>

<table>
<tr><td width="96" nowrap><b>문제</b></td><td>체감형 게임은 전용 컨트롤러나 VR 장비가 필요합니다. <b>일반 웹캠 하나</b>로 펀치 · 어퍼컷 · 가드 · 스쿼트를 인식하고 싶었습니다.</td></tr>
<tr><td width="96" nowrap><b>수행</b></td><td>MediaPipe Pose 33개 관절 → 어깨 중심 정규화 → <b>4프레임 Conv1D + GAP</b> 경량 모델로 7가지 동작 분류 → 4단계 후처리(EMA · 히스테리시스 · 어퍼컷 게이팅 · 쿨다운) → UDP로 Godot 게임에 전달</td></tr>
<tr><td width="96" nowrap><b>결과</b></td><td>v1.1.0에서 같은 플레이 기록 재생 기준 어퍼컷 정답 <b>37.3% → 91.0%</b>, 다른 공격이 먼저 나간 비율 <b>24.8% → 4.0%</b> · GPU 없이 CPU만으로 동작 · Windows용 Release 배포</td></tr>
<tr><td width="96" nowrap><b>기술</b></td><td><code>Python</code> <code>MediaPipe</code> <code>1D-CNN</code> <code>Godot 4.6</code> <code>UDP</code></td></tr>
</table>

<a href="https://github.com/wlgptjd333/body-hero"><img src="https://img.shields.io/badge/Repository-16233A?style=flat-square&logo=github" alt="repository"/></a>
<a href="https://github.com/wlgptjd333/body-hero/releases/latest"><img src="https://img.shields.io/badge/Download-Release-F2A541?style=flat-square" alt="release"/></a>

<div align="right"><a href="#top"><sub><b>↑ 맨 위로</b></sub></a></div>

<br/>

<a href="https://github.com/wlgptjd333/bean-leaf-disease-api"><img src="assets/project-02.svg" width="100%" alt="02 콩잎 질병 분류 Vision AI 서비스: ResNet-18 Fine-tuning을 동기 · 비동기 API로 서빙"/></a>

<table>
<tr><td width="96" nowrap><b>문제</b></td><td>헤드만 학습한 기준선은 Test 정확도가 0.72에 그쳤고, 모델을 실제 요청으로 받을 <b>서비스 구조</b>도 필요했습니다.</td></tr>
<tr><td width="96" nowrap><b>수행</b></td><td><code>ResNet-18</code>을 <b>각진잎반점병 · 녹병 · 정상</b> 3클래스로 Fine-tuning · 제공 코드는 그대로 두고 <b>실행 옵션만</b> 바꿔 3가지 실험 비교 · Validation으로만 모델을 고른 뒤 Test는 1회만 평가</td></tr>
<tr><td width="96" nowrap><b>결과</b></td><td>Test 정확도 <b>0.72 → 0.98</b> (125 / 128장) · 녹병 재현율(Val) <b>0.64 → 0.96</b></td></tr>
<tr><td width="96" nowrap><b>서비스</b></td><td>FastAPI 동기 API(<b>22 ms</b>, 캐시 HIT 1.4 ms) · Celery 비동기 작업 · Redis 캐시/큐 · PostgreSQL 작업 기록 · 기능 테스트 <b>18 / 18</b> PASS</td></tr>
<tr><td width="96" nowrap><b>기술</b></td><td><code>PyTorch</code> <code>Transformers</code> <code>FastAPI</code> <code>Celery</code> <code>Redis</code> <code>PostgreSQL</code> <code>Docker</code></td></tr>
</table>

<a href="https://github.com/wlgptjd333/bean-leaf-disease-api"><img src="https://img.shields.io/badge/Repository-16233A?style=flat-square&logo=github" alt="repository"/></a>

<div align="right"><a href="#top"><sub><b>↑ 맨 위로</b></sub></a></div>

<br/>

<a href="https://github.com/wlgptjd333/coin-float"><img src="assets/project-03.svg" width="100%" alt="03 CoinFloat: 다른 앱 위에 뜨는 초소형 실시간 시세 오버레이"/></a>

<table>
<tr><td width="96" nowrap><b>문제</b></td><td>다른 앱을 쓰는 동안에도 시세를 보고 싶은데, 기존 앱은 화면을 크게 가리거나 앱을 전환해야 했습니다.</td></tr>
<tr><td width="96" nowrap><b>수행</b></td><td>여백 없는 <b>플로팅 오버레이</b> · WebSocket <b>1개 커넥션</b>으로 실시간 체결 수신 · 지수 백오프 자동 재연결 · 숨기면 수신도 멈춰 배터리 절약</td></tr>
<tr><td width="96" nowrap><b>확장</b></td><td>앱 내 차트(이동평균 · 볼린저 · RSI · MACD · 볼륨 프로파일 · 그리기 도구) · <b>Pine Script 지표 59종</b> · <a href="https://coinfloat.byhyesung.com/">웹 버전</a> · 설정 동기화</td></tr>
<tr><td width="96" nowrap><b>기술</b></td><td><code>Android</code> <code>JavaScript</code> <code>WebSocket</code> <code>Lightweight Charts</code></td></tr>
</table>

<a href="https://github.com/wlgptjd333/coin-float"><img src="https://img.shields.io/badge/Repository-16233A?style=flat-square&logo=github" alt="repository"/></a>
<a href="https://coinfloat.byhyesung.com/"><img src="https://img.shields.io/badge/Web-coinfloat.byhyesung.com-3A6EA5?style=flat-square" alt="web"/></a>

<div align="right"><a href="#top"><sub><b>↑ 맨 위로</b></sub></a></div>

<br/>

<a href="https://github.com/wlgptjd333/handnote-digitizer"><img src="assets/project-04.svg" width="100%" alt="04 InkLog (진행 중): 종이 점검일지를 사진 한 장으로 칸별 데이터로"/></a>

<table>
<tr><td width="96" nowrap><b>문제</b></td><td>기존 OCR은 페이지를 글자 덩어리로 돌려줄 뿐, <b>어느 숫자가 온도인지 · 체크됐는지 · 기준을 넘었는지</b>는 모릅니다.</td></tr>
<tr><td width="96" nowrap><b>계획</b></td><td>양식 정렬 → 칸별 인식 → 체크박스 · 서명 판정 → 범위 검증 → CSV · 기존 도구를 baseline으로 정확도와 시간을 비교</td></tr>
<tr><td width="96" nowrap><b>현재</b></td><td>설비 일일 점검표 양식(칸 19개)과 좌표 프로필 완성 · 인식 엔진은 개발 전</td></tr>
<tr><td width="96" nowrap><b>기술</b></td><td><code>Python</code> <code>OpenCV</code> <code>FastAPI</code></td></tr>
</table>

<a href="https://github.com/wlgptjd333/handnote-digitizer"><img src="https://img.shields.io/badge/Repository-16233A?style=flat-square&logo=github" alt="repository"/></a>

<div align="right"><a href="#top"><sub><b>↑ 맨 위로</b></sub></a></div>

<br/>

## 🌱 Now Learning

Vision AI 과정에서 교과별 실습과 과제를 [vision-ai-lab](https://github.com/wlgptjd333/vision-ai-lab)에 쌓고 있습니다. (기초 과정은 [ai-dev-basics](https://github.com/wlgptjd333/ai-dev-basics))

| 교과 | 내용 |
| :--- | :--- |
| **7 · 8** | 조각김치 이물 검출 팀 프로젝트 (라벨링 → YOLO) |
| **9** | OpenCV 규칙 기반 머신비전 · FastAPI AI 서빙 · 평가과제 |
| **10** | YOLO Pose 자세추정 · 동작분석 |
| **12** | VICON 모션캡처 GLB → FastAPI · Three.js 재생, 웹캠 YOLO Pose와 비교 |

<div align="right"><a href="#top"><sub><b>↑ 맨 위로</b></sub></a></div>

<br/>

## 🛠 Tech Stack

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=flat-square&logo=pytorch&logoColor=white) ![Hugging Face](https://img.shields.io/badge/Hugging_Face-FFD21E?style=flat-square&logo=huggingface&logoColor=black) ![YOLO](https://img.shields.io/badge/YOLO-111F68?style=flat-square&logo=yolo&logoColor=white) ![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?style=flat-square&logo=opencv&logoColor=white) ![MediaPipe](https://img.shields.io/badge/MediaPipe-0097A7?style=flat-square&logo=mediapipe&logoColor=white)
<br/>
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) ![Celery](https://img.shields.io/badge/Celery-37814A?style=flat-square&logo=celery&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) ![Godot](https://img.shields.io/badge/Godot-478CBF?style=flat-square&logo=godotengine&logoColor=white) ![Android](https://img.shields.io/badge/Android-34A853?style=flat-square&logo=android&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)

</div>

<br/>

| 분야 | 기술 |
| :--- | :--- |
| 🤖 **AI · Vision** | `PyTorch` `Hugging Face Transformers` `YOLO (Ultralytics)` `MediaPipe` `OpenCV` |
| ⚙️ **Serving** | `FastAPI` `Celery` `Redis` `PostgreSQL` `SQLAlchemy` `Docker Compose` |
| 🎮 **Game · App** | `Godot 4` `Android` `JavaScript` `WebSocket` `Three.js` |
| 🧰 **Tools** | `Git` `GitHub` `WSL2 (Ubuntu)` `uv` `Jekyll` |

<div align="right"><a href="#top"><sub><b>↑ 맨 위로</b></sub></a></div>

<br/>

## 🔗 Links

<div align="center">

[![Home](https://img.shields.io/badge/Home-byhyesung.com-16233A?style=for-the-badge)](https://byhyesung.com/)
[![GitHub](https://img.shields.io/badge/GitHub-wlgptjd333-24426B?style=for-the-badge&logo=github)](https://github.com/wlgptjd333)

<br/>

<sub>Train the model · Measure it honestly · Ship something people can run</sub>

</div>
