import numpy
from copy import deepcopy

EPSILON = 10**-int(open("EPSILON.txt", "r").read())

def read_matrix():
    file = open("m1.txt", "r").read()
    A = [item.split() for item in file.split('\n')]
    length = len(A)
    rows_counter = 0
    for i in range (length):
        rows_counter+=1

    for i in range(rows_counter):
        for j in range(length):
            A[i][j] = float(A[i][j])

    return A

def pivotare(x, A):
    maxim = 0
    imax = x
    for i in range(x, len(A[1]) - 1):
        if (abs(int(A[i][x])) > maxim):
            maxim = abs(int(A[i][x]))
            imax = i

    aux = A[x]
    A[x] = A[imax]
    A[imax] = aux
    return imax


def fact(x, A):
    n = len(A[1]) - 1
    for q in range(x + 1, n):
        # A[q][0]+factor*A[0][0]=0
        if numpy.abs(A[x][x]) > EPSILON:
            factor = float((-1) * (A[q][x]) / (A[x][x]))
        else:
            print("Eroare! Nu se poate face impartirea!")
            return 0

        for i in range(x, len(A[1])):
            A[q][i] = A[q][i] + factor * A[x][i]

    return 1

def triung(A):
    for i in range(0, len(A[1]) - 1):
        pivot = pivotare(i, A)
        if (abs(A[pivot][pivot]) <= EPSILON):
            print("Matrice singulara!")
            return 0
        x = fact(i, A)
        if x == 0:
            return 0
    return A

def afis(matrice):
    copy_matrix = deepcopy(matrice)
    max_length = 0
    for i in range(0, len(copy_matrix)):
        for j in range(0, len(copy_matrix[0])):
            length = len(str(copy_matrix[i][j]))
            if length > max_length:
                max_length = length

    for i in range(0, len(copy_matrix)):
        for j in range(0, len(copy_matrix[0])):
            length = len(str(copy_matrix[i][j]))
            if length<max_length:
                copy_matrix[i][j]= " "*(max_length-length) + str(copy_matrix[i][j])
            else:
                copy_matrix[i][j] = str(copy_matrix[i][j])
        print(copy_matrix[i])

    for i in range(len(matrice)):
        for j in range(len(matrice[0])):
            matrice[i][j] = float(matrice[i][j])

def s_inversa(A):

    B = []
    x = []
    n = len(A[1]) - 2

    for i in range(0, n + 1):
        B.append(A[i][n + 1])

    for i in range(0, len(B)):
        x.append([0])

    if numpy.abs(A[n][n]) > EPSILON:
        x[len(x)-1][0] = A[n][n + 1] / A[n][n]
    else:
        print("Eroare! Nu se poate face impartirea!")
        return 0

    for i in range(n - 1, -1, -1):
        aux = 0
        # print (i)
        for j in range(i, n):
            # print(i,j)
            # print (A[i][j+1], x[j+1])
            aux = aux + A[i][j + 1] * x[j + 1][0]
        if numpy.abs(A[i][i]) > EPSILON:
            x[i][0] = (B[i] - aux) / A[i][i]
        else:
            print("Eroare! Nu se poate face impartirea!")
            return 0

    return x

def matrix_product(A, B):
    rows_A = len(A)
    cols_A = len(A[0])
    rows_B = len(B)
    cols_B = len(B[0])

    if cols_A != rows_B:
        print("coloane in A: ", cols_A, "linii in B: ", rows_B)
        print ("Matricile nu se pot inmulti!")
        return 0

    C = []
    for col in range(rows_A):
        C.append([0]*cols_B)

    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                C[i][j] += A[i][k] * B[k][j]
    return C


def check_solution(A_init, x_gauss, B):

    n = len(A_init[1]) - 2
    print("Matricea initiala:")
    afis(A_init)

    print("Coeficientii libieri:")
    afis(B)

    N = numpy.subtract( matrix_product(A_init, x_gauss), B)
    norm = numpy.sum(numpy.abs(N) ** 2, axis=0)**(1./2)
    print("Norma (A_init * x_gauss - b_init): ", norm)

    return True

def get_solution_with_lib(matrix, b):
    b = numpy.array(b)
    solution = numpy.linalg.solve(matrix, b)
    return solution


def main():
    A = read_matrix()
    print("Sistem:")
    afis(A)

    A_init = []

    for i in range(0, len(A)):
        A_init.append([0]* (len(A[0])-1))

    for i in range (0, len(A)):
        for j in range (0, len(A[0])-1):
            A_init[i][j]=A[i][j]


    #afis(A_init)
    B = []
    n = len(A[1]) - 2

    for i in range(0, n + 1):
        B.append([A[i][n + 1]])

    A = triung(A)
    print("trungh")
    afis(A)


    if isinstance(A, int):
        return 0
    else:
        print("============================\n")
        system_solution = s_inversa(A)
        if isinstance(system_solution, int):
            return 0

        print("Solutia sistemului: ")
        afis(system_solution)
        check = check_solution(A_init, system_solution,B)


        x_lib = get_solution_with_lib(A_init, B)
        print("Solutia din librarie: ")
        print(x_lib)
        print("Inversa matricei A: ")
        A_init_inv = numpy.linalg.inv(A_init)
        print(A_init_inv)

        print("Norma (x_gauss - x_lib):")
        x_gauss_x_lib = numpy.subtract(system_solution, x_lib)
        y = numpy.sum(numpy.abs(x_gauss_x_lib) ** 2, axis=-1)**(1./2)
        print(numpy.linalg.norm(y))

        x_gauss_inv = numpy.subtract(system_solution, matrix_product(A_init_inv, B))
        y = numpy.sum(numpy.abs(x_gauss_x_lib) ** 2, axis=-1)**(1./2)
        print("Norma (x_gauss - A_inv_lib * b_init):")
        print(numpy.linalg.norm(y))

if __name__ == '__main__':
    main()
