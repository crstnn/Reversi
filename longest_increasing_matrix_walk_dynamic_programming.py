def longest_walk(M: list) -> tuple:
    """
	Dynamic Programming solution of the longest increasing path in an n * m matrix
    :param M: Matrix of n * m (n being the rows and m being the columns) which contains a valid walk of at least one in length.
    :return: 2-tuple: the first element represents the longest walk and the second element is contains 2-tuples that
    represent the co-ordinates of (one of) the solutions.
    Time Complexity: O(nm) time and O(nm) auxiliary space. n being the rows and m being the columns in M
    """
    if not M or not M[0]: return 0, []
    DIRECTIONS = (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1))
    n, m = len(M), len(M[0])
    dp = [[0] * m for _ in range(n)]

    def is_in_range(row_in, column_in):
        if 0 <= row_in < n and 0 <= column_in < m:
            return True
        return False

    def dfs(i, j):
        if not dp[i][j]:
            dp[i][j] = 1 + max(
                dfs(x, y) if M[i][j] > M[x][y] else 0
                for (x, y) in [(d[0] + i, d[1] + j) for d in DIRECTIONS] if is_in_range(x, y))
        return dp[i][j]

    max_walk = max(dfs(x, y) for x in range(n) for y in range(m))

    def max_sol_pos():
        """Finds row and column of the local maxima of the solution walk"""
        for x in range(n):
            for y in range(m):
                if dp[x][y] == max_walk:
                    return [x, y]

    def walk_finder():
        """Walks back from local maxima of the solution walk and then reverses that to get the longest increasing walk"""
        counter = max_walk
        walk_sol = [tuple(max_sol_pos())]
        while counter > 1:
            for row, col in DIRECTIONS:
                temp_row, temp_col = walk_sol[-1][0] + row, walk_sol[-1][1] + col
                if is_in_range(temp_row, temp_col) and counter - 1 == dp[temp_row][temp_col] and M[walk_sol[-1][0]][
                        walk_sol[-1][1]] > M[temp_row][temp_col]:
                    walk_sol.append((temp_row, temp_col))
                    counter -= 1
                    break
        walk_sol.reverse()
        return walk_sol

    return max_walk, walk_finder()


