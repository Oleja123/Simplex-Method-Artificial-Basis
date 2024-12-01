from simplex_table import SimplexTable
from no_solution_exception import NoSolutionException


try:
    st = SimplexTable(3, 2, [-1, -4, -1], [[1, -1, 1], [2, -5, -1]], [3, 0])
    st.print_table_info()
except NoSolutionException as e:
    print(e)