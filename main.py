from simplex_table import SimplexTable

st = SimplexTable(3, 2, [-1, -4, -1], [[1, -1, 1], [2, -5, -1]], [3, 0])
# st = SimplexTable(4, 3, [1, -2, 3, -10], [[1, 1, 2, -6], [1, 1, 4, -8], [4, 2, 1, -4]], [1, 1, 3])
st.print_table_info()