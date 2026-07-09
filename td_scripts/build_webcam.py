import td
p = op('/project1/base1')

# 깨끗하게 시작
for c in list(p.children):
    c.destroy()

# ── TOP 체인: 웹캠 → 엣지 → (피드백 잔상) → 트랜스폼 → 널 ──
vid   = p.create(td.videodeviceinTOP, 'videodevin1')
edge  = p.create(td.edgeTOP,          'edge1')
fb    = p.create(td.feedbackTOP,      'feedback1')
fade  = p.create(td.levelTOP,         'level_fade')
add   = p.create(td.addTOP,           'add1')
xform = p.create(td.transformTOP,     'transform1')
out   = p.create(td.nullTOP,          'null1')

# ── CHOP: 마우스 → 부드럽게 → 널 ──
mouse = p.create(td.mouseinCHOP, 'mousein1')
lag   = p.create(td.lagCHOP,     'lag1')
shake = p.create(td.nullCHOP,    'null_shake')

# ── 와이어 ──
vid.outputConnectors[0].connect(edge.inputConnectors[0])
edge.outputConnectors[0].connect(add.inputConnectors[0])
fb.outputConnectors[0].connect(fade.inputConnectors[0])
fade.outputConnectors[0].connect(add.inputConnectors[1])
add.outputConnectors[0].connect(xform.inputConnectors[0])
xform.outputConnectors[0].connect(out.inputConnectors[0])
edge.outputConnectors[0].connect(fb.inputConnectors[0])
mouse.outputConnectors[0].connect(lag.inputConnectors[0])
lag.outputConnectors[0].connect(shake.inputConnectors[0])

# ── 파라미터 ──
fb.par.top = add                 # 피드백 루프 타겟
fade.par.opacity = 0.92          # 잔상 감쇠율
lag.par.lag1 = 0.15              # 마우스 스무딩
lag.par.lag2 = 0.15
# ★ Referencing: 마우스가 화면을 흔든다
xform.par.tx.expr = "op('null_shake')['tx']*0.3"
xform.par.ty.expr = "op('null_shake')['ty']*0.3"

# ── 레이아웃 ──
row_top  = [(vid,0,0),(edge,200,0),(add,400,0),(xform,600,0),(out,800,0)]
row_fb   = [(fb,200,150),(fade,400,150)]
row_chop = [(mouse,200,-200),(lag,400,-200),(shake,600,-200)]
for n,x,y in row_top+row_fb+row_chop:
    n.nodeX, n.nodeY = x, y

out.viewer = True
out.display = True

result = {'created': [c.name for c in p.children], 'errors': []}
