

def rotateMatrix(matrix):
    '''
    GENERATOR:
    yields each swapped pair after a swap occurs.

    in-place 90deg rotation of an NxN matrix.

    Let x = total number of matrix cells
    Time: O(x)?
    Space: O(1)
    '''

    N = len(matrix)
    n = N-1
    for i in range(0,N//2):

        for j in range(i,n):


            # 1 2
            # 4 3
            if i + j == n:
                break

            matrix[i][j], matrix[n-i][n-j] = matrix[n-i][n-j], matrix[i][j] 
            yield (matrix[i][j], matrix[n-i][n-j])

            matrix[i][j], matrix[n-j][i] = matrix[n-j][i], matrix[i][j]
            yield (matrix[i][j], matrix[n-j][i]) 

            matrix[j][n-i], matrix[n-i][n-j] = matrix[n-i][n-j],matrix[j][n-i]
            yield (matrix[j][n-i], matrix[n-i][n-j]) 