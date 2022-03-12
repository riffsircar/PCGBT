
import Mario.smb as smb
import MegaMan.mm as mm
import Dungeon.dungeon as dungeon
import blend
import generic
import argparse

parser = argparse.ArgumentParser(description='PCGBT')
parser.add_argument('--game', type=str, choices=['smb','mm','met','zelda','blend','generic'], default='smb', help='game (default: smb)')
parser.add_argument('--pp', type=float, default=0.5, help='paths and pipes probability (default: 0.5)')
parser.add_argument('--gv', type=float, default=0.5, help='gaps and valleys probability (default: 0.5)')
parser.add_argument('--num', type=int, default=10, help='num rooms in Zelda/Met (default: 10)')
parser.add_argument('--hp', type=float, default=0.5, help='horizontal probability (default: 0.5)')
parser.add_argument('--up', type=float, default=0.5, help='vertical probability (default: 0.5)')
args = parser.parse_args()

game = args.game
if game == 'smb':
    smb.generate()
elif game == 'mm':
    mm.generate()
elif game == 'met':
    dungeon.generate('met')
elif game == 'zelda':
    dungeon.generate('zelda')
elif game == 'blend':
    blend.generate()
elif game == 'generic':
    generic.generate()