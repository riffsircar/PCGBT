import argparse, json, random



parser = argparse.ArgumentParser(description='Generate room layout.')
parser.add_argument('--no-door-ns', action='store_true', help='Disallow NS doors. (default: false)')
parser.add_argument('--no-door-ew', action='store_true', help='Disallow EW doors. (default: false)')
parser.add_argument('--no-open-ns', action='store_true', help='Disallow NS open. (default: false)')
parser.add_argument('--no-open-ew', action='store_true', help='Disallow EW open. (default: false)')
parser.add_argument('--no-loops', action='store_true', help='Disallow loops. (default: false)')
parser.add_argument('--door-pct', type=int, help='Percent chance of door when there is a choice. (default: %(default)s)', default=20)
parser.add_argument('--min-rooms', type=int, help='Minimum rooms. (default: %(default)s)', default=5)
parser.add_argument('--max-rooms', type=int, help='Maximum rooms.(default: %(default)s)', default=20)
parser.add_argument('--json', action='store_true', help='Output JSON. (default: false)')
args = parser.parse_args()




NORTH  = 'north'
SOUTH  = 'south'
EAST   = 'east'
WEST   = 'west'
DIRS   = [NORTH, SOUTH, EAST, WEST]

CLOSED = 'closed'
DOOR   = 'door'
OPEN   = 'open'

layout = {}
layout[(0, 0)] = {}
layout[(0, 0)][NORTH] = CLOSED
layout[(0, 0)][SOUTH] = CLOSED
layout[(0, 0)][EAST]  = CLOSED
layout[(0, 0)][WEST]  = CLOSED

if False:
    layout[(1, 0)] = {}
    layout[(1, 0)][NORTH] = CLOSED
    layout[(1, 0)][SOUTH] = CLOSED
    layout[(1, 0)][EAST]  = OPEN
    layout[(1, 0)][WEST]  = CLOSED

    layout[(2, 0)] = {}
    layout[(2, 0)][NORTH] = CLOSED
    layout[(2, 0)][SOUTH] = CLOSED
    layout[(2, 0)][EAST]  = CLOSED
    layout[(2, 0)][WEST]  = OPEN

    layout[(1, 1)] = {}
    layout[(1, 1)][NORTH] = CLOSED
    layout[(1, 1)][SOUTH] = DOOR
    layout[(1, 1)][EAST]  = CLOSED
    layout[(1, 1)][WEST]  = CLOSED

    layout[(1, 2)] = {}
    layout[(1, 2)][NORTH] = DOOR
    layout[(1, 2)][SOUTH] = CLOSED
    layout[(1, 2)][EAST]  = CLOSED
    layout[(1, 2)][WEST]  = CLOSED

    layout[(3, 3)] = {}
    layout[(3, 3)][NORTH] = CLOSED
    layout[(3, 3)][SOUTH] = CLOSED
    layout[(3, 3)][EAST]  = CLOSED
    layout[(3, 3)][WEST]  = CLOSED



def neighbor(cell, dr):
    if dr == NORTH:
        return (cell[0], cell[1] - 1)
    elif dr == SOUTH:
        return (cell[0], cell[1] + 1)
    elif dr == EAST:
        return (cell[0] + 1, cell[1])
    elif dr == WEST:
        return (cell[0] - 1, cell[1])
    else:
        raise RuntimeError('invalid direction')

def opposite(dr):
    if dr == NORTH:
        return SOUTH
    elif dr == SOUTH:
        return NORTH
    elif dr == EAST:
        return WEST
    elif dr == WEST:
        return EAST
    else:
        raise RuntimeError('invalid direction')

if args.no_door_ns and args.no_open_ns and args.no_door_ew and args.no_open_ew:
    raise RuntimeError('no way to connect')

rooms = random.randint(args.min_rooms, args.max_rooms)
for ii in range(rooms):
    cells = list(layout.keys())

    options = []
    for cell in cells:
        for dr in DIRS:
            if dr in [NORTH, SOUTH] and args.no_door_ns and args.no_open_ns:
                continue
            if dr in [EAST, WEST] and args.no_door_ew and args.no_open_ew:
                continue

            nbr = neighbor(cell, dr)
            if layout[cell][dr] == CLOSED:
                if nbr not in layout or not args.no_loops:
                    options.append((cell, dr))
    
    cell, dr = random.choice(options)
    nbr = neighbor(cell, dr)
    opp = opposite(dr)

    if dr in [NORTH, SOUTH] and args.no_door_ns and args.no_open_ns:
        raise RuntimeError('bad option')
    elif dr in [NORTH, SOUTH] and args.no_door_ns:
        connection = OPEN
    elif dr in [NORTH, SOUTH] and args.no_open_ns:
        connection = DOOR
    elif dr in [EAST, WEST] and args.no_door_ew and args.no_open_ew:
        raise RuntimeError('bad option')
    elif dr in [EAST, WEST] and args.no_door_ew:
        connection = OPEN
    elif dr in [EAST, WEST] and args.no_open_ew:
        connection = DOOR
    else:
        if random.randint(0, 99) < args.door_pct:
            connection = DOOR
        else:
            connection = OPEN

    layout[cell][dr] = connection

    if nbr not in layout:
        layout[nbr] = {}
        layout[nbr][NORTH] = CLOSED
        layout[nbr][SOUTH] = CLOSED
        layout[nbr][EAST] = CLOSED
        layout[nbr][WEST] = CLOSED

    layout[nbr][opp] = connection

if args.json:
    out_list = []
    for k, v in layout.items():
        out_dict = dict(v)
        out_dict['cell'] = k
        out_list.append(out_dict)
    out = json.dumps(out_list, sort_keys=True, indent=4)
    print(out)

else:
    cells = list(layout.keys())
    x_lo = min(cells)[0]
    x_hi = max(cells)[0]
    y_lo = min(cells, key=lambda x: x[1])[1]
    y_hi = max(cells, key=lambda x: x[1])[1]


    for y in range(y_lo, y_hi + 1):
        line = ''
        for x in range(x_lo, x_hi + 1):
            cell = (x, y)
            if cell not in layout:
                line += '   '
            else:
                line += '┌'
                if (layout[cell][NORTH] == CLOSED):
                    line += '─'
                elif (layout[cell][NORTH] == DOOR):
                    line += '.'
                else:
                    line += ' '
                line += '┐'
        print(line)

        line = ''
        for x in range(x_lo, x_hi + 1):
            cell = (x, y)
            if cell not in layout:
                line += '   '
            else:
                if (layout[cell][WEST] == CLOSED):
                    line += '│'
                elif (layout[cell][WEST] == DOOR):
                    line += '.'
                else:
                    line += ' '
                line += ' '
                if (layout[cell][EAST] == CLOSED):
                    line += '│'
                elif (layout[cell][EAST] == DOOR):
                    line += '.'
                else:
                    line += ' '
        print(line)

        line = ''
        for x in range(x_lo, x_hi + 1):
            cell = (x, y)
            if cell not in layout:
                line += '   '
            else:
                line += '└'
                if (layout[cell][SOUTH] == CLOSED):
                    line += '─'
                elif (layout[cell][SOUTH] == DOOR):
                    line += '.'
                else:
                    line += ' '
                line += '┘'
        print(line)
