from simplex_table import SimplexTable
from no_solution_error import NoSolutionError
from miscalc_number import MiscalcNumber as ms


try:
    # st = SimplexTable(3, 2, [-1, -4, -1], [[1, -1, 1], [2, -5, -1]], [3, 0])
    # st = SimplexTable(4, 2, [1, 1, 1, 0], [[5, 2, 1, 0], [3, 1, 4, -1]], [10, 83])
    # st = SimplexTable(4, 2, [-8, 6, 5, -2], [[1,4,-1, 1], [4, -6, 3, -7]], [16, 20])
    # st = SimplexTable(5, 3, [-4, -5, 0, 0, 0], [[2,4,1, 0,0], [1,1,0, 1,0],[2,1,0, 0,1]], [560, 170, 300])
    # st = SimplexTable(6, 3, [1, -1, 1, 1, 1, -1], [[1,0,0, 1,0, 6], [3,1,-4, 0,0, 2], [1,2,0,0,5,2]], [9, 2, 6])
    # st = SimplexTable(5, 3, [1, 2, 0, 0, 0], [ [1, 2, 1, 0, 0],  [4, 2, 0, 1, 0],  [4, 6, 0, 0, -1]], [120, 240, 320])
    # st = SimplexTable(4, 3, [4, 1, 0, 0], [ [3, 1, 0, 0],  [4, 3, -1, 0],  [1, 2, 0, 1]], [3, 6, 4])
    # st = SimplexTable(4, 2, [-8, -6, 0, 0], [ [10, 5, 1, 0],  [6, 9, 0, 1] ], [50, 54])
    #файловый ввод
    file_in = open("input.txt", encoding='UTF-8')
    lines = file_in.readlines()
    file_in.close()
    n = int(lines[0].split()[0])
    m = int(lines[0].split()[1])
    f = [int(i) for i in lines[1].split()]
    matrix = []
    for line in lines[2:-1]:
        matrix.append([int(i) for i in line.split()])
    b = [int(i) for i in lines[-1].split()]
    st = SimplexTable(n, m, f, matrix, b)
    st.solve()
    st.print_table_info()
except NoSolutionError as e:
    print(e)
