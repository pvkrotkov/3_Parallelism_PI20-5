from multiprocessing import Process, Manager, Queue


# функция принимающая кол-во строк и столбцов, и списки в виде матриц и делает их перемножение
def element(i: int, j: int, A: list, B: list, answer: Queue):
    answer.put((sum(A[i][k] * B[k][j] for k in range(len(A[0]) or len(B))), [i, j]))


# Начало работы программы
if __name__ == '__main__':
    manager = Manager()

    # Как выглядит матрица в файле matrix1.txt:

    # [[3, 2, 6],
    # [2, 7, 3]]

    # Пишем в первом input 3
    # Пишем во втором input 2
    # То есть мы даем программе понять что матрица у нас
    # А 2 на 3 2-строки 3-столбца

    n1 = int(input('Введите число элементов в строке -> '))
    n2 = int(input('Введите число строк в матрице -> '))

    matrix1 = [[[] for i in range(n1)] for j in range(n2)]
    matrix1 = [[0 for i in range(n1)] for j in range(n2)]

    # [[1, 5],
    # [1, 2],
    # [7, 1]]

    # Пишем в первом input 2
    # Пишем во втором input 3

    # То есть мы даем программе понять что матрица у нас
    # B 3 на 2 3-строки 2-столбца

    n1 = int(input('Введите число элементов в строке -> '))
    n2 = int(input('Введите число строк в матрице -> '))

    matrix2 = [[[] for i in range(n1)] for j in range(n2)]
    matrix2 = [[0 for i in range(n1)] for j in range(n2)]

    matrix_l1 = []
    matrix_l2 = []
    k = 0
    kk = 0

    # открытие файлов matrix1.txt и matrix2.txt и их чтение

    with open('matrix1.txt', 'r') as m1:
        for line in m1.read():
            if line != '[' and line != ']' and line != ',' and line != '\n' and line != ' ':
                matrix_l1 += line

    with open('matrix2.txt', 'r') as m2:
        for line in m2.read():
            if line != '[' and line != ']' and line != ',' and line != '\n' and line != ' ':
                matrix_l2 += line

    for i in range(len(matrix1)):
        for j in range(len(matrix1[0])):
            try:
                matrix1[i][j] = int(matrix_l1[k])
                k += 1
            except:
                if k <= len(matrix_l1):
                    i = k
                    k += 1

    print(matrix1)

    for i in range(len(matrix2)):
        for j in range(len(matrix2[0])):
            try:
                matrix2[i][j] = int(matrix_l2[kk])
                kk += 1
            except:
                if kk <= len(matrix_l2):
                    i = kk
                    kk += 1

    print(matrix2)

    matrix3 = [[0 for _ in range(len(matrix2[0]))] for _ in range(len(matrix2[0]))]

    processes = list()
    answer = manager.Queue()

    for i in range(len(matrix3)):
        for j in range(len(matrix3[i])):
            p = Process(target=element, args=(i, j, matrix1, matrix2, answer,))
            processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()

    for i in range(len(matrix3)):
        for j in range(len(matrix3[i])):
            mt_l, mt_k = answer.get()
            matrix3[mt_k[0]][mt_k[1]] = mt_l

    # запись перемножения матрицы в файл result.txt
    with open('result.txt', 'w') as file:
        '''Программа выводит сначала первые две матрицы полученные из файлов'''
        '''Потом выводится результат перемножения матриц и соответсвенно записывает результат'''
        file.write(str(matrix3))

    print(matrix3)
