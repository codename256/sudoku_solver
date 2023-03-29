from sudoku_obj import Sudoku

# tests:
# test_one_in_a_box = Sudoku([243, 373,
#                             423, 733])
# test_one_in_a_row = Sudoku([129, 138,
#                             243,
#                             383])
# test_one_in_a_col = Sudoku([219, 318,
#                             423,
#                             733])

hard_level = Sudoku([118, 126, 163,
                     245, 269, 271, 292,
                     354,
                     412, 436, 473, 495,
                     577,
                     624, 691,
                     714, 723, 732, 797,
                     821, 846, 868,
                     962])

three_stars = Sudoku([195,
                      237, 264,
                      324, 352, 387, 396,
                      418, 429, 481,
                      562, 594,
                      613, 666, 685,
                      727, 753, 771,
                      814, 835, 842, 851, 867, 889,
                      938])
three_stars.solve()
three_stars.show_fillers()
three_stars.show()
# test_one_in_a_row.solve(showlog=False)
# test_one_in_a_col.solve(showlog=False)
# test_one_in_a_box.solve(showlog=False)
# hard_level.solve()
# hard_level.show_fillers()
# hard_level.show()





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

# test_one_in_a_box = Sudoku([243, 373,
#                             423, 733])
# test_one_in_a_row = Sudoku([129, 128,
#                             243,
#                             383])
# # ,
# #                446, 465, 472
# # mysud.solve(showlog=False)
# # other.solve()
# # hard_level.solve()
# test_one_in_a_box.solve(showlog=False)
# test_one_in_a_row.solve(showlog=False)

# td:
# make the showlog work correctly and make it less ugly
# add some way to stop the iteration when it's stuck, or it finished (with returns from functions if they did sth)
