import td
import json as _j
report = {}
p = op('/project1/03_Audio')

# ── 기존 링-확대 물결 클러스터 제거 (유체 심으로 교체) ──
for nm in ('add_ripple','feedback_rip','transform_expand','level_decay',
           'blur_map','add_map','null_map','displace_water',
           'glsl_fluid','glsl_coord','glsl_image','fb_fluid','fb_coord',
           'dat_fluid','dat_coord','dat_image','add_force','blur_force','null_force'):
    o = p.op(nm)
    if o: o.destroy()

# ── 힘(force) 지도: 링 8개 + 개울 노이즈 ──
comp = p.op('comp_rings')
addf = p.create(td.addTOP,  'add_force')
blrf = p.create(td.blurTOP, 'blur_force')
nulf = p.create(td.nullTOP, 'null_force')
lvn  = p.op('level_creek')
lvn.par.opacity = 0.05                      # 유체에겐 아주 작은 힘이면 충분
comp.outputConnectors[0].connect(addf.inputConnectors[0])
lvn.outputConnectors[0].connect(addf.inputConnectors[1])
addf.outputConnectors[0].connect(blrf.inputConnectors[0])
try: blrf.par.size = 8
except Exception: pass
blrf.outputConnectors[0].connect(nulf.inputConnectors[0])

# ── 셰이더 코드 (textDAT) ──
FLUID = """// 유체 솔버 — xy:속도, z:압력, w:회전  (wyatt 스타일)
layout(location = 0) out vec4 fragColor;
vec2 R;
vec4 t(vec2 U){ return texture(sTD2DInputs[0], U/R); }          // 이전 프레임 유체
vec4 T(vec2 U){ U -= 0.5*t(U).xy; U -= 0.5*t(U).xy; return t(U); }  // 반보 되돌아가 샘플
void main(){
  R = uTD2DInfos[0].res.zw;
  vec2 U = vUV.st * R;
  vec4 C = T(U);
  float o = 1.;
  vec4 n=T(U+vec2(0,o)), e=T(U+vec2(o,0)), s=T(U-vec2(0,o)), w=T(U-vec2(o,0));
  C.x -= 0.25*(e.z-w.z - C.w*(n.w-s.w));
  C.y -= 0.25*(n.z-s.z - C.w*(e.w-w.w));
  C.z  = 0.25*((s.y-n.y+w.x-e.x)+(n.z+e.z+s.z+w.z));
  C.w  = 0.25*((s.x-n.x+w.y-e.y)-(n.w+e.w+s.w+w.w));
  C.xy *= 0.999;                                        // 점성 감쇠
  C.xy -= 0.001*(U - texture(sTD2DInputs[2], U/R).xy);  // 제자리로 돌아가려는 힘
  // ★ 소리 임펄스: 링 밝기만큼 중심→바깥 방향으로 물을 민다
  float m = texture(sTD2DInputs[1], U/R).r;
  vec2 dir = normalize(U - 0.5*R + vec2(1e-4));
  C.xy += dir * m * 1.0;
  if(U.x<2.||U.y<2.||R.x-U.x<2.||R.y-U.y<2.) C.xy *= 0.;  // 벽
  fragColor = C;
}"""

COORD = """// 좌표 추적 버퍼 — 각 픽셀의 '원래 자리'가 어디로 밀려갔는지 기억
layout(location = 0) out vec4 fragColor;
vec2 R;
vec4 F(vec2 U){ return texture(sTD2DInputs[1], U/R); }   // 유체 속도
vec4 t(vec2 U){ return texture(sTD2DInputs[0], U/R); }   // 이전 좌표
vec4 T(vec2 U){ U -= F(U).xy; U -= F(U).xy; return t(U); }
void main(){
  R = uTD2DInfos[0].res.zw;
  vec2 U = vUV.st * R;
  vec4 pv = t(U);
  vec4 Q = 0.25*(T(U+vec2(1,0))+T(U-vec2(1,0))+T(U+vec2(0,1))+T(U-vec2(0,1)));
  // 초기화: 피드백이 아직 검정(0,0)이면 자기 좌표로 시작
  if((pv.x==0. && pv.y==0.) || U.x<2.||U.y<2.||R.x-U.x<2.||R.y-U.y<2.) Q = vec4(U,0,0);
  fragColor = Q;
}"""

IMAGE = """// 렌더 — 밀려간 좌표대로 웹캠을 샘플 = 물에 비친 얼굴이 꿀렁임
layout(location = 0) out vec4 fragColor;
vec2 R;
vec4 A(vec2 U){ return texture(sTD2DInputs[0], U/R); }   // 좌표 버퍼
vec4 B(vec2 U){ return texture(sTD2DInputs[1], U/R); }   // 유체 (압력 음영용)
void main(){
  R = uTD2DInfos[0].res.zw;
  vec2 U = vUV.st * R;
  vec4 n=B(U+vec2(0,1)), e=B(U+vec2(1,0)), s=B(U-vec2(0,1)), w=B(U-vec2(1,0));
  vec2 g = vec2(e.z-w.z, n.z-s.z);                       // 압력 기울기 = 수면 음영
  fragColor = (1.-g.x)*texture(sTD2DInputs[2], A(U).xy/R);
}"""

