class Sudoku:
    """This is a class for a sudoku board with methods for solving it using logical approach.
    Takes an input from the user and creates a sudoku board with those preconditions.
    Sample input is a list of 3-digit numbers xyz.
    x - position top-bot (1-9)
    y - position l-r (1-9)
    z - value(1-9)
    The (1, 1) point for x and y is the left-top cell. The last one is bot-right one with id (9, 9).
    Example:
         Sudoku([123, 456]) - set a value of 3 in the position x: 1, y: 2
                            - set a value of 6 in the position x: 4, y: 5
    Sudoku is stored in two tables:
        board - each field is " ", that means empty, or 1-9 if the value is found or inserted at the start
        fillers - table of sets, for each field they start at {range(1,10)}. If any value can't be written
        in a field, then it is deleted from the set corresponding with this value coordinates (x, y)

    Methods:
        find_the_cross
             ..._box
        cross_fillers
        box_fillers
        one_in_a_row
             ..._col
             ..._box

    To implement:
        hidden_pair
        hidden_three
        swordfish
    """

    def __init__(self, user_input):
        """Initialize the sudoku table according to information in Sudoku.__doc__"""

        print("<" * 20, "SUDOKU INITIALIZATION", ">" * 20)
        self.board = []
        self.fillers = []

        for _ in range(9):
            self.board.append([" "] * 9)
            line_filler = [set(range(1, 10)) for _ in range(9)]
            self.fillers.append(line_filler)
        print("Sudoku created")
        self.import_values(*user_input)

    def __repr__(self):
        return str(self.board)

    def __str__(self):
        self.printer = ""
        for line in self.board:
            self.printer += str(line) + "\n"
        return self.printer

    def show(self):
        """Print the sudoku board with borders"""

        print("\nCurrent state of the sudoku\n" + "_" * 25)
        for i, line in enumerate(self.board):
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
        """Print:
         val - value that field (i, j) in the board possesses
         filler - set of possible values for a field (i, j)
        """

        for i in range(9):
            for j in range(9):
                print("Val: ", self.board[i][j], "Filler: ", self.fillers[i][j])

    def show_fillers(self):
        """Print the possible values set for each field in a style of a table"""

        for i, line in enumerate(self.fillers):
            if not i % 3:
                print("-"*117)
            print("|", end="")
            for item_fil in line:
                print(("".join(str(x) for x in [*item_fil] if isinstance(x, (int, float))).center(10)), end=" | ")
            print()
        print("-" * 117)

    def add_value(self, val: tuple):
        """Add value for a field according to information in Sudoku.__doc__"""

        print(f"Insert value: row {val[0] + 1}, col {val[1] + 1}, num {val[2]}")
        self.board[val[0]][val[1]] = val[2]

    def import_values(self, *values):
        """This method is used at the start of creating a Sudoku board.
        It takes all the values that were defined by user according to information
        in Sudoku.__doc__
        """

        for val in values:
            next_val = str(val)
            next_val = tuple([int(next_val[0]) - 1, int(next_val[1]) - 1, int(next_val[2])])
            self.add_value(next_val)
        self.show()

    def set_value(self, val):
        """Created to determine the difference between importing values at the start and
        setting its value after determining what's the correct one to insert.
        """

        print("Value for this field is determined to be:", val[2])
        self.add_value(val)

    def init_fillers(self):
        """If a field has a value, then update its possible values to have only this one"""

        print("\n1. If value known, leave ONLY field value in its fillers set(). Repeat for all fields")
        for i, line in enumerate(self.board):
            for j, field in enumerate(line):
                if field != " ":
                    self.fillers[i][j].intersection_update({field})

    def find_the_cross(self, field_num):
        """Works on fields values
        Find the defined values in board (" " doesn't count) that are in one line
        with checked field left-right and top-bottom
        Field included
        Return the values as a set
        """

        tb, lr = [], []  # top-bottom, left-right

        for i in range(9):
            tb.append(self.board[i][field_num[1]])
            lr.append(self.board[field_num[0]][i])
        cross = {*tb, *lr}.difference({" ", self.board[field_num[0]][field_num[1]]})

        return cross

    def find_the_box(self, field_num):
        """Works on fields values
        Find the defined values in board (" " doesn't count) that are in one box 3x3
        with checked field (sudoku has 9 division boxes 3x3)
        Field included
        Return the values as a set
        """

        box_ids = dict()
        box = set()
        for i in range(3):
            box_ids[i] = 0
            box_ids[i + 3] = 1
            box_ids[i + 6] = 2
        box_id = (box_ids[field_num[0]], box_ids[field_num[1]])

        for i in range(3):
            for j in range(3):
                box.update({self.board[i + 3 * box_id[0]][j + 3 * box_id[1]]})
            box.difference_update({" ", self.board[field_num[0]][field_num[1]]})

        return box

    def cross_fillers(self):
        """Works on all fillers at one run
        From a currently checked filler field remove values that are written in top-bot,
        left-right fields (cross). If the field is left with only one filler, its
        board value will be updated
        """

        print("2. Remove from field filler values that are written in top-bot left-right fields (cross)")
        print("If only one filler element and the board value is ' ', then it'll be updated with the filler")

        for i, line in enumerate(self.board):
            for j, val in enumerate(line):
                cross = self.find_the_cross((i, j))
                self.fillers[i][j].difference_update(cross)

                if len(self.fillers[i][j]) == 1 and self.board[i][j] == " ":
                    print("Updated value from '{}' to {}".format(self.board[i][j], *self.fillers[i][j]))
                    self.set_value((i, j, int(*self.fillers[i][j])))

    def box_fillers(self):
        """Works on all fillers at one run
        From a currently checked filler field remove values that are written in top-bot,
        left-right fields (cross). If the field is left with only one filler, its
        board value will be updated
        """

        for i in range(9):
            for j in range(9):
                box = self.find_the_box((i, j))
                self.fillers[i][j].difference_update(box)

                if len(self.fillers[i][j]) == 1 and self.board[i][j] == " ":
                    print("Update value from '{}' to {}".format(self.board[i][j], *self.fillers[i][j]))
                    self.set_value((i, j, int(*self.fillers[i][j])))

    def one_in_all_fillers(self):
        """
        """
        print("<<< ONE IN A ROW >>>")
        for i in range(9):
            for j in range(9):
                self.one_in_a_row((i, j))

        print("<<< ONE IN A COL >>>")
        for i in range(9):
            for j in range(9):
                self.one_in_a_col((i, j))

        print("<<< ONE IN A BOX >>>")
        for i in range(9):
            for j in range(9):
                self.one_in_a_box((i, j))

    def one_in_a_row(self, field_num):
        """Checks if there is a field in the board that is the only one possible for some value in a row
        If there is one, write this value in this field. Update board and fillers
        """

        # Use update instead of '=' to have different set id's
        temp = set()
        temp.update(self.fillers[field_num[0]][field_num[1]])
        fillers_line = set()

        # consider: .update(*self.fillers[field_num[0]][:9]) with removing the element set
        for i in range(9):
            if i is not field_num[1]:
                fillers_line.update(self.fillers[field_num[0]][i])
        temp.difference_update(fillers_line)

        if len(temp) == 1 and self.board[field_num[0]][field_num[1]] is not int(*temp):
            self.set_value((field_num[0], field_num[1], int(*temp)))
            self.fillers[field_num[0]][field_num[1]].intersection_update(temp)

    def one_in_a_col(self, field_num):
        """Checks if there is a field in the board that is the only one possible for some value in a col
        If there is one, write this value in this field. Update board and fillers
        """

        # Use update instead of '=' to have different set id's
        temp = set()
        temp.update(self.fillers[field_num[0]][field_num[1]])
        fillers_line = set()

        # consider: .update(*self.fillers[field_num[0]][:9]) with removing the element set
        for i in range(9):
            if i is not field_num[1]:
                fillers_line.update(self.fillers[i][field_num[1]])
        temp.difference_update(fillers_line)

        if len(temp) == 1 and self.board[field_num[0]][field_num[1]] is not int(*temp):
            self.set_value((field_num[0], field_num[1], int(*temp)))
            self.fillers[field_num[0]][field_num[1]].intersection_update(temp)

    def one_in_a_box(self, field_num):
        """Checks if there is a field in the board that is the only one possible for some value in a box (3x3)
        If there is one, write this value in this field. Update board and fillers
        """

        # Use update instead of '=' to have different set id's
        temp, fillers_box = set(), set()
        box_ids = dict()
        for i in range(3):
            box_ids[i] = 0
            box_ids[i + 3] = 1
            box_ids[i + 6] = 2

        temp.update(self.fillers[field_num[0]][field_num[1]])

        box_id = (box_ids[field_num[0]], box_ids[field_num[1]])
        for i in range(3):
            for j in range(3):
                if [i, j] != [(field_num[0]) % 3, (field_num[1]) % 3]:
                    fillers_box.update(self.fillers[i + 3 * box_id[0]][j + 3 * box_id[1]])

        temp.difference_update(fillers_box)
        if len(temp) == 1 and self.board[field_num[0]][field_num[1]] != int(*temp):
            self.set_value((field_num[0], field_num[1], int(*temp)))
            self.fillers[field_num[0]][field_num[1]].intersection_update(temp)

    def advanced_search(self):
        # hidden pair
        # hidden three
        # swordfish method
        pass

    def is_done(self):
        """Check if there is still any empty field left on board"""

        for line in self.board:
            for elem in line:
                if elem == ' ':
                    return False
                else:
                    continue
        else:
            return True

    def solve(self):
        """The main method for solving the sudoku. It uses all of defined methods in a loop
        until the Sudoku board is solved. Additional comments are used to show
        the process of solving.
        Max number of iterations is set to 20. Usually when it doesn't solve the board
        in that many loops, it won't solve it at all
        """

        i = 0

        while True:
            print("<"*20, "INIT FILLERS", ">"*20)
            self.init_fillers()
            self.show()

            print("<"*20, "CROSS FILLERS", ">"*20)
            self.cross_fillers()
            self.show()

            print("<"*20, "BOX FILLERS", ">"*20)
            self.box_fillers()
            self.show()

            print("<"*20, "ONE IN ALL FILLERS", ">"*20)
            self.one_in_all_fillers()
            self.show()

            print("<<<<< {} >>>>>".format(i))

            pass

            if self.is_done():
                print("Finished after {} loops".format(i))
                break
            i += 1
            if i > 20:
                break
