class Grid:
    def __init__(self, grd: str):
        self.original = grd
        self.read_grid(grd)
        grd = grd.split()
        self.size = (len(grd[0]), len(grd))
        self.is_square = False
        if self.size[0] == self.size[1]:
            self.is_square = True
        self.possibles = [[[] for _ in range(self.size[0])] for _ in range(self.size[1])]
        self.letters = []
        self.states = []
        for line in self.grid:
            for cell in line:
                c = cell
                if c != '*' and c not in self.letters:
                    self.letters.append(c)

    def read_grid(self, grd: str):
        grd = grd.split()
        self.grid = [[i for i in j] for j in grd]

    def __str__(self):
        res = []
        for ln in self.grid:
            line = []
            for cell in ln:
                line.append(cell)
            res.append(''.join(line))
        return '\n'.join(res)

    def check_cell(self, pos: (int, int)):
        assert 0 <= pos[0] <= self.size[0]
        assert 0 <= pos[1] <= self.size[1]
        if self.grid[pos[1]][pos[0]] != '*':
            self.possibles[pos[1]][pos[0]] = []
            return
        letters = self.letters.copy()
        for i in range(self.size[0]):
            c = self.grid[i][pos[0]]
            if c in letters:
                letters.remove(c)
        for i in range(self.size[1]):
            c = self.grid[pos[1]][i]
            if c in letters:
                letters.remove(c)
        if self.is_square:
            size = self.size[0]
            if pos[0] == pos[1]:
                for i in range(size):
                    c = self.grid[i][i]
                    if c in letters:
                        letters.remove(c)
            if pos[0] == size - pos[1] - 1:
                for i in range(size):
                    c = self.grid[i][size - i - 1]
                    if c in letters:
                        letters.remove(c)
        self.possibles[pos[1]][pos[0]] = letters

    def check_all(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.check_cell((i,j))

    def find_invariants(self):
        counter = 0
        flag = True
        while flag:
            flag = False
            for i in range(self.size[0]):
                for j in range(self.size[1]):
                    if len(self.possibles[i][j]) == 0:
                        if self.grid[i][j] == '*':
                            return -1
                    elif len(self.possibles[i][j]) == 1:
                        flag = True
                        counter += 1
                        self.update((i,j), self.possibles[i][j][0])
        return counter

    def update(self, pos: (int, int), let):
        self.grid[pos[0]][pos[1]] = let
        self.possibles[pos[0]][pos[1]] = []
        let = self.grid[pos[0]][pos[1]]
        for i in range(self.size[0]):
            if let in self.possibles[i][pos[1]]:
                self.possibles[i][pos[1]].remove(let)
        for i in range(self.size[0]):
            if let in self.possibles[pos[0]][i]:
                self.possibles[pos[0]][i].remove(let)
        if self.is_square:
            size = self.size[0]
            if pos[0] == pos[1]:
                for i in range(size):
                    if let in self.possibles[i][i]:
                        self.possibles[i][i].remove(let)
            if pos[0] == size - pos[1] - 1:
                for i in range(size):
                    if let in self.possibles[i][size - i - 1]:
                        self.possibles[i][size - i - 1].remove(let)

    def assume(self):
        m = len(self.letters)
        pos = None
        for j in range(self.size[0]):
            for i in range(self.size[1]):
                l = len(self.possibles[i][j])
                if l != 0 and l < m:
                    m = l
                    pos = (i, j)
        if pos is None:
            return -1
        c = self.possibles[pos[0]][pos[1]].pop()
        self.states.append((str(self), pos,
                            self.possibles[pos[0]][pos[1]].copy()))
        self.update(pos, c)
        return 0

    def next(self):
        if len(self.states) == 0:
            return -1
        state = self.states.pop()
        self.read_grid(state[0])
        c = state[2].pop()
        self.grid[state[1][0]][state[1][1]] = c
        self.check_all()
        if len(state[2]) != 0:
            self.states.append(state)
        return 0

    def is_solved(self):
        s = str(self)
        return '*' not in s

    def solve(self):
        self.check_all()
        while True:
            r = self.find_invariants()
            if self.is_solved():
                print(self, end='\n\n')
                if self.next() != 0:
                    return
            elif r < 0:  # имеется противоречие
                if self.next() != 0:
                    return
            else:  # не решено, но ошибок нет
                self.assume()


st = []
st.append('СЛЕЗА\n*****\n**ЛЕС\n*****\n*****')
st.append('СЛЮДА\n*****\nЛАД**\n*****\n*****')
st.append('ЗАБОР\n*****\n*БОР*\n*****\n*****')
st.append('КРУЧА\n*****\n**РАК\n*****\n*****')
st.append('СПОРТ\n*****\n*****\nРОТ**\n*****')
st.append('ПИЛОТ\n*****\n*****\n*ЛОТ*\n*****')
for s in st:
    g = Grid(s)
    g.solve()