from collections import namedtuple

ALIVE = '*'
EMPTY = '_'

Query = namedtuple('Query', ('y', 'x'))  # light x-y class
Transition = namedtuple('Transition', ('y', 'x', 'state'))  # light x-y-state class


def count_neighbors(y, x):
    """a life search friends / corutine Implementation
    :return around friends total nums
    """
    n_ = yield Query(y + 1, x + 0)  # north
    ne = yield Query(y + 1, x + 1)  # norse east
    e_ = yield Query(y + 0, x + 1)  # east
    se = yield Query(y - 1, x + 1)  # south east

    s_ = yield Query(y - 1, x + 0)  # south
    sw = yield Query(y - 1, x - 1)  # norse
    w_ = yield Query(y + 0, x - 1)  # norse
    nw = yield Query(y + 1, x - 1)  # norse

    neighbors_states = [n_, ne, e_, se, s_, sw, w_, nw]

    count = 0

    for i, state in enumerate(neighbors_states):
        if state == ALIVE:
            count += 1
    return count


def step_cell(y, x):
    """apply the game logic to a_life"""
    state = yield Query(y, x)
    neighbors = yield from count_neighbors(y, x)  # Synthesis corutine
    next_state = game_logic(state, neighbors)
    yield Transition(y, x, next_state)


def game_logic(state, neighbors):
    """a life's rule / judge dead or alive or reverse """
    if state == ALIVE:
        if neighbors < 2:
            return EMPTY  # death / too few
        elif neighbors > 3:
            return EMPTY  # death / too many

    else:
        if neighbors == 3:
            return ALIVE  # revrse

    return state


TICK = object()


def simulate(height, width):
    """ simulation all life's dead or alive
     hou to use: next(simulate) # do one step forward (this simulation)"""
    while True:
        # all field lifes do next state
        for y in range(height):
            for x in range(width):
                yield from step_cell(y, x)  # return Transition
        yield TICK


class Grid(object):
    """life's living field"""

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.rows = []  # all field / alive or empty

        for _ in range(self.height):
            self.rows.append([EMPTY] * self.width)

    def __str__(self):
        out = ""
        for r in self.rows:
            out += " ".join(r)
            out += "\n"

        return out

    def query(self, y, x):
        return self.rows[y % self.height][x % self.width]

    def assign(self, y, x, state):
        self.rows[y % self.height][x % self.width] = state


def live_a_generation(grid, sim):
    """
    lifegame's world / call this , do one flame foward this world
    :param grid: current field of game
    :param sim:
    :return:
    """
    progeny = Grid(grid.height, grid.width)  # nex grid / no affects current grid
    item = next(sim)

    while item is not TICK:
        if isinstance(item, Query):
            state = grid.query(item.y, item.x)
            item = sim.send(state)
        else:  # Transition
            progeny.assign(item.y, item.x, item.state)
            item = next(sim)

    return progeny


class ColumnPrinter(object):
    def __init__(self):
        self.column = []

    def append(self, grid):
        self.column.append(str(grid))

    def __str__(self):
        out = ""

        column_len = len(self.column)

        col_str = self.column[0]
        print_height = col_str.count('\n')

        header = ""

        for i in range(column_len):
            header += "{0:^17}".format(i) + "|"

        out += header
        out_l = ["" for i in range(print_height)]

        for col in self.column:
            str_l = col.split('\n')
            for i, str_single in enumerate(str_l[:-1]):
                out_l[i] += str_single + "|"

        for l in out_l:
            out += "\n" + l

        return out


# start pos settings
grid = Grid(5, 9)
# lifegame / glider pattern
grid.assign(0, 3, ALIVE)
grid.assign(1, 4, ALIVE)
grid.assign(2, 2, ALIVE)
grid.assign(2, 3, ALIVE)
grid.assign(2, 4, ALIVE)

# do lifegame and print field
columns = ColumnPrinter()
sim = simulate(grid.height, grid.width)
for i in range(5):
    columns.append(grid)
    grid = live_a_generation(grid, sim)

print(columns)

# # step_cell test
# it = step_cell(10,5)
# q0 = next(it)
# print('Me:        ',q0)
#
# q1 = it.send(ALIVE)
# print('Q1:        ',q1)
#
# q2 = it.send(ALIVE)
# print('Q2:        ',q2)
#
# q3 = it.send(ALIVE)
# print('Q3:        ',q3)
#
# q4 = it.send(ALIVE)
# print('Q4:        ',q4)
#
# q5 = it.send(ALIVE)
# print('Q5:        ',q5)
#
# q6 = it.send(ALIVE)
# print('Q6:        ',q6)
#
# q7 = it.send(ALIVE)
# print('Q7:        ',q7)
#
# q7 = it.send(ALIVE)
# print('Q7:        ',q7)
#
#
# t1 = it.send(ALIVE)
# print('Outcome:',t1)

# #count_neighbors test
# it = conunt_neighbors(10,5)
# q1 = next(it)
# print('First yield:',q1)
#
# q2 = it.send(ALIVE)
# print('First yield:',q2)
#
# q3 = it.send(ALIVE)
# print('First yield:',q3)
#
# q4 = it.send(ALIVE)
# print('First yield:',q4)
#
# q5 = it.send(ALIVE)
# print('First yield:',q5)
#
# q6 = it.send(ALIVE)
# print('First yield:',q6)
#
# q7 = it.send(ALIVE)
# print('First yield:',q7)
#
# q8 = it.send(ALIVE)
# print('First yield:',q8)
#
# try:
#     q9 = it.send(ALIVE)
# except StopIteration as e:
#     print('COUNT: ',e.value)
