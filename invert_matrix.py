import fractions


def invert_matrix(m):
    """invert an n x n matrix"""
    # Error conditions
    if not array_is_matrix(m):
        print("Invalid matrix: array is not a matrix")
        return [[-1]];
    elif len(m) != len(m[0]):
        print("Invalid matrix: matrix is not square")
        return [[-2]];
    elif len(m) < 2:
        print("Invalid matrix: matrix is too small")
        return [[-3]];
    elif get_determinant(m) == 0:
        print("Invalid matrix: matrix is square, but singular (determinant = 0)")
        return [[-4]];

    # Calculation
    elif len(m) == 2:
        # simple case
        multiplier = 1 / get_determinant(m)
        inverted = [[multiplier] * len(m) for n in range(len(m))]
        inverted[0][1] = inverted[0][1] * -1 * m[0][1]
        inverted[1][0] = inverted[1][0] * -1 * m[1][0]
        inverted[0][0] = multiplier * m[1][1]
        inverted[1][1] = multiplier * m[0][0]
        return inverted
    else:
        """some steps combined in helpers to reduce traversals"""
        # get matrix of minors w/ "checkerboard" signs
        m_of_minors = get_matrix_of_minors(m)

        # calculate determinant (we need to know 1/det)
        multiplier = fractions.Fraction(1, get_determinant(m))

        # adjugate (swap on diagonals) and multiply by 1/det
        inverted = transpose_and_multiply(m_of_minors, multiplier)

        return inverted


def get_determinant(m):
    """recursively calculate the determinant of an n x n matrix, n >= 2"""
    if len(m) == 2:
        # trivial case
        return (m[0][0] * m[1][1]) - (m[0][1] * m[1][0])
    else:
        sign = 1
        det = 0
        for i in range(len(m)):
            det += sign * m[0][i] * get_determinant(get_minor(m, 0, i))
            sign *= -1
        return det


def get_matrix_of_minors(m):
    """get the matrix of minors and alternate signs"""
    matrix_of_minors = [[0 for i in range(len(m))] for j in range(len(m))]
    for row in range(len(m)):
        for col in range(len(m[0])):
            if (row + col) % 2 == 0:
                sign = 1
            else:
                sign = -1
            matrix_of_minors[row][col] = sign * get_determinant(get_minor(m, row, col))
    return matrix_of_minors


def get_minor(m, row, col):
    """
    get the minor of the matrix position m[row][col]
    (all values m[r][c] where r != row and c != col)
    """
    minors = []
    for i in range(len(m)):
        if i != row:
            new_row = m[i][:col]
            new_row.extend(m[i][col + 1:])
            minors.append(new_row)
    return minors


def transpose_and_multiply(m, multiplier=1):
    """swap values along diagonal, optionally adding multiplier"""
    for row in range(len(m)):
        for col in range(row + 1):
            temp = m[row][col] * multiplier
            m[row][col] = m[col][row] * multiplier
            m[col][row] = temp
    return m


def array_is_matrix(m):
    if len(m) == 0:
        return False
    first_col = len(m[0])
    for row in m:
        if len(row) != first_col:
            return False
    return True
