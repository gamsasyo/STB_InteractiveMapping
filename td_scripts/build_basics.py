import td
report = {}

# ── 1) base1 → 웹캠(가능하면 한글, 안 되면 webcam) ──
b1 = op('/project1/base1')
try:
    b1.name = '웹캠'
except Exception:
    b1.name = 'webcam'
report['webcam_base'] = b1.name

# ── 2) basics 베이스 생성 ──
proj = op('/project1')
old = proj.op('basics')
if old: old.destroy()
p = proj.create(td.baseCOMP, 'basics')
p.nodeX, p.nodeY = b1.nodeX, b1.nodeY + 200
p.comment = '가이드 빌드 ① 베이직 — 슬라이드 8과 핑퐁'

# ── 클러스터 A: ① 첫 노드 체인 ──
rect  = p.create(td.rectangleTOP, 'rectangle1')
xf    = p.create(td.transformTOP, 'transform1')
lvl   = p.create(td.levelTOP,     'level1')
nul   = p.create(td.nullTOP,      'null1')
rect.outputConnectors[0].connect(xf.inputConnectors[0])
xf.outputConnectors[0].connect(lvl.inputConnectors[0])
lvl.outputConnectors[0].connect(nul.inputConnectors[0])
rect.comment = '① 첫 노드 체인: 만들고-잇고-파라미터'
for n,x in [(rect,0),(xf,200),(lvl,400),(nul,600)]:
    n.nodeX, n.nodeY = x, 400

# ── 클러스터 B: ② 자주 쓰는 TOP ──
circ  = p.create(td.circleTOP,      'circle1')
mov   = p.create(td.moviefileinTOP, 'moviefilein1')
ramp  = p.create(td.rampTOP,        'ramp1')
noi   = p.create(td.noiseTOP,       'noise1')
circ.comment = '② 자주 쓰는 TOP 둘러보기'
for n,x in [(circ,0),(mov,200),(ramp,400),(noi,600)]:
    n.nodeX, n.nodeY = x, 150

# ── 클러스터 C: ③ 스스로 움직이는 값 ──
lfo   = p.create(td.lfoCHOP,      'lfo1')
nrot  = p.create(td.nullCHOP,     'null_wobble')
lfo.outputConnectors[0].connect(nrot.inputConnectors[0])

con   = p.create(td.constantCHOP, 'constant1')
spd   = p.create(td.speedCHOP,    'speed1')
nspin = p.create(td.nullCHOP,     'null_spin')
con.par.value0 = 30            # 초당 30도
con.outputConnectors[0].connect(spd.inputConnectors[0])
spd.outputConnectors[0].connect(nspin.inputConnectors[0])

lfo2  = p.create(td.lfoCHOP,  'lfo2')
mth   = p.create(td.mathCHOP, 'math1')
nhue  = p.create(td.nullCHOP, 'null_hue')
mth.par.fromrange1, mth.par.fromrange2 = -1, 1
mth.par.torange1,  mth.par.torange2  = 0, 360
lfo2.outputConnectors[0].connect(mth.inputConnectors[0])
mth.outputConnectors[0].connect(nhue.inputConnectors[0])
lfo2.par.frequency = 0.2
lfo.comment = '③ LFO=반복 / Speed=누적 / Math=리매핑(-1~1 → 0~360)'
for n,x,y in [(lfo,0,-100),(nrot,200,-100),(con,0,-250),(spd,200,-250),(nspin,400,-250),(lfo2,0,-400),(mth,200,-400),(nhue,400,-400)]:
    n.nodeX, n.nodeY = x, y

# ── 클러스터 D: ④⑤ Referencing → 미니 모션그래픽 ──
rect2 = p.create(td.rectangleTOP, 'rectangle2')
xf2   = p.create(td.transformTOP, 'transform2')
try:
    hsv = p.create(td.hsvadjustTOP, 'hsvadj1')
except Exception:
    hsv = p.create(td.hsvtorgbTOP, 'hsvadj1')  # fallback
fin   = p.create(td.nullTOP, 'null_final')
rect2.outputConnectors[0].connect(xf2.inputConnectors[0])
xf2.outputConnectors[0].connect(hsv.inputConnectors[0])
hsv.outputConnectors[0].connect(fin.inputConnectors[0])
rect2.par.fillcolorr, rect2.par.fillcolorg, rect2.par.fillcolorb = 1, 0.15, 0.09
rect2.par.sizex, rect2.par.sizey = 0.3, 0.3
xf2.par.rotate.expr = "op('null_spin')['chan1']"          # ★ Referencing: 스스로 돎
hsv.par.hueoffset.expr = "op('null_hue')['chan1']"        # ★ Referencing: 색 순환
rect2.comment = '④⑤ Referencing 완성작: 스스로 돌고 색이 순환하는 사각형'
for n,x in [(rect2,600,),(xf2,800),(hsv,1000),(fin,1200)]:
    pass
for n,x in [(rect2,600),(xf2,800),(hsv,1000),(fin,1200)]:
    n.nodeX, n.nodeY = x, -250
fin.viewer = True
fin.display = True

# 검증
for c in p.children:
    c.cook(force=True)
report['basics_children'] = sorted([c.name for c in p.children])
report['errors'] = {c.name: c.errors() for c in p.children if c.errors()}
result = report
