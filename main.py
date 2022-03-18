
import Mario.smb as smb
import MegaMan.mm as mm
import Dungeon.dungeon as dungeon
import blend, generic
import argparse

parser = argparse.ArgumentParser(description='PCGBT')
parser.add_argument('--game', type=str, choices=['smb','mm','met','zelda','blend','generic'], default='smb', help='game (default: smb)')
parser.add_argument('--pp', type=float, default=0.5, help='paths and pipes probability (default: 0.5)')
parser.add_argument('--gv', type=float, default=0.5, help='gaps and valleys probability (default: 0.5)')
parser.add_argument('--num', type=int, default=10, help='num rooms in Zelda/Met (default: 10)')
parser.add_argument('--hp', type=float, default=0.5, help='horizontal probability (default: 0.5)')
parser.add_argument('--up', type=float, default=0.5, help='vertical probability (default: 0.5)')
parser.add_argument('--name', type=str, default='', help='output file name')
parser.add_argument('--gen', type=str, choices=['met','mm'], default='met', help='game for generic BT (default: met)')
args = parser.parse_args()
path_pipe_prob, gaps_valleys_prob, num_rooms, horizontal_prob, up_prob = args.pp, args.gv, args.num, args.hp, args.up

game = args.game
if args.name == '':
    args.name = game + '_level'
if game == 'smb':
    smb.generate(path_pipe_prob, gaps_valleys_prob, args.name)
elif game == 'mm':
    mm.generate(horizontal_prob, up_prob, args.name)
elif game == 'met':
    dungeon.generate('met', num_rooms, args.name)
elif game == 'zelda':
    dungeon.generate('zelda', num_rooms, args.name)
elif game == 'blend':
    blend.generate(horizontal_prob, up_prob, args.name)
elif game == 'generic':
    generic.generate(horizontal_prob, up_prob, args.gen, args.name)