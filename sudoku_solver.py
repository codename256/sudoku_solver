from sudoku_obj import Sudoku

# tests:
test_one_in_a_box = Sudoku([243, 373,
                            423, 733])
test_one_in_a_row = Sudoku([129, 138,
                            243,
                            383])
test_one_in_a_col = Sudoku([219, 318,
                            423,
                            733])

test_one_in_a_row.solve(showlog=False)
test_one_in_a_col.solve(showlog=False)
test_one_in_a_box.solve(showlog=False)