dats = {}
for nm, code in (('dat_fluid',FLUID),('dat_coord',COORD),('dat_image',IMAGE)):
    d = p.create(td.textDAT, nm)
    d.text = code
    dats[nm] = d

# ── GLSL TOP 3개 + 피드백 2개 ──
gf = p.create(td.glslTOP, 'glsl_fluid')
gc = p.create(td.glslTOP, 'glsl_coord')
gi = p.create(td.glslTOP, 'glsl_image')
ff = p.create(td.feedbackTOP, 'fb_fluid')
fc = p.create(td.feedbackTOP, 'fb_coord')

RES = (960, 540)
for g, dat in ((gf,'dat_fluid'),(gc,'dat_coord'),(gi,'dat_image')):
    g.par.pixeldat = dats[dat]
    g.par.outputresolution = 'custom'
    g.par.resolutionw, g.par.resolutionh = RES
gf.par.format = 'rgba32float'
gc.par.format = 'rgba32float'

# 배선
gf.outputConnectors[0].connect(ff.inputConnectors[0])
gc.outputConnectors[0].connect(fc.inputConnectors[0])
ff.par.top = gf
fc.par.top = gc
# fluid: [0]=자기 피드백  [1]=힘 지도  [2]=좌표 피드백
ff.outputConnectors[0].connect(gf.inputConnectors[0])
nulf.outputConnectors[0].connect(gf.inputConnectors[1])
fc.outputConnectors[0].connect(gf.inputConnectors[2])
# coord: [0]=자기 피드백  [1]=유체
fc.outputConnectors[0].connect(gc.inputConnectors[0])
gf.outputConnectors[0].connect(gc.inputConnectors[1])
# image: [0]=좌표  [1]=유체  [2]=웹캠(거울)
flp = p.op('flip_mirror')
gc.outputConnectors[0].connect(gi.inputConnectors[0])
gf.outputConnectors[0].connect(gi.inputConnectors[1])
flp.outputConnectors[0].connect(gi.inputConnectors[2])

outn = p.op('null_out')
gi.outputConnectors[0].connect(outn.inputConnectors[0])
outn.viewer = True
outn.display = True

# ── 레이아웃 ──
POS = {
 'comp_rings':(250,250),'add_force':(470,250),'blur_force':(690,250),'null_force':(910,250),
 'noise_creek':(470,90),'level_creek':(690,90),
 'dat_fluid':(1150,80),'dat_coord':(1450,80),'dat_image':(1750,80),
 'fb_fluid':(1150,430),'glsl_fluid':(1150,250),
 'fb_coord':(1450,430),'glsl_coord':(1450,250),
 'glsl_image':(1750,250),'null_out':(1970,250),
 'select_cam':(0,-150),'flip_mirror':(220,-150),
}
for nm,(x,y) in POS.items():
    o = p.op(nm)
    if o: o.nodeX, o.nodeY = x, y

# ── 코멘트 ──
CM = {
 'add_force':  '힘 지도 합성 — 소리 링 + 개울 노이즈 = 물을 미는 힘',
 'blur_force': '블러 — 힘을 부드럽게 (뾰족한 힘 = 튀는 물)',
 'null_force': '출력 단자 — 힘 지도. 유체 셰이더의 2번 입력',
 'level_creek':'개울의 잔잔함 — Opacity 0.05. 유체에겐 작은 힘이면 충분',
 'glsl_fluid': '★유체 솔버 GLSL — xy:속도 z:압력 w:회전. 진짜 물리로 꿀렁임',
 'fb_fluid':   '유체의 기억 — 이전 프레임 상태 (시뮬레이션의 심장)',
 'glsl_coord': '좌표 추적 GLSL — 각 픽셀이 원래 어디 있었는지. 굴절의 지도',
 'fb_coord':   '좌표의 기억 — 이전 프레임 좌표',
 'glsl_image': '렌더 GLSL — 밀려간 좌표로 웹캠 샘플 + 압력 음영 = 물거울',
 'dat_fluid':  '유체 솔버 코드 — 속도·압력·회전 4이웃 업데이트',
 'dat_coord':  '좌표 추적 코드 — 속도 따라 반보씩 되돌아가 샘플',
 'dat_image':  '렌더 코드 — (1-압력기울기) × 웹캠(밀린 좌표)',
}
for nm, txt in CM.items():
    o = p.op(nm)
    if o: o.comment = txt

# 검증
for c in p.children:
    c.cook(force=True)
errs = {c.name: c.errors()[:200] for c in p.children if c.errors()}
report['nodes'] = len(p.children)
report['errors'] = errs
project.save()
report['saved'] = project.name
result = _j.dumps(report, ensure_ascii=False)
