known = [
    (4,  3, 1), (8,  4, 0), (12, 4, 6), (16, 0, 2),
    (20, 6, 0), (24, 5, 7), (28, 7, 5), (32, 1, 7),
    (36, 2, 0), (40, 4, 2), (44, 3, 5), (48, 1, 5),
    (52, 0, 0), (56, 7, 3), (60, 3, 7), (64, 6, 2)
]
moves = [
    (-2,  1), (-1,  2),  # .7.0.
    ( 1,  2), ( 2,  1),  # 6...1
    ( 2, -1), ( 1, -2),  # ..X..
    (-1, -2), (-2, -1)   # 5...2
]                        # .4.3.

board = [[0] * 8 for _ in range(8)]
for p in known:
    board[p[1]][p[2]] = p[0]


def print_board():
    for l in board:
        for s in l:
            if s == 0:
                print(' ** ', end='')
            else:
                print('{:^4}'.format(s), end='')
        print()
    print()


def get_move(c_pos: (int, int), num: int) -> (int, int) or None:
    if num > 7:
        return None
    x = c_pos[0] + moves[num][0]
    y = c_pos[1] + moves[num][1]
    if (0 <= x < 8) and (0 <= y < 8):
        return x, y
    return None


def search_paths(start: (int, int, int), end: (int, int), max_depth: int):
    assert max_depth < 10
    current = []
    path = [(start[0], start[1])]
    founded = []
    current.append([start[2], -1])
    while True:  # поиск в глубину
        c = current[-1]
        if len(current) <= max_depth:
            num = c[1]
            turn = None
            while num < 8 and turn is None:
                num += 1
                turn = get_move(path[-1], num)
                if turn is not None:
                    b_val = board[turn[0]][turn[1]]
                    if (b_val != 0) and (b_val != c[0]+1) or (turn in path):
                        turn = None
            if num == 8:
                current.pop()
                path.pop()
                if len(current) == 0:
                    break
            else:
                current[-1][1] = num
                path.append(turn)
                current.append([c[0]+1, -1])
        else:
            if path[-1] == end:
                founded.append(path.copy())
            current.pop()
            path.pop()
        pass
    return founded

# TODO:функция обработки списка путей.
# TODO:цикл первого прохода. (поиск путей между известными точками)
# TODO:цикл поиска противоречий.


print_board()
pos = (9, -1, 0)
pf = search_paths(pos, known[0][1:], 4)
for i in range(3):
    board[pf[0][i+1][0]][pf[0][i+1][1]] = i+1
print_board()
pos = (3, 1, 4)
pf = search_paths(pos, known[1][1:], 4)
print(len(pf))
print(pf)
