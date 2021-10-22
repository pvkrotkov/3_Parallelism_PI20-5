from multiprocessing import Process, Pool
from multiprocessing.pool import ThreadPool
from threading import Thread
import random
import time

def element(index, A, B):
    i, j = index
    res = 0
    N = len(A[0]) or len(B)
    for k in range(N):
        res += A[i][k] * B[k][j]
    return res

def matrix_generator(min, max, square = False):
    if square:
        a = random.randint(min, max)
        b = a
    else:
        a, b = random.randint(min, max), random.randint(min, max)
    matrix1 = [[random.randint(0,100) for _ in range(b)] for _ in range(a)]
    matrix2 = [[random.randint(0,100) for _ in range(a)] for _ in range(b)]
    return matrix1, matrix2

def matrix_multiplier(matrix1, matrix2):
    maxS = 0 # max strings
    maxC = 0 # max columns

    # считаем сколько строк и столбцов будет в будущей матрице (перемноженной)
    for el in matrix1:
        maxS += 1
    for el2 in matrix2[0]:
        maxC += 1

    newmatrix = [['' for _ in range(maxC)] for _ in range(maxS)]
    
    amountOfProcesses = maxS ** maxC

    pool = ThreadPool(processes=amountOfProcesses)
    for i in range(maxS):
        for j in range(maxC):
            newmatrix[i][j] = pool.apply_async(element, ((i,j),matrix1,matrix2)).get()
    return newmatrix

def main():
    while True:
        matrix1, matrix2 = matrix_generator(2, 4, square = True)
        print(f'matrix1: {matrix1};\nmatrix2: {matrix2};')
        
        newmatrix = matrix_multiplier(matrix1, matrix2)
        print(f'newmatrix: {newmatrix}', end = '\n\n')

        time.sleep(3)

if __name__ == '__main__':
    Thread(target = main, daemon = True).start()
    input()