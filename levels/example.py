"""
Minimal example level — demonstrates gd_lib usage.
Run with: python levels/example.py
"""
import sys
sys.path.insert(0, ".")

from gd_lib import *

reset()

# Ground
ground(0, 30)

# Simple obstacle sequence
sp(4)
ground(6, 10)
yellow_pad(12)
sp(16)
sp(18)
ground(20, 30)

# Color: warm teal opening
color_trigger(0, 1,    r=0,   g_=180, b=160, duration=0.0)
color_trigger(0, 1000, r=5,   g_=20,  b=18,  duration=0.0)

validate()

lvl = build("Example Level", song_id=1, description="gd_lib example", version=1)
lvl.to_file("output/Example.gmd")
print("Exported output/Example.gmd")
