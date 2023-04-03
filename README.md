This is an implementation of a class for a sudoku board with methods for solving it using logical approach.
    Takes an input from the user and creates a sudoku board with those preconditions.
    
    Sample input is a list of 3-digit numbers xyz.
    x - position top-bot (1-9)
    y - position l-r (1-9)
    z - value(1-9)
    
    The (1, 1) point for x and y is the left-top cell. The last one is bot-right one with id (9, 9).
    Example:
         new_sud = Sudoku([123, 456]) 
         - set a value of 3 in the position x: 1, y: 2
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
