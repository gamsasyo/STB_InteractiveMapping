import json as _j

C = {
    # ── /project1/basics ──
    '/project1/basics/rectangle1':  '사각형 생성 TOP — 주요: Size(크기) · Fill Color(색) · Border(테두리)',
    '/project1/basics/rectangle2':  '사각형 생성 TOP — 주요: Size · Fill Color',
    '/project1/basics/transform1':  '이동·회전·크기 TOP — 주요: Translate · Rotate · Scale. Referencing 단골 목적지',
    '/project1/basics/transform2':  '이동·회전·크기 TOP — Rotate에 null_spin 참조 중',
    '/project1/basics/level1':      '톤 조절 TOP — 주요: Opacity(투명도) · Brightness · Gamma · Contrast',
    '/project1/basics/null1':       '출력 단자 — 연산 없음. 체인 끝은 항상 Null',
    '/project1/basics/null_final':  '출력 단자 — ①의 완성작. 여기를 Display',
    '/project1/basics/circle1':     '원 생성 TOP — 파라미터 구조는 Rectangle과 동일',
    '/project1/basics/moviefilein1':'이미지·영상 파일 입력 TOP — 주요: File(경로) · Play·Speed(영상일 때)',
    '/project1/basics/ramp1':       '그라데이션 생성 TOP — 주요: Type(방향) · 색 키 편집(Ramp 페이지)',
    '/project1/basics/noise1':      '노이즈 생성 TOP — 주요: Type · Period(패턴 크기) · Translate(시간 연결하면 움직임)',
    '/project1/basics/lfo1':        '반복 신호 CHOP — 주요: Type(파형) · Frequency(속도) · Amplitude(크기)',
    '/project1/basics/lfo2':        '반복 신호 CHOP — Frequency 0.2 = 5초에 한 바퀴',
    '/project1/basics/constant1':   '고정값 CHOP — 주요: Name(채널명) · Value. 모든 신호의 시작점 (여기선 30 = 초당 30도)',
    '/project1/basics/speed1':      '누적 CHOP — 입력을 계속 쌓음. 입력 필수. 주요: Limit(범위 제한)',
    '/project1/basics/math1':       '연산·범위 변환 CHOP — 주요: From Range → To Range(리매핑) · Multiply · Combine',
    '/project1/basics/null_wobble': '출력 단자 — 왕복값(-1~1). 여기서 드래그해서 Referencing',
    '/project1/basics/null_spin':   '출력 단자 — 누적 회전값(도). transform2 Rotate로',
    '/project1/basics/null_hue':    '출력 단자 — 0~360 색상값. hsvadj1 Hue로',
    '/project1/basics/hsvadj1':     '색상 조절 TOP — 주요: Hue Offset(색상환 회전, 0~360) · Saturation · Value',

    # ── /project1/webcam ──
    '/project1/webcam/videodevin1': '웹캠 입력 TOP — 주요: Device(카메라 선택) · Active. 장치는 한 곳에서만!',
    '/project1/webcam/flip1':       '뒤집기 TOP — 주요: Flip X(거울 반전). 웹캠은 뒤집어야 자연스러움',
    '/project1/webcam/edge1':       '윤곽선 추출 TOP — 주요: Strength(세기) · Edge Color · Alpha',
    '/project1/webcam/feedback1':   '이전 프레임 기억 TOP — 주요: Target TOP(루프 지점 = add1). 잔상의 심장',
    '/project1/webcam/level_fade':  '잔상 감쇠 — 주요: Opacity(0.92). 1에 가까울수록 잔상이 길게 남음',
    '/project1/webcam/level_play':  '밝기·대비 노브 — 주요: Brightness · Contrast · Gamma. 여기서 장난치기',
    '/project1/webcam/add1':        '합성 TOP — 두 입력을 더함(밝아짐). 현재 프레임 + 잔상',
    '/project1/webcam/transform1':  '화면 흔들기 — Translate에 마우스 참조 중 (*0.3 = 흔들림 세기)',
    '/project1/webcam/null1':       '출력 단자 — 완성 화면. 여기를 Display',
    '/project1/webcam/mousein1':    '마우스 입력 CHOP — 채널 tx·ty (-1~1로 이미 정규화됨)',
    '/project1/webcam/lag1':        '부드럽게 CHOP — 주요: Lag(초). 클수록 늦게 따라옴 = 반응 속도 노브',
    '/project1/webcam/null_shake':  '출력 단자 — 부드러운 마우스값. transform1 Translate로',

    # ── /project1/audio ──
    '/project1/audio/select_cam':      '참조 TOP — 주요: TOP(가져올 경로). 웹캠 장치를 /webcam과 공유',
    '/project1/audio/audiodevin1':     '마이크 입력 CHOP — 주요: Device(입력 장치) · Active',
    '/project1/audio/analyze_level':   '채널 분석 CHOP — 주요: Function(RMS Power = 음량 크기)',
    '/project1/audio/analyze_kick':    '채널 분석 CHOP — Function: RMS Power. 저역만 들어와서 = 킥 세기',
    '/project1/audio/math_level':      '범위 변환 — From 0~0.3 → To 0~1. 마이크 음량을 공용어(0~1)로',
    '/project1/audio/math_kick':       '범위 변환 — From 0~0.2 → To 0~1. 킥 세기를 공용어(0~1)로',
    '/project1/audio/rename_level':    '채널 이름 변경 — chan1 → level. 이름이 곧 의미',
    '/project1/audio/rename_kick':     '채널 이름 변경 — chan1 → kick',
    '/project1/audio/lag_level':       '부드럽게 — Lag 0.2/0.2. 색이 출렁이지 않게',
    '/project1/audio/lag_kick':        '부드럽게 — 올림 0.02/내림 0.25. 비대칭 = 펀치감의 비밀',
    '/project1/audio/null_level':      '출력 단자 — level(0~1). hsvadj1 Hue로 (*360)',
    '/project1/audio/null_kick':       '출력 단자 — kick(0~1). transform1 Scale로 (1 + *0.35)',
    '/project1/audio/audiofilter_low': '주파수 필터 CHOP — 주요: Filter(Low Pass) · Cutoff(140Hz). 킥 대역만 통과',
    '/project1/audio/mousein1':        '마우스 입력 CHOP — 채널 tx·ty (-1~1)',
    '/project1/audio/lag_mouse':       '부드럽게 — Lag 0.15/0.15',
    '/project1/audio/null_mouse':      '출력 단자 — displace1 Weight로 (일렁임 세기)',
    '/project1/audio/noise1':          '노이즈 생성 TOP — Translate Z에 시간 연결 = 일렁임이 살아 움직임',
    '/project1/audio/displace1':       '픽셀 밀기 TOP — 주요: Displace Weight(세기 ← 마우스) · Source(2번 입력 = 노이즈)',
    '/project1/audio/hsvadj1':         '색상 조절 TOP — Hue Offset ← level*360 (음량이 색을 돌림)',
    '/project1/audio/transform1':      '크기 펀치 — Scale ← 1 + kick*0.35 (킥 칠 때 화면이 튐)',
    '/project1/audio/null_out':        '출력 단자 — 완성 화면. 여기를 Display',
}

missing, done = [], 0
for path, txt in C.items():
    o = op(path)
    if o is None:
        missing.append(path)
        continue
    o.comment = txt
    done += 1

project.save()
result = _j.dumps({'set': done, 'missing': missing, 'saved': project.name}, ensure_ascii=False)
