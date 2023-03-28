class Sudoku:
    NUM_OF_POSS = 9 ** 3  # number of all possible values

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
    def numeration_help():
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
        print("\n1. Set the possible vals for every field")
        counter = 0
        for i, line in enumerate(self.array):
            for j, field in enumerate(line):
                if field != " ":
                    self.fillers[i][j].intersection_update({field})
                    counter += 8
                if showlog:
                    print(field, self.fillers[i][j])
        if not showlog:
            print("(...)")
        print("Removed {} possible values of {}. One for each field filled with a number".format(counter, 9 ** 3))

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

            # Uncomment if you want a really detailed log
            # if showlog:
            #     print("top-bottom", tb, end=" | ")
            #     print("left-right", lr, end=" | ")

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
            print()
            for j in range(3):
                box.update({self.array[i + 3 * box_id[0]][j + 3 * box_id[1]]})
                if showlog:
                    print(f"'{self.array[i + 3 * box_id[0]][j + 3 * box_id[1]]}'", end="")
            box.difference_update({" ", self.array[field_num[0]][field_num[1]]})

        print(f"\nFor field ({field_num[0] + 1}, {field_num[1] + 1}), val: {self.array[field_num[0]][field_num[1]]} | "
              f"on screen ({field_num[0] % 3 + 1}, {field_num[1] % 3 + 1}), the box fillers set is: ", box)
        return box

    def cross_fillers(self, showlog=False):
        print("\n2. Remove the cross top-bot left-right values from the fillers")
        print("If there is only one filler left and the value is ' ', then it'll be updated with the filler")
        print("Cross fillers search:")
        print("Update fillers by removing the cross values from possible decisions in fillers")

        for i, line in enumerate(self.array):
            for j, val in enumerate(line):
                cross = self.find_the_cross((i, j), showlog=showlog)
                self.fillers[i][j].difference_update(cross)

                print(" " * 40 + "Updated filler:    ", self.fillers[i][j])
                if len(self.fillers[i][j]) == 1 and self.array[i][j] == " ":
                    print("Updated value from '{}' to {}".format(self.array[i][j], *self.fillers[i][j]))
                    try:
                        print("")
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
                        if showlog:
                            print("")
                        self.set_value((i, j, int(*self.fillers[i][j])))
                    except TypeError:
                        if showlog:
                            print("Probably too much fillers to set as int")

    def one_in_all_fillers(self, showlog=False):
        for i in range(9):
            for j in range(9):
                self.one_in_a_row((i, j), showlog)
                self.one_in_a_col((i, j), showlog)
                self.one_in_a_box((i, j), showlog)

    def one_in_a_row(self, field_num, showlog=False):
        # if some value is present as possible for only one field, then input it there
        # make a temp, because we'll pop the elements. Use update instead of '=' to have different id's

        temp = set()
        temp.update(self.fillers[field_num[0]][field_num[1]])
        fillers_line = set()
        for i in range(9):
            if i == field_num[1]:
                continue
            else:
                fillers_line.update(self.fillers[field_num[0]][i])

        if showlog:
            print("\nField: {} {}".format(field_num[0] + 1, field_num[1] + 1))
            print("Fillers for this line: [", end="")
            for i in range(9):
                if i == field_num[1]:
                    print("<This field>", end="")
                else:
                    print(self.fillers[field_num[0]][i], end="")
            print("] --> Fillers combined: ", fillers_line, end=" ")
            print("| Filler for this field: ", temp)

        temp.difference_update(fillers_line)
        if showlog:
            print("Value that fits only for this field in a line is: ", temp)
        if len(temp) == 1 and self.array[field_num[0]][field_num[1]] is not int(*temp):
            if showlog:
                print("Value is written")
            self.set_value((field_num[0], field_num[1], int(*temp)))

    def one_in_a_col(self, field_num, showlog=False):
        # this is a tactic, that is used when a number is in only one field of a column, so it should be there
        # despite the fact that this field and others have more possible values
        # in this one we compare fillers sets for each position in a column
        pass

    def one_in_a_box(self, field_num, showlog=False):
        # this is a tactic, that is used when a number is in only one field of a box, so it should be there
        # despite the fact that this field and others have more possible values
        # in this one we compare fillers sets for each position in a box
        pass

    def solve(self, showlog=False):
        for k in range(3):
            self.init_fillers(showlog)
            self.cross_fillers(showlog)
            self.show()
            self.box_fillers(showlog)
            self.show()
            self.one_in_all_fillers(showlog)
            self.show()


mysud = Sudoku([111, 122, 139, 196,
                255,
                324, 388, 392,
                419, 428, 437, 453, 481,
                516, 542, 577, 593,
                621, 678,
                766, 771, 784,
                814, 882,
                923, 941, 957])
# ,
#                446, 465, 472
mysud.solve(showlog=False)

# td:
# make the showlog work correctly and make it less ugly
# add some way to stop the iteration when it's stuck, or it finished (with returns from functions if they did sth)
