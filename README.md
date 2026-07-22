# 수퍼 테스트베드 — 인터랙티브 매핑 LAB

TouchDesigner 인터랙티브 아트 워크숍 자료입니다.
**모든 자료 한눈에: https://gamsasyo.github.io/STB_InteractiveMapping/Slide/**
**📦 전체 자료 한 번에: [Download ZIP](https://github.com/gamsasyo/STB_InteractiveMapping/archive/refs/heads/main.zip)**

## 3주차 (7/23) — 아두이노 시리얼

물리 세계의 센서가 CHOP이 되는 날 — 시리얼 통신 · CSV · `Serial DAT → Convert → DAT to CHOP → Rename → Math → Lag → Null`. 아두이노는 "숫자 뱉는 상자", 배우는 건 그 숫자가 TD로 들어오는 통로.

| 자료 | 링크 |
|---|---|
| 📺 슬라이드 (웹) | [week3.html](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week3.html) |
| 🎛 TD 완성본 | 수업 현장 공유 (라이브 빌드) |

**빌드 가이드** — 완성 네트워크 · 단계별 파라미터 · 아두이노 스케치(복붙) · 트러블슈팅:

| 가이드 | 내용 | 링크 |
|---|---|---|
| `공통 빌드` | Serial DAT → … → Null — 센서가 뭐든 똑같은 체인 | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week3.html#g01) |
| `가변저항` | 첫 센서, 값 1개 — `analogRead` (키트 1강) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week3.html#g02) |
| `초음파` | HC-SR04 거리 = 손 거리 재현 — `pulseIn` (키트 3강) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week3.html#g03) |

> 아두이노 회로·IDE 코드 기본기는 **에듀이노 스타터키트 입문편 강의자료 v4.1**(키트 구매 시 제공)로 진행합니다 — 1강 가변저항, 3강 초음파.

## 2주차 (7/16) — MediaPipe 인터랙션

웹캠이 몸 컨트롤러가 된다 — 손/포즈 트래킹 · 정규화 · 매핑.

| 자료 | 링크 |
|---|---|
| 📺 슬라이드 (웹) | [week2.html](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html) |
| 🎛 TD 완성본 | [TD/week2.toe](TD/week2.toe) — 경량판, [MediaPipe TD Plugin](https://github.com/torinmb/mediapipe-touchdesigner/releases)과 함께 실행 |

**베이스별 빌드 가이드** — 완성 네트워크 · 단계별 파라미터 · 왜 이렇게 만드는지 · 트러블슈팅:

| 베이스 | 내용 | 가이드 |
|---|---|---|
| `01_Hand` | 검지끝 = 허공 마우스 + 잔상 (손으로 그리는 빛) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g01) |
| `02_Theremin` | 손 높이 = 음정 · 좌우 = 볼륨 (허공 테레민) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g02) |
| `03_Pose` | 포즈 트래킹 — 손목 사이 거리를 선·숫자로 표시, 팔 벌리면 원이 커진다 | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g03) |
| `04_TwoHands` | 핸드 트래킹 — 두 손 거리를 선·숫자로 표시 + 바나나 블러 🍌 (확장 미션 1) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g04) |
| `05_Pinch` | 핀치 → Logic → Trigger 폭발 (확장 미션 2) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g05) |
| `06_RPS` | 가위바위보 ① 제스처 모델 (블랙박스) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g06) |
| `07_RPS_Chop` | 가위바위보 ② 관절 기하학 · 순수 CHOP (회전 불변) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g07) |
| `08_RPS_Script` | 가위바위보 ③ 같은 수학을 파이썬 30줄로 | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g08) |

## 1주차 (7/9) — TouchDesigner Basics

| 자료 | 링크 |
|---|---|
| 📺 슬라이드 (웹) | [week1.html](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week1.html) |
| 📄 01_Basics 강의 PDF | [Basic/01_Basics.pdf](Basic/01_Basics.pdf) |
| 🎛 TD 완성본 파일 | [TD/week1.toe](TD/week1.toe) — `01_Basic` · `02_Webcam` · `03_Audio` · `04_WaterMirror` |

## 📚 TD 기초 자료실 — [`Basic/`](Basic)

더 파고들 분들을 위한 기초 강의 PDF 시리즈 + 연습용 TD 파일:

| 자료 | 내용 |
|---|---|
| [01_Basics.pdf](Basic/01_Basics.pdf) | TD 기초 — 오퍼레이터 · 와이어 · Referencing (1주차 교재) |
| [02_Feedback.pdf](Basic/02_Feedback.pdf) | 피드백 — 잔상 · 루프 구조 |
| [03_Sop.pdf](Basic/03_Sop.pdf) | SOP — 3D 지오메트리 기초 |
| [04_Particle.pdf](Basic/04_Particle.pdf) | 파티클 시스템 |
| [TD_Basic.toe](Basic/TD_Basic.toe) | 기초 연습용 TD 파일 |

---

## 도구 (전부 무료)

- **TouchDesigner** (Non-Commercial): https://derivative.ca/download
- **MediaPipe TD Plugin**: https://github.com/torinmb/mediapipe-touchdesigner — 설치 불필요, 릴리즈의 `.toe` 실행
- **Arduino IDE** (3주차): https://www.arduino.cc/en/software

노드를 클릭하면 파라미터 창 위 초록 코멘트가 안내합니다.
공통 노드: **입력 → 정규화 → 매핑** — 소스만 바뀝니다.
