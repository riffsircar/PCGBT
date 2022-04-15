
import Mario.smb as smb
import MegaMan.mm as mm
import Dungeon.dungeon as dungeon
import blend, generic
import argparse

parser = argparse.ArgumentParser(description='PCGBT')
parser.add_argument('--game', type=str, choices=['smb','mm','met','zelda','blend','generic'], default='smb', help='game (default: smb)')

parser.add_argument('--loop', action='store_true', default=False, help='use looping or non-looping BT for MM')

parser.add_argument('--pp', type=float, default=0.5, help='paths and pipes probability (default: 0.5)')
parser.add_argument('--gv', type=float, default=0.5, help='gaps and valleys probability (default: 0.5)')

parser.add_argument('--hp', type=float, default=0.5, help='horizontal probability (default: 0.5)')
parser.add_argument('--vp', type=float, default=0.5, help='vertical probability (default: 0.5)')

parser.add_argument('--num', type=int, default=10, help='num rooms in Zelda/Met or segments in MM (default: 10)')

parser.add_argument('--gen', type=str, choices=['met','mm'], default='met', help='game for generic BT (default: met)')
parser.add_argument('--hsize', type=int, default=3, help='size of horizontal sections in generic')

parser.add_argument('--mmsize', type=int, default=3, help='size of horizontal MM section in blend')
parser.add_argument('--metsize', type=int, default=3, help='size of horizontal Metroid section in blend')

parser.add_argument('--name', type=str, default='', help='output file name')

args = parser.parse_args()
path_pipe_prob, gaps_valleys_prob, num_rooms, horizontal_prob, up_prob = args.pp, args.gv, args.num, args.hp, args.vp

game = args.game
if args.name == '':
    args.name = game + '_level'
if game == 'smb':
    smb.generate(path_pipe_prob, gaps_valleys_prob, args.name)
elif game == 'mm':
    if args.loop:
        mm.generate_loop(args.num, args.name)
    else:
        mm.generate(horizontal_prob, up_prob, args.name)
elif game == 'met':
    dungeon.generate('met', num_rooms, args.name)
elif game == 'zelda':
    dungeon.generate('zelda', num_rooms, args.name)
elif game == 'blend':
    blend.generate(horizontal_prob, up_prob, args.mmsize, args.metsize, args.name)
elif game == 'generic':
    generic.generate(args.gen, horizontal_prob, up_prob, args.hsize, args.name)