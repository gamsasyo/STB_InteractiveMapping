import td
import json as _j
report = {}
p = op('/project1/03_Audio')

# ── 기존 단일 displace 제거, 기울기 굴절 리그로 교체 ──
for nm in ('displace_water','t_xp','t_xn','t_yp','t_yn','comp_dx','comp_dy',
           'lvl_dx','lvl_dy','displace_x','displace_y'):
    o = p.op(nm)
    if o: o.destroy()

nmap = p.op('null_map')

def grad(axis):
    # 맵을 ±2px 밀어서 빼면 = 그 방향 기울기
    tp = p.create(td.transformTOP, 't_%sp' % axis)
    tn = p.create(td.transformTOP, 't_%sn' % axis)
    for t, sign in ((tp, 1), (tn, -1)):
        try:
            t.par.tunit = 'pixels'
            setattr(t.par, 't' + axis, 2 * sign)
        except Exception:
            setattr(t.par, 't' + axis, (2.0/960) * sign)
        nmap.outputConnectors[0].connect(t.inputConnectors[0])
    co = p.create(td.compositeTOP, 'comp_d' + axis)
    co.par.operand = 'subtract'
    co.par.format = 'rgba16float'          # 음수 살리기
    tp.outputConnectors[0].connect(co.inputConnectors[0])
    tn.outputConnectors[0].connect(co.inputConnectors[1])
    lv = p.create(td.levelTOP, 'lvl_d' + axis)
    lv.par.inlow, lv.par.inhigh = -0.5, 0.5    # ±0.5 기울기 → 0~1
    lv.par.outlow, lv.par.outhigh = 0, 1
    co.outputConnectors[0].connect(lv.inputConnectors[0])
    return tp, tn, co, lv

txp, txn, cdx, ldx = grad('x')
typ_, tyn, cdy, ldy = grad('y')

# ── Displace 2개 직렬: x 굴절 → y 굴절 ──
flp, outn = p.op('flip_mirror'), p.op('null_out')
dx = p.create(td.displaceTOP, 'displace_x')
dy = p.create(td.displaceTOP, 'displace_y')
flp.outputConnectors[0].connect(dx.inputConnectors[0])
ldx.outputConnectors[0].connect(dx.inputConnectors[1])
dx.outputConnectors[0].connect(dy.inputConnectors[0])
ldy.outputConnectors[0].connect(dy.inputConnectors[1])
dy.outputConnectors[0].connect(outn.inputConnectors[0])
for d in (dx, dy):
    d.par.midpointx = 0.5
    d.par.midpointy = 0.5
dx.par.displaceweightx.expr = "0.06 + op('null_master')['bin1']*0.25"
dx.par.displaceweighty = 0
dy.par.displaceweightx = 0
dy.par.displaceweighty.expr = "0.06 + op('null_master')['bin1']*0.25"
outn.viewer = True
outn.display = True

# ── 레이아웃 ──
POS = {
 't_xp':(1570,410),'t_xn':(1570,330),'comp_dx':(1790,370),'lvl_dx':(2010,370),
 't_yp':(1570,190),'t_yn':(1570,110),'comp_dy':(1790,150),'lvl_dy':(2010,150),
 'displace_x':(2230,260),'displace_y':(2450,260),'null_out':(2670,260),
}
for nm,(x,y) in POS.items():
    o = p.op(nm)
    if o: o.nodeX, o.nodeY = x, y

# ── 코멘트 ──
CM = {
 't_xp':'맵을 오른쪽 2px 이동','t_xn':'맵을 왼쪽 2px 이동',
 'comp_dx':'빼기 = x방향 기울기 (수면의 경사). Format 16f = 음수 보존',
 'lvl_dx':'기울기 ±0.5 → 0~1 (Displace 미드포인트 0.5 기준)',
 't_yp':'맵을 위로 2px 이동','t_yn':'맵을 아래로 2px 이동',
 'comp_dy':'빼기 = y방향 기울기','lvl_dy':'기울기 ±0.5 → 0~1',
 'displace_x':'x 굴절 — 수면 경사 방향으로만. 물리적으로 정확한 굴절',
 'displace_y':'y 굴절 — 직렬로 한 번 더. 링이 사방으로 자연스럽게 민다',
}
for nm, txt in CM.items():
    o = p.op(nm)
    if o: o.comment = txt

for c in p.children:
    c.cook(force=True)
errs = {c.name: c.errors()[:150] for c in p.children if c.errors()}
report['errors'] = errs
report['nodes'] = len(p.children)
project.save()
report['saved'] = project.name
result = _j.dumps(report, ensure_ascii=False)
