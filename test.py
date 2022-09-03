import json
from rubikscubetracker import RubiksImage as rbimg
from rubikscubetracker import RubiksVideo as rbvideo
import rubikscolorresolver  
from rubikscolorresolver.solver import resolve_colors as color
import sys
# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)7s: %(message)s")

# resolve_colors(sys.argv)
rba=rbimg()
# rba=rbvideo(0)
rba.analyze_file("F:/107334.jpg")
rba.analyze_webcam()
# print(dir(rb))
# print(json.dumps(rba.data, sort_keys=True))
# print(rba.data)
# print(dir(rubikscolorresolver))
arg=["",'--filename', 'F:/webcam.json']
print(color(arg))
# print(sys.argv)
