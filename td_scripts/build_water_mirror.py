import td
import json as _j
report = {}

# ── 03_Audio 재구축: 개울 물거울 (심화) ──
# 박수 → 스펙트럼 8빈 → 링 파동이 중심에서 퍼지며 → 서서히 잔잔해짐
p = op('/project1/03_Audio')
for c in list(p.children):
    c.destroy()

# ═══ ① 소리 → 8빈 ═══════════════════════════════ (y=-400줄)
adev = p.create(td.audiodeviceinCHOP, 'audiodevin1')
spec = p.create(td.audiospectrumCHOP, 'audiospectrum1')
shuf = p.create(td.shuffleCHOP,       'shuffle_8bins')
ana  = p.create(td.analyzeCHOP,       'analyze_bins')
mth  = p.create(td.mathCHOP,          'math_norm')
ren  = p.create(td.renameCHOP,        'rename_bins')
lag  = p.create(td.lagCHOP,           'lag_water')
nbin = p.create(td.nullCHOP,          'null_bins')

adev.outputConnectors[0].connect(spec.inputConnectors[0])
spec.outputConnectors[0].connect(shuf.inputConnectors[0])
shuf.outputConnectors[0].connect(ana.inputConnectors[0])
ana.outputConnectors[0].connect(mth.inputConnectors[0])
mth.outputConnectors[0].connect(ren.inputConnectors[0])
ren.outputConnectors[0].connect(lag.inputConnectors[0])
lag.outputConnectors[0].connect(nbin.inputConnectors[0])

shuf.par.method = 'splitn'          # 스펙트럼을 N구간으로 쪼개기
for pname in ('nval','n','numsplits'):
    try:
        setattr(shuf.par, pname, 8); break
    except Exception: pass
ana.par.function = 'maximum'        # 구간 대표값 = 최대 (박수 펀치가 살게)
mth.par.fromrange1, mth.par.fromrange2 = 0, 0.4
mth.par.torange1,  mth.par.torange2  = 0, 1
try:
    ren.par.renamefrom = '*'
    ren.par.renameto = 'bin[1-8]'
except Exception: pass
lag.par.lag1, lag.par.lag2 = 0.02, 0.8   # 올림 즉각 / 내림 천천히 = 물결이 잔잔해지는 필터

for n,x in [(adev,0),(spec,220),(shuf,440),(ana,660),(mth,880),(ren,1100),(lag,1320),(nbin,1540)]:
    n.nodeX, n.nodeY = x, -400

# ═══ ② 물결 지도: 링 8개 + 퍼짐(피드백) + 개울 노이즈 ═══ (y=0~550)
rings = []
for i in range(8):
    ci = p.create(td.circleTOP, 'ring%d' % (i+1))
    ci.par.radiusx = ci.par.radiusy = 0.05 + 0.04*i      # 저음=안쪽, 고음=바깥쪽
    try: ci.par.fillalpha = 0
    except Exception: pass
    ci.par.borderwidth = 0.012
    ch = "op('null_bins')['bin%d']" % (i+1)
    ci.par.borderr.expr = ch
    ci.par.borderg.expr = ch
    ci.par.borderb.expr = ch
    ci.comment = '링 %d — 밝기 ← bin%d (%s역)' % (i+1, i+1, '저음' if i < 3 else ('중음' if i < 6 else '고음'))
    ci.nodeX, ci.nodeY = 0, 520 - 70*i
    rings.append(ci)

comp = p.create(td.compositeTOP, 'comp_rings')
comp.par.operand = 'add'
for i, ci in enumerate(rings):
    ci.outputConnectors[0].connect(comp.inputConnectors[i])

# 퍼져나감: Feedback + Scale-up 루프
addr = p.create(td.addTOP,       'add_ripple')
fb   = p.create(td.feedbackTOP,  'feedback_rip')
xfe  = p.create(td.transformTOP, 'transform_expand')
lvd  = p.create(td.levelTOP,     'level_decay')
comp.outputConnectors[0].connect(addr.inputConnectors[0])
comp.outputConnectors[0].connect(fb.inputConnectors[0])
fb.outputConnectors[0].connect(xfe.inputConnectors[0])
xfe.outputConnectors[0].connect(lvd.inputConnectors[0])
lvd.outputConnectors[0].connect(addr.inputConnectors[1])
fb.par.top = addr
xfe.par.sx = xfe.par.sy = 1.06      # 매 프레임 6% 확대 = 링이 바깥으로 이동
lvd.par.opacity = 0.90               # 퍼지면서 서서히 사라짐

blurm = p.create(td.blurTOP, 'blur_map')
addr.outputConnectors[0].connect(blurm.inputConnectors[0])
for pname in ('size','sizex'):
    try:
        setattr(blurm.par, pname, 12); break
    except Exception: pass

# 잔잔한 개울 기본 일렁임
noib = p.create(td.noiseTOP, 'noise_creek')
lvn  = p.create(td.levelTOP, 'level_creek')
noib.par.tz.expr = 'absTime.seconds*0.08'
noib.outputConnectors[0].connect(lvn.inputConnectors[0])
lvn.par.opacity = 0.18

