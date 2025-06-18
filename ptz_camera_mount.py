import FreeCAD
import Part
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(script_dir, "ptz_camera_mount.step")

doc = FreeCAD.newDocument("ptz_camera_mount")

# 파라미터
outer_diameter = 210        # 전체 지름
wall_thickness = 10         # 벽 두께
height = 80                 # 전체 높이
bottom_thickness = 10       # 바닥 두께
hole_diameter = 20          # 전선 구멍 지름
hole_height = 20            # 바닥으로부터 구멍 위치

# 외부 실린더
outer_cyl = Part.makeCylinder(outer_diameter / 2, height)

# 내부 실린더
inner_diameter = outer_diameter - 2 * wall_thickness
inner_height = height - bottom_thickness
inner_cyl = Part.makeCylinder(inner_diameter / 2, inner_height)
inner_cyl.translate(FreeCAD.Vector(0, 0, bottom_thickness))

# 전선 구멍 (옆면 → 수평, X축 방향으로 관통)
hole_length = outer_diameter  # 충분히 길게 뚫어서 양쪽 관통
hole_cyl = Part.makeCylinder(hole_diameter / 2, hole_length)

# 위치 조정: 바닥에서 20mm 위, 옆면을 X축 방향으로 관통
# 회전: Y축으로 90도 돌려서 X방향으로 구멍 나게 함
hole_cyl.rotate(FreeCAD.Vector(0,0,0), FreeCAD.Vector(0,1,0), 90)
hole_cyl.translate(FreeCAD.Vector(-hole_length/2, outer_diameter/2 - wall_thickness/2, hole_height))

# 구조물 만들기
hollow = outer_cyl.cut(inner_cyl)
final = hollow.cut(hole_cyl)

# 객체 추가
obj = doc.addObject("Part::Feature", "ptz_camera_mount")
obj.Shape = final

# STEP 파일 저장
Part.export([obj], output_path)

doc.recompute()

# 실행 방법: 터미널에서 아래 명령어 실행
# freecadcmd ptz_camera_mount.py