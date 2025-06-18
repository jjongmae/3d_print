import FreeCAD as App
import Part

doc = App.newDocument("ScoopDock")

# ───── 설정값 ─────
pin_diameter = 3.0      # 핀의 지름 (mm)
pin_radius   = pin_diameter / 2  # 핀의 반지름 (mm)
pin_length   = 30         # 핀의 노출 길이 (mm)
embed        = 2          # 베이스에 박히는 핀의 길이 (mm)
pin_spacing  = 40         # 핀 간격 (mm)
pin_count    = 1          # 핀 개수
base_t       = 5          # 베이스 두께 (mm)
base_h       = 50         # 베이스 높이 (mm)
base_w       = pin_spacing * (pin_count - 1) + 20  # 베이스 폭 (mm)

# ───── 베이스판 ─────
solid = Part.makeBox(base_w, base_t, base_h)

# ───── 핀 생성 & Fuse ─────
for i in range(pin_count):
    x_pos = 10 + i * pin_spacing
    pin = Part.makeCylinder(pin_radius,
                            pin_length + embed,
                            App.Vector(x_pos, 0, base_h/2),
                            App.Vector(0, -1, 0))      # -Y 축
    solid = solid.fuse(pin)

# ───── 결과 표시 & STEP 저장 ─────
obj = doc.addObject("Part::Feature", "ScoopDock")
obj.Shape = solid
doc.recompute()
Part.export([obj], "scoop_dock.step")
print("✅ 3 mm 핀으로 scoop_dock.step 생성 완료")

# 실행 방법: 터미널에서 아래 명령어 실행
# freecadcmd scoop_dock.py