# 수퍼 테스트베드 — 인터랙티브 매핑 LAB

TouchDesigner 인터랙티브 아트 워크숍 자료입니다.
**모든 자료 한눈에: https://gamsasyo.github.io/STB_InteractiveMapping/Slide/**

## 2주차 (7/16) — MediaPipe 인터랙션

웹캠이 몸 컨트롤러가 된다 — 손/포즈 트래킹 · 정규화 · 매핑.

| 자료 | 링크 |
|---|---|
| 📺 슬라이드 (웹) | [week2.html](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html) |
| 🎛 TD 완성본 | [TD/week2.zip](TD/week2.zip) — 압축 해제 후 .toe 실행 (경량판, [MediaPipe TD Plugin](https://github.com/torinmb/mediapipe-touchdesigner/releases)과 함께) |

**베이스별 빌드 가이드** — 완성 네트워크 · 단계별 파라미터 · 왜 이렇게 만드는지 · 트러블슈팅:

| 베이스 | 내용 | 가이드 |
|---|---|---|
| `01_Hand` | 검지끝 = 허공 마우스 + 잔상 (손으로 그리는 빛) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g01) |
| `02_Theremin` | 손 높이 = 음정 · 좌우 = 볼륨 (허공 테레민) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g02) |
| `03_Pose` | 양 손목 거리 → 팔 벌리면 화면이 커진다 | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g03) |
| `04_TwoHands` | 두 손 사이 거리 → 화면이 숨쉰다 (확장 미션 1) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g04) |
| `05_Pinch` | 핀치 → Logic → Trigger 폭발 (확장 미션 2) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g05) |
| `06_RPS` | 가위바위보 ① 제스처 모델 (블랙박스) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g06) |
| `07_RPS_Chop` | 가위바위보 ② 관절 기하학 · 순수 CHOP (회전 불변) | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g07) |
| `08_RPS_Script` | 가위바위보 ③ 같은 수학을 파이썬 30줄로 | [바로가기](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week2.html#g08) |

## 1주차 (7/9) — TouchDesigner Basics

| 자료 | 링크 |
|---|---|
| 📺 슬라이드 (웹) | [week1.html](https://gamsasyo.github.io/STB_InteractiveMapping/Slide/week1.html) |
| 📄 01_Basics 강의 PDF | 수업 참가자에게 별도 공유 |
| 🎛 TD 완성본 파일 | [TD/week1.zip](TD/week1.zip) — 압축 해제 후 .toe 실행. `01_Basic` · `02_Webcam` · `03_Audio` · `04_WaterMirror` |

## 3주차 (7/23) — 아두이노 시리얼 *(예정)*

물리 세계의 센서가 CHOP이 되는 날. 자료는 수업 후 공개됩니다.

---

## 도구 (전부 무료)

- **TouchDesigner** (Non-Commercial): https://derivative.ca/download
- **MediaPipe TD Plugin**: https://github.com/torinmb/mediapipe-touchdesigner — 설치 불필요, 릴리즈의 `.toe` 실행
- **Arduino IDE** (3주차): https://www.arduino.cc/en/software

TD 파일은 **zip 링크로 받으세요** — 깃헙의 Raw 보기로 저장하면 파일이 깨집니다. 노드를 클릭하면 파라미터 창 위 초록 코멘트가 안내합니다.
공통 노드: **입력 → 정규화 → 매핑** — 소스만 바뀝니다.
