import td
report = {}

# ── /project1/audio — 확장 미션 답안 데모 ──
# MISSION 02: 마우스 = Displace 세기 / 오디오 = 색 / 저역 킥 펀치
# 공통 척추: 입력 → 정규화(Math+Lag) → 매핑(Referencing)
proj = op('/project1')
old = proj.op('audio')
if old: old.destroy()
p = proj.create(td.baseCOMP, 'audio')
ref = proj.op('webcam')
if ref:
    p.nodeX, p.nodeY = ref.nodeX, ref.nodeY - 200
p.comment = '확장 미션 답안: 오디오(소리)로 화면 흔들기 — MISSION 02'

# ── 입력 1: 오디오 ──
adev = p.create(td.audiodeviceinCHOP, 'audiodevin1')

# 브랜치 A: 전체 음량 → 색 (Hue)
anaL = p.create(td.analyzeCHOP, 'analyze_level')
mthL = p.create(td.mathCHOP,    'math_level')
lagL = p.create(td.lagCHOP,     'lag_level')
nulL = p.create(td.nullCHOP,    'null_level')
anaL.par.function = 'rmspower'
mthL.par.fromrange1, mthL.par.fromrange2 = 0, 0.3   # 마이크 RMS 대략 범위
mthL.par.torange1,  mthL.par.torange2  = 0, 1       # → 공용어 0~1
lagL.par.lag1, lagL.par.lag2 = 0.2, 0.2
adev.outputConnectors[0].connect(anaL.inputConnectors[0])
anaL.outputConnectors[0].connect(mthL.inputConnectors[0])
mthL.outputConnectors[0].connect(lagL.inputConnectors[0])
lagL.outputConnectors[0].connect(nulL.inputConnectors[0])
anaL.comment = '브랜치 A: 전체 음량(RMS) → 0~1 → 색'

# 브랜치 B: 저역만 → 킥 펀치 (Scale)
flt  = p.create(td.audiofilterCHOP, 'audiofilter_low')
anaK = p.create(td.analyzeCHOP, 'analyze_kick')
mthK = p.create(td.mathCHOP,    'math_kick')
lagK = p.create(td.lagCHOP,     'lag_kick')
nulK = p.create(td.nullCHOP,    'null_kick')
flt.par.filter = 'lowpass'
flt.par.units  = 'frequency'
flt.par.cutofffrequency = 140          # 킥 대역만 통과
anaK.par.function = 'rmspower'
mthK.par.fromrange1, mthK.par.fromrange2 = 0, 0.2
mthK.par.torange1,  mthK.par.torange2  = 0, 1
lagK.par.lag1, lagK.par.lag2 = 0.02, 0.25   # ★ 올라갈 땐 빠르게, 내려올 땐 천천히 = 펀치감
adev.outputConnectors[0].connect(flt.inputConnectors[0])
flt.outputConnectors[0].connect(anaK.inputConnectors[0])
anaK.outputConnectors[0].connect(mthK.inputConnectors[0])
mthK.outputConnectors[0].connect(lagK.inputConnectors[0])
lagK.outputConnectors[0].connect(nulK.inputConnectors[0])
flt.comment = '브랜치 B: 저역(<140Hz)만 → 킥 칠 때 화면 펀치'

# ── 입력 2: 마우스 → Displace 세기 ──
mou  = p.create(td.mouseinCHOP, 'mousein1')
lagM = p.create(td.lagCHOP,     'lag_mouse')
nulM = p.create(td.nullCHOP,    'null_mouse')
lagM.par.lag1, lagM.par.lag2 = 0.15, 0.15
mou.outputConnectors[0].connect(lagM.inputConnectors[0])
lagM.outputConnectors[0].connect(nulM.inputConnectors[0])
mou.comment = '입력 2: 마우스 = Displace(일렁임) 세기'

# ── TOP 체인: 웹캠 → Displace(노이즈) → HSV(색) → Transform(펀치) → Null ──
vid  = p.create(td.videodeviceinTOP, 'videodevin1')
noi  = p.create(td.noiseTOP,         'noise1')
dsp  = p.create(td.displaceTOP,      'displace1')
hsv  = p.create(td.hsvadjustTOP,     'hsvadj1')
xf   = p.create(td.transformTOP,     'transform1')
out  = p.create(td.nullTOP,          'null_out')
noi.par.tz.expr = 'absTime.seconds*0.3'      # 노이즈가 살아 움직이게
vid.outputConnectors[0].connect(dsp.inputConnectors[0])
noi.outputConnectors[0].connect(dsp.inputConnectors[1])
dsp.outputConnectors[0].connect(hsv.inputConnectors[0])
hsv.outputConnectors[0].connect(xf.inputConnectors[0])
xf.outputConnectors[0].connect(out.inputConnectors[0])

# ★ Referencing 3개 = 매핑
dsp.par.displaceweightx.expr = "abs(op('null_mouse')['tx'])*0.15"   # 마우스 → 일렁임
dsp.par.displaceweighty.expr = "abs(op('null_mouse')['ty'])*0.15"
hsv.par.hueoffset.expr = "op('null_level')['chan1']*360"            # 음량 → 색
xf.par.sx.expr = "1 + op('null_kick')['chan1']*0.35"                # 킥 → 펀치
xf.par.sy.expr = "1 + op('null_kick')['chan1']*0.35"
dsp.comment = '★ Referencing: 마우스=일렁임 / 음량=색 / 킥=펀치'

# ── 레이아웃 ──
rows = [
    (vid,0,100),(noi,0,250),(dsp,250,100),(hsv,450,100),(xf,650,100),(out,850,100),
    (adev,0,-100),(anaL,250,-100),(mthL,450,-100),(lagL,650,-100),(nulL,850,-100),
    (flt,250,-250),(anaK,450,-250),(mthK,650,-250),(lagK,850,-250),(nulK,1050,-250),
    (mou,0,-400),(lagM,250,-400),(nulM,450,-400),
]
for n,x,y in rows:
    n.nodeX, n.nodeY = x, y
out.viewer = True
out.display = True

# 검증
for c in p.children:
    c.cook(force=True)
report['children'] = sorted([c.name for c in p.children])
report['errors'] = {c.name: c.errors() for c in p.children if c.errors()}
result = report
