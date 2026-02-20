import time
def remove_string(s, l1, n):
    # Base case: no more strings to remove
    if n == 0:
        return s
    # Remove all occurrences of the last string in the list
    current = l1[n - 1]
    s = s.replace(current, "")
    # Recursive call on the remaining list
    return remove_string(s, l1, n - 1)


s = "abcdxyzabc"
l1 = ["ab", "yz"]
n = 2

print("Before:", s, ", remove:", l1)
result = remove_string(s, l1, n)
print("After :", result)


# q3
def has_square_with_sum(l1, num):
    """
        returns (row_index, col_index) of the top-left of the first 2x2 square
        whose sum equals num or (-1, -1) if none exists.
    """
    # must have at least 2 rows and 2 columns to contain a 2x2 square
    if not l1 or len(l1) < 2 or not l1[0] or len(l1[0]) < 2:
        return -1, -1

    rows = len(l1)
    cols = len(l1[0])

    # scan all possible top-left corners of a 2x2 square
    for i in range(rows - 1):
        for j in range(cols - 1):
            s = l1[i][j] + l1[i][j + 1] + l1[i + 1][j] + l1[i + 1][j + 1]
            if s == num:
                return i, j

    return -1, -1

matrix = [
    [5, 8, 3, 0, 9],
    [2, 1, 2, 7, 4],
    [3, 5, 2, 8, 2],
    [7, 7, 6, 2, 8]
    ]

print(has_square_with_sum(matrix, 10))  # (1, 1)
print(has_square_with_sum(matrix, 17))  # (-1, -1)
