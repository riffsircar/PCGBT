from PIL import Image
import os, sys

path = os.path.abspath(os.path.dirname(__file__)) + '/'

smb_images = {
    # TODO: Get T, D, M tiles from Icarus
    "E": Image.open(path + 'tiles/E.png'),
    "H": Image.open(path + 'tiles/H.png'),
    "G": Image.open(path + 'tiles/G.png'),
    "M": Image.open(path + 'tiles/M.png'),
    "o": Image.open(path + 'tiles/o.png'),
    "S": Image.open(path + 'tiles/S.png'),
    "T": Image.open(path + 'tiles/T.png'),
    "?": Image.open(path + 'tiles/Q.png'),
    "Q": Image.open(path + 'tiles/Q.png'),
    "X": Image.open(path + 'tiles/X1.png'),
    "#": Image.open(path + 'tiles/X.png'),
    "-": Image.open(path + 'tiles/-.png'),
    "0": Image.open(path + 'tiles/0.png'),
    "D": Image.open(path + 'tiles/D.png'),
    "<": Image.open(path + 'tiles/PTL.png'),
    ">": Image.open(path + 'tiles/PTR.png'),
    "[": Image.open(path + 'tiles/[.png'),
    "]": Image.open(path + 'tiles/].png'),
    "*": Image.open(path + 'tiles/-.png'),
    "P": Image.open(path + 'tiles/P.png'),
	"B": Image.open(path + 'tiles/B.png'),
	"b": Image.open(path + 'tiles/bb.png')
}

mm_images = {
	"#":Image.open(path + 'tiles/MM_X2.png'),
	"*":Image.open(path + 'tiles/MM_star.png'),
	"+":Image.open(path + 'tiles/MM_+.png'),
	"-":Image.open(path + 'tiles/-.png'),
	"B":Image.open(path + 'tiles/MM_B2.png'),
	"C":Image.open(path + 'tiles/CMM.png'),
	"D":Image.open(path + 'tiles/DMM.png'),
	"H":Image.open(path + 'tiles/HMM.png'),
	"L":Image.open(path + 'tiles/MM_L.png'),
	"M":Image.open(path + 'tiles/MMM.png'),
	"P":Image.open(path + 'tiles/-.png'),
	"U":Image.open(path + 'tiles/MM_U.png'),
	"W":Image.open(path + 'tiles/MM_w.png'),
	"l":Image.open(path + 'tiles/MM_L.png'),
	"t":Image.open(path + 'tiles/TMM.png'),
	"w":Image.open(path + 'tiles/MM_w.png'),
	"|":Image.open(path + 'tiles/LMM.png')
}

zelda_images = {
   "B":Image.open(path + 'tiles/Z_B.png'), # block
   "D":Image.open(path + 'tiles/DMM.png'), # door
   "F":Image.open(path + 'tiles/Z_F.png'), # floor
   "I":Image.open(path + 'tiles/Z_I.png'), # elemental block
   "M":Image.open(path + 'tiles/Z_M.png'), # statue/monster
   "O":Image.open(path + 'tiles/Z_O.png'), # elemental floor
   "P":Image.open(path + 'tiles/Z_P.png'), # pond/lava
   "S":Image.open(path + 'tiles/Z_S.png'), # stairs
   "W":Image.open(path + 'tiles/Z_W.png')  # wall
}

met_images = {
    "#":Image.open(path + 'tiles/Met_X.png'),  # solid
    "(":Image.open(path + 'tiles/0.png'),  # beam around door (ignore using background)
    ")":Image.open(path + 'tiles/0.png'),  # beam around door (ignore using background)
    "+":Image.open(path + 'tiles/Met_+.png'),  # powerup
    "-":Image.open(path + 'tiles/0.png'),   # background
    "B":Image.open(path + 'tiles/Met_B.png'),  # breakable
    "D":Image.open(path + 'tiles/Met_D.png'),  # door
    "E":Image.open(path + 'tiles/Met_E.png'),  # enemy
    "P":Image.open(path + 'tiles/0.png'),   # path
    "[":Image.open(path + 'tiles/Met_[.png'),  # ??
    "]":Image.open(path + 'tiles/Met_].png'),  # ??
    "^":Image.open(path + 'tiles/Met_^2.png'),  # lava
    "v":Image.open(path + 'tiles/0.png')  # ??
}