# sink_basket_d_hook.py
# 싱크대 턱을 ㄷ자(앞·위·뒤)로 감싸고 Z자 형태로 바구니를 지지하는 설계
# 작성자: ChatGPT – 2025-05-26

import FreeCAD as App
import Part

doc = App.newDocument("SinkBasket_D_Hook")

# ────────── 사용자 파라미터 (모두 mm) ──────────
# 1) 싱크대 턱 관련 -------------------------------------------------
sink_thickness = 20.0       # 턱 실제 두께
clearance      = 0.5        # 여유 간격
hook_gap       = sink_thickness + clearance   # ㄷ자 내부 간극

front_drop     = 10         # 싱크 외측으로 내려가는 길이
inner_drop     = 40         # 싱크 내측으로 내려가는 길이
bottom_run     = 7          # 바구니 쪽으로 이어지는 길이
inner_lip      = 5          # 미니 턱(위로)

plate_thk      = 4          # 상판·벽 두께(=wall_t)

# 2) 바구니 본체 ----------------------------------------------------
basket_w       = 200        # 가로(좌우)
basket_d       = 80         # 앞뒤 돌출
basket_h       = 20         # 깊이(높이)
bottom_t       = 4          # 바닥 두께
wall_t         = plate_thk  # 옆·앞 벽 두께

# 3) 배수 구멍 ------------------------------------------------------
hole_d   = 7
rows     = 2
cols     = 7
gap_x    = (basket_w - 2*wall_t - cols*hole_d) / (cols-1)
gap_y    = (basket_d - rows*hole_d) / (rows+1)

# ────────── 1. ㄷ+Z 형태 훅 함수 ──────────
def make_d_hook(x0: float) -> Part.Shape:
    # 앞턱
    front = Part.makeBox(plate_thk, wall_t, front_drop)          # X,Y,Z
    front.rotate(App.Vector(0,0,0), App.Vector(0,0,1), 90)       # 세우기
    front.translate(App.Vector(0, 0, -front_drop))               # ↓

    # 상판 (턱 위)
    top = Part.makeBox(hook_gap, wall_t, plate_thk)               # X=간극, Y=두께

    # 뒤벽(싱크 안쪽)
    back = Part.makeBox(plate_thk, wall_t, inner_drop)
    back.rotate(App.Vector(0,0,0), App.Vector(0,0,1), 90)
    back.translate(App.Vector(hook_gap - plate_thk,
                              0,
                              -inner_drop))

    # 바닥으로 이어지는 Z자
    bottom = Part.makeBox(bottom_run, wall_t, plate_thk)
    bottom.translate(App.Vector(hook_gap - plate_thk,
                                0,
                                -inner_drop - plate_thk))

    # 위로 살짝 올린 미니 턱(흘러내림 방지)
    lip = Part.makeBox(plate_thk, wall_t, inner_lip)
    lip.rotate(App.Vector(0,0,0), App.Vector(0,0,1), 90)
    lip.translate(App.Vector(hook_gap - plate_thk + bottom_run - plate_thk,
                             0,
                             -inner_drop - inner_lip))

    hook = top.fuse(front).fuse(back).fuse(bottom).fuse(lip)
    hook.translate(App.Vector(x0, 0, 0))
    return hook

# 왼쪽·오른쪽 두 개 훅 생성
hook_left  = make_d_hook(0)
hook_right = make_d_hook(basket_w - hook_gap)
hooks = hook_left.fuse(hook_right)

# ────────── 2. 뒤판 (바구니 지지벽) ──────────
back_wall_h = inner_drop + basket_h
back_wall   = Part.makeBox(basket_w, wall_t, back_wall_h)
back_wall.translate(App.Vector(0, -wall_t, -back_wall_h))

# ────────── 3. 바구니 본체 ──────────
# 바닥
bottom = Part.makeBox(basket_w, basket_d, bottom_t)
bottom.translate(App.Vector(0, -(wall_t + basket_d), -basket_h))

# 좌‧우‧앞 벽
left_wall  = Part.makeBox(wall_t, basket_d, basket_h)
left_wall.translate(App.Vector(0, -(wall_t + basket_d), -basket_h))

right_wall = Part.makeBox(wall_t, basket_d, basket_h)
right_wall.translate(App.Vector(basket_w - wall_t,
                                -(wall_t + basket_d),
                                -basket_h))

front_wall = Part.makeBox(basket_w, wall_t, basket_h)
front_wall.translate(App.Vector(0,
                                -(wall_t + basket_d) - wall_t,
                                -basket_h))

basket = bottom.fuse(left_wall).fuse(right_wall).fuse(front_wall)

# ────────── 4. 배수 구멍 뚫기 ──────────
start_x = wall_t + hole_d/2
start_y = hole_d/2 + gap_y
for r in range(rows):
    for c in range(cols):
        x = start_x + c*(hole_d + gap_x)
        y = -(wall_t + start_y + r*(hole_d + gap_y))
        cyl = Part.makeCylinder(hole_d/2,
                                bottom_t+0.2,
                                App.Vector(x, y, -basket_h - bottom_t),
                                App.Vector(0,0,1))
        basket = basket.cut(cyl)

# ────────── 5. 모든 파트 결합 & STEP 저장 ──────────
assembly = hooks.fuse(back_wall).fuse(basket)
obj = doc.addObject("Part::Feature", "SinkBasket")
obj.Shape = assembly
doc.recompute()

Part.export([obj], "sink_drying_hanger.step")
print("✅ sink_drying_hanger.step 저장 완료")


# 실행 방법: 터미널에서 아래 명령어 실행
# freecadcmd sink_drying_hanger.py