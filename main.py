import csv
import random
import multiprocessing
import time

def element(index, matrix1, matrix2):
    i, j = index
    res = 0
    # get a middle dimension
    N = len(matrix1[0]) or len(matrix2)
    for k in range(N):
        res += matrix1[i][k] * matrix2[k][j]
    return res

def read_matrix(filename):
    try:
        with open (filename, "r", newline = '') as matrix_file:
            matrix = []
            spamreader = csv.reader(matrix_file, delimiter=';')
            for row in spamreader:
                matrix.append([float(el) for el in row])
    except:
        matrix = []
    return matrix

def write_matrix(filename, matrix):
    with open (filename, "w", newline = '') as matrix_file:
        spamwriter = csv.writer(matrix_file, delimiter=';')
        for row in matrix:
            spamwriter.writerow(row)
    return 

def generate_matrix(size = 2, start = 0, end = 9):
    return [[random.randint(start, end) for _ in range(size)] for _ in range(size)]

def immediately_writer(args):
    global lock
    filename, index, matrix1, matrix2 = args
    value = element(index, matrix1, matrix2)
    i, j = index
    with lock:
        matrix = read_matrix(filename)
        if len(matrix) <= i:
            for _ in range(i - len(matrix) + 1):
                matrix.append([])
        if len(matrix[i]) <= j:
            for _ in range(j - len(matrix[i]) + 1):
                matrix[i].append(0)
        matrix[i][j] = value
        write_matrix(filename, matrix)
    return value

def queue_creating(que):
    while True:
        matrix = generate_matrix()
        filename = f"matrix_{time.time()}.csv"
        write_matrix(filename, matrix)
        que.put(filename)
        time.sleep(5)

def init(l):
    global lock
    lock = l

def create_arguments(filename, matrix1, matrix2):
    indexes = []
    for i in range(len(matrix1)):
        for j in range(len(matrix2[0])):
            indexes.append([filename, (i, j), matrix1, matrix2])
    return indexes

def matrix_multiplier(que, run):
    while True:
        if run.value:
            matrix1 = read_matrix(que.get())
            matrix2 = read_matrix(que.get())
            filename = f"muliply_{time.time()}.csv"
            indexes = create_arguments(filename, matrix1, matrix2)

            l = multiprocessing.Lock()
            cnt = len(matrix1) + len(matrix2[0])
            pool = multiprocessing.Pool(processes = cnt, initializer = init,  initargs=(l,))

            pool.map(immediately_writer, indexes)
            pool.close()
            pool.join()



if __name__ == '__main__':
    matrix_q = multiprocessing.Queue()
    run = multiprocessing.Value('i', 1)
    queue_process =  multiprocessing.Process(target=queue_creating, args=[matrix_q])
    queue_process.start()

    multiplier_process = multiprocessing.Process(target=matrix_multiplier, args=[matrix_q, run])
    multiplier_process.start()
    proc_list = [queue_process, multiplier_process]

    print("stop - приостановить перемножение\nexit - выключить")
    while True:
        cmd = input()
        if cmd == "stop":
            run.value = not run.value
        elif cmd == "exit":
            for proc in proc_list:
                proc.terminate()
            break
        else:
            pass