#!/usr/bin/env python
# encoding: utf-8
from gevent import monkey
monkey.patch_all()

import json
import pprint
import random
from pickle import load, dump
from bottle import route, run, request, template, static_file


class Player(object):
    def __init__(self, char, x, y):
        self.char=char
        self.x=x
        self.y=y


def draw_players(all_players):
    size = 8
    background = [['-'] * size for i in range(size)]
    for player in all_players:
        background[player.x][player.y] = player.char
    return background


def by_position(position):
    for player in players:
        if players[player].get('matrix') == position:
            return players[player]
    return None


"""
p=[Player('M',0,1)]
pprint.pprint(draw_players(p))
pprint.pprint(draw_players([Player('H',7,6)]))
"""


db_file = 'players.db'


def load_db():
    with open(db_file, 'rb') as db:
        return load(db)


def dump_db(obj):
    with open(db_file, 'wb') as db:
        return dump(obj, db)

global players
global barriers

barriers = [
    {
        'x': 1,
        'y': 1,
        'level': 3,
    }
]


try:
    players = load_db()
except:
    players = {}


mx = 25
my = 25


def _matrix():
    global players

    if len(players) == 0:
        players = {}
    background = [['_'] * mx for i in range(my)]
    for player in players:
        if players[player].get('life'):
            background[players[player].get('matrix')[0]][players[player].get('matrix')[1]] = "{}|{}".format(players[player].get('name'), players[player].get('matrix')[2])

    for barrier in barriers:
        background[barrier['x']][barrier['y']] = '#'
    return background


global matrix
matrix = _matrix()
pprint.pprint(matrix)


def valid_extent(position):
    if position[1] < 0:
        return False
    elif position[0] < 0:
        return False
    elif position[1] > mx:
        return False
    elif position[1] > my:
        return False
    return True

	
def valid_position(position):
    for barrier in barriers:
        if barrier['x'] == position[0] and barrier['y'] == position[1]:
            return False
    if valid_extent(position):
        p = by_position(position)
        if p:
            return not p['life']
        else:
            return True            
    return False


def get_position(position, direction, jump=False):
    x = 1
    if jump:
       x = 2
    new_position = position[:]
    if direction == "u":
        new_position[0] -= x
    elif direction == "d":
        new_position[0] += x
    elif direction == "r":
        new_position[1] += x
    elif direction == "l":
        new_position[1] -= x
    elif direction == "ru":
        new_position[1] += x
        new_position[0] -= x
    elif direction == "lu":
        new_position[1] -= x
        new_position[0] -= x
    elif direction == "rd":
        new_position[1] += x	
        new_position[0] += x
    elif direction == "ld":
        new_position[1] -= x
        new_position[0] += x

    if valid_position(new_position):
        return new_position
    else:
        return position

def get_position_shot(position, direction):
    new_position = position[:]
    if direction == "u":
        new_position[0] -= 1
    elif direction == "d":
        new_position[0] += 1
    elif direction == "r":
        new_position[1] += 1
    elif direction == "l":
        new_position[1] -= 1
    elif direction == "ru":
        new_position[1] += 1
        new_position[0] -= 1
    elif direction == "lu":
        new_position[1] -= 1
        new_position[0] -= 1
    elif direction == "rd":
        new_position[1] += 1
        new_position[0] += 1
    elif direction == "ld":
        new_position[1] -= 1
        new_position[0] += 1
    return new_position


@route('/goto/<direction>/', method="POST")
def goto(direction, jump=False):
    player = players[request.remote_addr]

    # if not set point direction position
    if player.get('matrix')[2] != direction:
        return {"invalid action": True}

    new_position = get_position(player['matrix'], direction, jump)
    if new_position != player['matrix']:
        player['matrix'] = new_position
        matrix = _matrix()
        pprint.pprint(matrix)
        return {"ok": True}
    else:
        return {"invalid position": True}


@route('/jump/<direction>/', method="POST")
def jump(direction):
    return goto(direction, True)


@route('/point/<direction>/', method="POST")
def point(direction):
    player = players[request.remote_addr]
    m = player['matrix']
    player['matrix'] = [m[0], m[1], direction]

    matrix = _matrix()
    pprint.pprint(matrix)
    return {"ok": True}


def barrier_colide(shoot_position):
    for i, barrier in enumerate(barriers):
        if barrier['x'] == shoot_position[0] and barrier['y'] == shoot_position[1]:
            return i
    return None


@route('/shoot/<direction>/', method='POST')
def shoot(direction):
    player = players[request.remote_addr]

    # if not set point direction position
    if player.get('matrix')[2] != direction:
        return {"invalid action": True}

    position = player['matrix'][:]
    previous_position = position[:]
    while valid_extent(previous_position):
        shoot_position = get_position_shot(previous_position, direction)
        target_player = by_position(shoot_position)
        if target_player and target_player['life']:
            target_player['life'] = False
            barriers.append({'x': target_player['matrix'][0], 'y': target_player['matrix'][1], 'level': 3})
            return "headshot in {}!".format(target_player.get("name"))
            break
        target_barrier = barrier_colide(shoot_position)
        if target_barrier is not None:
            if barriers[target_barrier]['level'] <= 0:
                del barriers[target_barrier]
                return 'Barrier destroyed'
            else:
                barriers[target_barrier]['level'] -= 1
                return 'Barrier shot remaning %s' % (barriers[target_barrier]['level'] + 1)

        previous_position = shoot_position

    return 'Not location player'


@route('/get_players/')
def get_players():
    matrix = _matrix()
    pprint.pprint(matrix)

    return players


@route('/matrix/')
def get_matrix():
    matrix = _matrix()
    pprint.pprint(matrix)

    return json.dumps(matrix)


@route('/imalive/', method='POST')
def im_alive():
    dump_db(players)

    if request.POST.get("name") == "_":
        return "Change you name, not accept `_`"

    x = random.randrange(mx)
    y = random.randrange(my)
    players[request.remote_addr] = {
        'name': request.POST.get('name'),
        "matrix": [x, y, request.POST.get('direction', 'u')],
        "life": True}

    matrix = _matrix()
    pprint.pprint(matrix)


@route('/assets/<path:path>', name='assets')
def static(path):
    yield static_file(path, root="./public/")


@route('/')
def home():
    return template('home')


run(host='0.0.0.0', port=8080, server='gevent', debug=True, reloader=True)
