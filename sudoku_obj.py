class Sudoku:
    NUM_OF_POSS = 9**3  # number of all possible values

    def __init__(self, user_input):
        self.array = []
        self.fillers = []

        for _ in range(9):
            line_filler = []
            self.array.append([" "] * 9)
            for _ in range(9):
                line_filler.append(set(map(lambda x: x + 1, range(9))))
            self.fillers.append(line_filler)
        self.numeration_help()
        self.import_values(*user_input)

    def __repr__(self):
        self.printer = ""
        for line in self.array:
            self.printer += str(line) + "\n"
        return self.printer

    def __str__(self):
        return self.__repr__()

    def show(self):
        print("_" * 25)
        for i, line in enumerate(self.array):
            print("| ", end="")
            for j, num in enumerate(line):
                if (j + 1) % 3 == 0:
                    sep = " | "
                else:
                    sep = " "
                print(str(num) + sep, end="")
            if (i + 1) % 3 == 0:
                print("\n" + "-" * 25, end="")
            print()

    @staticmethod
    def numeration_help():
        print("Object created!")
        print("Array of initial possible values created")
        print("Values addition log: ")
        print("\tCoordinates and values inserted as an integer xyz containing x - row, y - column, z - value")

    def add_value(self, val: tuple):
        print(f"\tInput value: col {val[0] + 1}, row {val[1] + 1}, num {val[2]}")
        self.array[val[0]][val[1]] = val[2]

    def import_values(self, *args):
        for arg in args:
            next_val = str(arg)
            next_val = tuple([int(next_val[0]) - 1, int(next_val[1]) - 1, int(next_val[2])])
            self.add_value(next_val)
        self.show()

    def easy_fillers(self, show=False):
        print("1. Set the possible vals for every field")
        counter = 0
        for i, line in enumerate(self.array):
            for j, field in enumerate(line):
                if field != " ":
                    self.fillers[i][j].intersection_update({field})
                    counter += 8
                if show:
                    print(field, self.fillers[i][j])
        if not show:
            print("(...)")
        print("Removed {} possible values of {}. One for each field filled with a number".format(counter, 9**3))

    def find_the_cross(self, field_num, showlog=False):
        tb = []  # top-bottom
        lr = []  # left-right
        cross = set()

        if showlog:
            print("Find the cross for field: ({}, {})".format(field_num[0]+1, field_num[1]+1))
            print("Value: <", self.array[field_num[0]][field_num[1]], ">", sep="")
            print("Possible values: ", self.fillers[field_num[0]][field_num[1]])

        for i in range(9):
            tb.append(self.array[i][field_num[1]])
            lr.append(self.array[field_num[0]][i])

        if showlog:
            print("top-bottom", tb)
            print("left-right", lr)

        cross = {*tb, *lr}.difference({" ", self.array[field_num[0]][field_num[1]]})
        if showlog:
            print("cross: ", cross)

        return cross

    def find_the_box(self):
        # like finding the cross but for the box 3x3
        pass

    def cross_fillers(self):
        pass

    def box_fillers(self):
        pass

    def solve(self, showlog=False):
        self.easy_fillers()
        self.find_the_cross((5, 6), showlog)
        pass


mysud = Sudoku([111, 122, 139, 196,
                255,
                324, 388, 392,
                419, 428, 437, 453, 481,
                516, 542, 577, 593,
                621, 678,
                766, 771, 784,
                814, 882,
                923, 941, 957])

mysud.solve(showlog=True)
