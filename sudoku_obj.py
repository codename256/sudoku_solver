class Sudoku:
    NUM_OF_POSS = 9 ** 3  # number of all possible values

    def __init__(self, user_input, showlog=False):
        print("<" * 20, "SUDOKU INITIALIZATION", ">" * 20)
        self.array = []
        self.fillers = []

        for _ in range(9):
            line_filler = []
            self.array.append([" "] * 9)
            for _ in range(9):
                line_filler.append(set(map(lambda x: x + 1, range(9))))
            self.fillers.append(line_filler)
        self.numeration_help(showlog)
        self.import_values(*user_input)

    def __repr__(self):
        return str(self.array)

    def __str__(self):
        self.printer = ""
        for line in self.array:
            self.printer += str(line) + "\n"
        return self.printer

    def show(self):
        print("\nCurrent state of the sudoku")
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

    def show_vals_fillers(self):
        for i in range(9):
            for j in range(9):
                print("Val: ", self.array[i][j], "Filler: ", self.fillers[i][j])

    @staticmethod
    def numeration_help(showlog=False):
        if showlog:
            print("\nObject created!")
            print("Array of initial possible values created")
            print("Values addition log: ")
            print("\tCoordinates and values inserted as an integer xyz containing x - row, y - column, z - value")
            print("\tValues of columns and rows are 0-8 code-wise, but are shown as 1-9 for more intuitive approach")

    def add_value(self, val: tuple):
        print(f"\tInput value: row {val[0] + 1}, col {val[1] + 1}, num {val[2]}")
        self.array[val[0]][val[1]] = val[2]

    def import_values(self, *args):
        for arg in args:
            next_val = str(arg)
            next_val = tuple([int(next_val[0]) - 1, int(next_val[1]) - 1, int(next_val[2])])
            self.add_value(next_val)
        self.show()

    def set_value(self, val):
        print("Value for this field is determined to be:", val[2])
        self.add_value(val)

    def init_fillers(self, showlog=False):
        print("\n1. If value known, leave ONLY array->line->field->value in its fillers set(). Repeat for all fields")
        for i, line in enumerate(self.array):
            for j, field in enumerate(line):
                if field != " ":
                    self.fillers[i][j].intersection_update({field})
                    pass

    def find_the_cross(self, field_num, showlog=False):
        tb = []  # top-bottom
        lr = []  # left-right

        for i in range(9):
            tb.append(self.array[i][field_num[1]])
            lr.append(self.array[field_num[0]][i])
        cross = {*tb, *lr}.difference({" ", self.array[field_num[0]][field_num[1]]})

        if showlog:
            print("Cross for: ({}, {}) | ".format(field_num[0] + 1, field_num[1] + 1), end="")
            print("\tVal: <", self.array[field_num[0]][field_num[1]], "> | ", sep="", end="")
            print("\tCurrently possible:", str(self.fillers[field_num[0]][field_num[1]]).ljust(27), end=" | ")
            print("\tcross:", cross)
        return cross

    def find_the_box(self, field_num, showlog=False):
        box_ids = dict()
        box = set()
        for i in range(3):
            box_ids[i] = 0
            box_ids[i + 3] = 1
            box_ids[i + 6] = 2
        box_id = (box_ids[field_num[0]], box_ids[field_num[1]])

        for i in range(3):
            for j in range(3):
                box.update({self.array[i + 3 * box_id[0]][j + 3 * box_id[1]]})
                if showlog:
                    print(f"'{self.array[i + 3 * box_id[0]][j + 3 * box_id[1]]}'", end="")
            box.difference_update({" ", self.array[field_num[0]][field_num[1]]})

        if showlog:
            print(f"\nFor field ({field_num[0] + 1}, {field_num[1] + 1}), val: {self.array[field_num[0]][field_num[1]]} | "
                  f"on screen ({field_num[0] % 3 + 1}, {field_num[1] % 3 + 1}), the box fillers set is: ", box)
        return box

    def cross_fillers(self, showlog=False):
        print("2. Remove from field filler values that are written in top-bot left-right fields (cross)")
        print("If only one filler element and the array value is ' ', then it'll be updated with the filler")

        for i, line in enumerate(self.array):
            for j, val in enumerate(line):
                cross = self.find_the_cross((i, j), showlog=showlog)
                self.fillers[i][j].difference_update(cross)

                if showlog:
                    print(" " * 40 + "Updated filler:    ", self.fillers[i][j])
                if len(self.fillers[i][j]) == 1 and self.array[i][j] == " ":
                    if showlog:
                        print("Updated value from '{}' to {}".format(self.array[i][j], *self.fillers[i][j]))
                    try:
                        self.set_value((i, j, int(*self.fillers[i][j])))
                    except TypeError:
                        print("Probably too much fillers to set as int")

    def box_fillers(self, showlog=False):
        for i in range(9):
            for j in range(9):
                box = self.find_the_box((i, j), showlog=showlog)
                self.fillers[i][j].difference_update(box)
                if showlog:
                    print("\tUpdate filler:    ", self.fillers[i][j])
                if len(self.fillers[i][j]) == 1 and self.array[i][j] == " ":
                    if showlog:
                        print("Update value from '{}' to {}".format(self.array[i][j], *self.fillers[i][j]))
                    try:
                        self.set_value((i, j, int(*self.fillers[i][j])))
                    except TypeError:
                        if showlog:
                            print("Probably too much fillers to set as int")

    def one_in_all_fillers(self, showlog=False):
        print("<<< ONE IN A ROW >>>")
        for i in range(9):
            for j in range(9):
                self.one_in_a_row((i, j), showlog)

        print("<<< ONE IN A COL >>>")
        for i in range(9):
            for j in range(9):
                self.one_in_a_col((i, j), showlog)

        print("<<< ONE IN A BOX >>>")
        for i in range(9):
            for j in range(9):
                self.one_in_a_box((i, j), showlog)

    def one_in_a_row(self, field_num, showlog=False):
        # Value possible only for one field -> write it
        # Use update instead of '=' to have different set id's
        temp = set()
        temp.update(self.fillers[field_num[0]][field_num[1]])
        fillers_line = set()

        # consider: .update(*self.fillers[field_num[0]][:9]) with removing the element set
        for i in range(9):
            if i is not field_num[1]:
                fillers_line.update(self.fillers[field_num[0]][i])
        temp.difference_update(fillers_line)

        if len(temp) == 1 and self.array[field_num[0]][field_num[1]] is not int(*temp):
            self.set_value((field_num[0], field_num[1], int(*temp)))

    def one_in_a_col(self, field_num, showlog=False):
        # Value possible only for one field -> write it
        # Use update instead of '=' to have different set id's
        temp = set()
        temp.update(self.fillers[field_num[0]][field_num[1]])
        fillers_line = set()

        # consider: .update(*self.fillers[field_num[0]][:9]) with removing the element set
        for i in range(9):
            if i is not field_num[1]:
                fillers_line.update(self.fillers[i][field_num[1]])
        temp.difference_update(fillers_line)

        if len(temp) == 1 and self.array[field_num[0]][field_num[1]] is not int(*temp):
            self.set_value((field_num[0], field_num[1], int(*temp)))

    def one_in_a_box(self, field_num, showlog=False):
        # Value possible only for one field in a box -> write it
        # Use update instead of '=' to have different set id's
        temp, fillers_box, box = set(), set(), set()
        box_ids = dict()
        for i in range(3):
            box_ids[i] = 0
            box_ids[i + 3] = 1
            box_ids[i + 6] = 2

        temp.update(self.fillers[field_num[0]][field_num[1]])

        box_id = (box_ids[field_num[0]], box_ids[field_num[1]])
        for i in range(3):
            for j in range(3):
                if [i, j] != [field_num[0], field_num[1]]:
                    fillers_box.update(self.fillers[i + 3 * box_id[0]][j + 3 * box_id[1]])

        if len(temp) == 1 and self.array[field_num[0]][field_num[1]] != int(*temp):
            self.set_value((field_num[0], field_num[1], int(*temp)))

    def is_done(self):
        for line in self.array:
            for elem in line:
                if elem == ' ':
                    return False
                else:
                    continue
        else:
            return True

    def solve(self, showlog=False):
        i = 0

        while True:
            print("<"*20, "INIT FILLERS", ">"*20)
            self.init_fillers(showlog)
            self.show()
            print("<"*20, "CROSS FILLERS", ">"*20)
            self.cross_fillers(showlog)
            self.show()
            print("<"*20, "BOX FILLERS", ">"*20)
            self.box_fillers(showlog)
            self.show()
            print("<"*20, "ONE IN ALL FILLERS", ">"*20)
            self.one_in_all_fillers(showlog)
            self.show()
            print("<<<<< {} >>>>>".format(i))
            if self.is_done():
                print("Finished after {} loops".format(i))
                break
            i += 1
            if i > 15:
                break


# mysud = Sudoku([111, 122, 139, 196,
#                 255,
#                 324, 388, 392,
#                 419, 428, 437, 453, 481,
#                 516, 542, 577, 593,
#                 621, 678,
#                 766, 771, 784,
#                 814, 882,
#                 923, 941, 957])

# other = Sudoku([126, 134, 152,
#                 255, 282,
#                 323, 348, 361, 394,
#                 418, 465, 481, 493,
#                 576, 599,
#                 622, 663, 685, 698,
#                 716, 771,
#                 835, 888,
#                 953, 966, 989])
#
# hard_level = Sudoku([118, 126, 163,
#                      245, 269, 271, 292,
#                      354,
#                      412, 436, 473, 495,
#                      577,
#                      624, 691,
#                      714, 723, 732, 797,
#                      821, 846, 868,
#                      962])

test_one_in_a_box = Sudoku([243, 373,
                    423, 733])
# ,
#                446, 465, 472
# mysud.solve(showlog=False)
# other.solve()
# hard_level.solve()
test_one_in_a_box.solve(showlog=False)

# td:
# make the showlog work correctly and make it less ugly
# add some way to stop the iteration when it's stuck, or it finished (with returns from functions if they did sth)
