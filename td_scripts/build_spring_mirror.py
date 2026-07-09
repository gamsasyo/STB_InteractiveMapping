import td
import json as _j
report = {}
p = op('/project1/03_Audio')

# ── GLSL 유체 클러스터 + 옛 잔재 제거 ──
for nm in ('glsl_fluid','glsl_coord','glsl_image','fb_fluid','fb_coord',
           'dat_fluid','dat_coord','dat_image','add_force','blur_force','null_force',
           'add_ripple','feedback_rip','transform_expand','level_decay',
           'blur_map','add_map','null_map','displace_water','lag_water'):
    o = p.op(nm)
    if o: o.destroy()

# ── ① 소리 체인에 Spring 삽입: rename_bins → spring_water → null_bins ──
ren, nbin = p.op('rename_bins'), p.op('null_bins')
spr = p.create(td.springCHOP, 'spring_water')
spr.par.springk  = 60     # 스프링 강성 — 클수록 빠르게 통통
spr.par.dampingk = 4      # 감쇠 — 작을수록 오래 출렁 (임계감쇠보다 한참 아래)
spr.par.mass     = 1
ren.outputConnectors[0].connect(spr.inputConnectors[0])
spr.outputConnectors[0].connect(nbin.inputConnectors[0])
for nm,x in [('audiodevin1',0),('audiospectrum1',220),('shuffle_8bins',440),('analyze_bins',660),('math_norm',880),('rename_bins',1100),('spring_water',1320),('null_bins',1540)]:
    p.op(nm).nodeX, p.op(nm).nodeY = x, -400

# ── 마스터 바운스: 8빈 평균 → Spring → 화면 전체 굴절 세기 ──
msum = p.create(td.mathCHOP,   'math_master')
sprm = p.create(td.springCHOP, 'spring_bounce')
nmas = p.create(td.nullCHOP,   'null_master')
msum.par.chopop = 'add'            # 채널 합치기(합)
nbin.outputConnectors[0].connect(msum.inputConnectors[0])
msum.outputConnectors[0].connect(sprm.inputConnectors[0])
sprm.outputConnectors[0].connect(nmas.inputConnectors[0])
sprm.par.springk, sprm.par.dampingk = 40, 3
for n,x in [(msum,1100),(sprm,1320),(nmas,1540)]:
    n.nodeX, n.nodeY = x, -560

# ── ② 물결 지도: 링(스프링 밝기) → 피드백 확대 = 퍼짐 ──
comp = p.op('comp_rings')
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
xfe.par.sx = xfe.par.sy = 1.05
lvd.par.opacity = 0.92

blurm = p.create(td.blurTOP, 'blur_map')
addr.outputConnectors[0].connect(blurm.inputConnectors[0])
try: blurm.par.size = 14
except Exception: pass

# 개울 노이즈: 컬러(rg = x·y 방향), displace에 직접 살짝
noi, lvn = p.op('noise_creek'), p.op('level_creek')
noi.par.mono = 0
lvn.par.opacity = 0.15
if not lvn.inputConnectors[0].connections:
    noi.outputConnectors[0].connect(lvn.inputConnectors[0])

addm = p.create(td.addTOP,  'add_map')
nmap = p.create(td.nullTOP, 'null_map')
blurm.outputConnectors[0].connect(addm.inputConnectors[0])
lvn.outputConnectors[0].connect(addm.inputConnectors[1])
addm.outputConnectors[0].connect(nmap.inputConnectors[0])
for n,x,y in [(comp,250,250),(addr,470,250),(fb,470,470),(xfe,690,470),(lvd,910,470),
              (blurm,690,250),(noi,690,90),(lvn,910,90),(addm,1130,250),(nmap,1350,250)]:
    n.nodeX, n.nodeY = x, y

# ── ③ 거울: Displace, 웨이트는 스프링 마스터로 바운스 ──
flp = p.op('flip_mirror')
dsp = p.create(td.displaceTOP, 'displace_water')
outn = p.op('null_out')
flp.outputConnectors[0].connect(dsp.inputConnectors[0])
nmap.outputConnectors[0].connect(dsp.inputConnectors[1])
dsp.outputConnectors[0].connect(outn.inputConnectors[0])
dsp.par.midpointx = 0
dsp.par.midpointy = 0
dsp.par.displaceweightx.expr = "0.03 + op('null_master')['bin1']*0.05"
dsp.par.displaceweighty.expr = "0.03 + op('null_master')['bin1']*0.05"
for n,x,y in [(dsp,1570,50),(outn,1790,50)]:
    n.nodeX, n.nodeY = x, y
outn.viewer = True
outn.display = True

# ── 코멘트 ──
CM = {
 'spring_water':  '★스프링 CHOP — 값이 목표를 지나쳐 튕기며 가라앉음 = 꿀렁의 물리. Spring(강성)·Damping(감쇠)',
 'math_master':   '채널 합치기 — 8빈 합 = 전체 소리 에너지',
 'spring_bounce': '스프링 CHOP — 화면 전체 굴절 세기가 통통 바운스',
 'null_master':   '출력 단자 — displace 웨이트로 (0.03 + 값*0.05)',
 'add_ripple':    '합성 — 새 링 + 퍼지고 있는 링(피드백)',
 'feedback_rip':  '이전 프레임 기억 — Target: add_ripple. 파동 퍼짐의 심장',
 'transform_expand':'확대 — Scale 1.05/프레임 = 링이 바깥으로 이동',
 'level_decay':   '감쇠 — Opacity 0.92. 퍼질수록 흐려짐',
 'blur_map':      '블러 — 링 경계를 물결답게',
 'noise_creek':   '노이즈 TOP(컬러) — rg = x·y 방향 미세 일렁임. 잔잔한 개울',
 'level_creek':   '개울 잔잔함 — Opacity 0.15',
 'add_map':       '물결 지도 완성 — 파동 + 기본 일렁임',
 'null_map':      '출력 단자 — displace의 2번 입력',
 'displace_water':'픽셀 굴절 — 웨이트가 스프링으로 바운스 (0.03~0.08)',
 'null_out':      '출력 단자 — 완성: 소리에 꿀렁이는 물거울',
}
for nm, txt in CM.items():
    o = p.op(nm)
    if o: o.comment = txt

for c in p.children:
    c.cook(force=True)
errs = {c.name: c.errors()[:150] for c in p.children if c.errors()}
report['nodes'] = len(p.children)
report['errors'] = errs
report['master_chans'] = [ch.name for ch in p.op('null_master').chans()]
project.save()
report['saved'] = project.name
result = _j.dumps(report, ensure_ascii=False)