addm = p.create(td.addTOP,  'add_map')
nmap = p.create(td.nullTOP, 'null_map')
blurm.outputConnectors[0].connect(addm.inputConnectors[0])
lvn.outputConnectors[0].connect(addm.inputConnectors[1])
addm.outputConnectors[0].connect(nmap.inputConnectors[0])

for n,x,y in [(comp,250,250),(addr,470,250),(fb,470,470),(xfe,690,470),(lvd,910,470),
              (blurm,690,250),(noib,690,90),(lvn,910,90),(addm,1130,250),(nmap,1350,250)]:
    n.nodeX, n.nodeY = x, y

# ═══ ③ 거울: 웹캠 → 물결로 굴절 ═══════════════════ (y=-150줄)
sel  = p.create(td.selectTOP,   'select_cam')
flp  = p.create(td.flipTOP,     'flip_mirror')
dsp  = p.create(td.displaceTOP, 'displace_water')
outn = p.create(td.nullTOP,     'null_out')
sel.par.top = '/project1/02_Webcam/videodevin1'
flp.par.flipx = 1
sel.outputConnectors[0].connect(flp.inputConnectors[0])
flp.outputConnectors[0].connect(dsp.inputConnectors[0])
nmap.outputConnectors[0].connect(dsp.inputConnectors[1])
dsp.outputConnectors[0].connect(outn.inputConnectors[0])
dsp.par.displaceweightx = 0.08
dsp.par.displaceweighty = 0.08
dsp.par.midpointx = 0
dsp.par.midpointy = 0
for n,x,y in [(sel,0,-150),(flp,220,-150),(dsp,1570,50),(outn,1790,50)]:
    n.nodeX, n.nodeY = x, y
outn.viewer = True
outn.display = True

# ═══ 코멘트 (오퍼레이터 사전) ═══
CM = {
 'audiodevin1':    '마이크 입력 CHOP — 주요: Device · Active',
 'audiospectrum1': '스펙트럼 분석 CHOP — 소리를 주파수별 세기로. 주요: FFT Size · High Freq Boost',
 'shuffle_8bins':  '샘플 재배열 CHOP — Split into N(8) = 스펙트럼을 8구간으로 쪼갬',
 'analyze_bins':   '채널 분석 CHOP — Function: Maximum = 각 구간의 대표값 → 8채널',
 'math_norm':      '범위 변환 — From 0~0.4 → To 0~1. 공용어(0~1)로 정규화',
 'rename_bins':    '채널 이름 변경 — chan* → bin1~bin8. 이름이 곧 의미',
 'lag_water':      '★물결 필터 — 올림 0.02(즉각) / 내림 0.8(천천히 0으로) = 물이 잔잔해지는 시간',
 'null_bins':      '출력 단자 — bin1~8 (0~1). 링 8개의 밝기로',
 'comp_rings':     '합성 TOP — 링 8개를 Add로 겹침 = 소리의 단면',
 'add_ripple':     '합성 — 새 링 + 퍼지고 있는 링(피드백). 파동의 누적',
 'feedback_rip':   '이전 프레임 기억 — Target: add_ripple. 파동 퍼짐의 심장',
 'transform_expand':'확대 — Scale 1.06/프레임 = 링이 중심에서 바깥으로 이동',
 'level_decay':    '감쇠 — Opacity 0.90. 퍼질수록 흐려짐 (에너지 소멸)',
 'blur_map':       '블러 — 링 경계를 물결답게 부드럽게',
 'noise_creek':    '노이즈 TOP — 시간 연결(tz) = 잔잔한 개울의 기본 일렁임',
 'level_creek':    '노이즈 세기 — Opacity 0.18. 개울의 "잔잔함" 정도',
 'add_map':        '물결 지도 완성 — 파동 + 기본 일렁임',
 'null_map':       '출력 단자 — 물결 지도. displace의 2번 입력으로',
 'select_cam':     '참조 TOP — 웹캠은 02_Webcam과 공유 (장치는 한 곳에서만)',
 'flip_mirror':    '거울 반전 — Flip X. 개울에 비친 나',
 'displace_water': '픽셀 굴절 TOP — 물결 지도가 밝은 곳의 픽셀을 밀어냄. Weight 0.08 = 굴절 세기',
 'null_out':       '출력 단자 — 완성: 소리에 흔들리는 물거울',
}
for nm, txt in CM.items():
    o = p.op(nm)
    if o: o.comment = txt

# 검증
for c in p.children:
    c.cook(force=True)
errs = {c.name: c.errors()[:100] for c in p.children if c.errors()}
report['nodes'] = len(p.children)
report['errors'] = errs
report['bin_channels'] = [ch.name for ch in nbin.chans()]
report['bin_values'] = [round(float(ch[0]), 4) for ch in nbin.chans()]
project.save()
report['saved'] = project.name
result = _j.dumps(report, ensure_ascii=False)
