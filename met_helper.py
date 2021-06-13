from py_trees import *
from met_library import *
import random
from PIL import Image

images = {
    "#":Image.open('tiles/Met_X.png'),  # solid
    "(":Image.open('tiles/0.png'),  # beam around door (ignore using background)
    ")":Image.open('tiles/0.png'),  # beam around door (ignore using background)
    "+":Image.open('tiles/Met_+.png'),  # powerup
    "-":Image.open('tiles/0.png'),   # background
    "B":Image.open('tiles/Met_B.png'),  # breakable
    "D":Image.open('tiles/Met_D.png'),  # door
    "E":Image.open('tiles/Met_E.png'),  # enemy
    "P":Image.open('tiles/0.png'),   # path
    "[":Image.open('tiles/Met_[.png'),  # ??
    "]":Image.open('tiles/Met_].png'),  # ??
    "^":Image.open('tiles/Met_^2.png'),  # lava
    "v":Image.open('tiles/0.png')  # ??
}