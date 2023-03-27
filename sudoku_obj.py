import re


class Sudoku:
    def __init__(self):
        self.array = []
        self.fillers = []

        for _ in range(9):
            line_filler = []
            self.array.append([" "] * 9)
            for _ in range(9):
                line_filler.append(set(map(lambda x: x+1, range(9))))
            self.fillers.append(line_filler)
        self.numeration_help()

    def __repr__(self):
        return str(self.array)

    def __str__(self):
        self.printer = ""
        for line in self.array:
            self.printer += str(line) + "\n"
        return self.printer

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
        print("Now add some values to it: ")
        print("Coordinates and values inserted as an integer xyz containing x - row, y - column, z - value")

    def add_value(self, val: tuple):
        print(f"Input value: col {val[0]+1}, row {val[1]+1}, num {val[2]}")
        self.array[val[0]][val[1]] = val[2]

    def import_values(self, *args: int):
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
                    counter += 1
                if show:
                    print(field, self.fillers[i][j])
        if not show:
            print("(...)")
        print("Removed {} possible values. One for each field filled with a number".format(counter))

    def find_the_cross(self, field_num):
        pass


mysud = Sudoku()
mysud.import_values(111, 122, 139, 196,
                    255,
                    324, 388, 392,
                    419, 428, 437, 453, 481,
                    516, 542, 577, 593,
                    621, 678,
                    766, 771, 784,
                    814, 882,
                    923, 941, 957)

mysud.easy_fillers(True)  # show=True to show the log
print(repr(mysud))
