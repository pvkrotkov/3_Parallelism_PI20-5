from random import randint
from multiprocessing import Pool

def save_matrix(a):
    with open('matrix.txt', 'a') as file:
        file.write(str(a) + " ")
def matrix_mnoj(x, y):
    result = sum(i*k for i, k in zip(x, y))
    return result

matrix1 = [[randint(0, 15) for i in range(3)] for i in range(3)]
matrix2 = [[randint(0, 10) for i in range(3)] for i in range(3)]
print(f'1st: {matrix1}')
print(f'2nd: {matrix2}')
if __name__=='__main__':
    with Pool(4) as pool:
        matrix = pool.starmap(matrix_mnoj, [(i, k) for i in matrix1 for k in zip(*matrix2)])
        print(matrix, 'result.txt')
        save_matrix(matrix)

