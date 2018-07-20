from copy import deepcopy

def read_input(filename):
    file_object = open(filename, "r")

    n = int(file_object.readline())
    file_object.readline()
    epsilon = 10**-int(file_object.readline())
    file_object.readline()
    k_max = int(file_object.readline())
    file_object.readline()

    matrix = []
    while 1:
        line = file_object.readline().replace('\n', '')
        if line == "":
            break
        line = [int(i) for i in line.split(' ')]
        matrix.append(line)

    file_object.close()

    return n, epsilon, k_max, matrix


def transpose(matrix):
    n = len(matrix)
    transpose_matrix = []
    for i in range (0, n):
        line = []
        for j in range (0, n):
            line.append(matrix[j][i])
        transpose_matrix.append(line)

    return transpose_matrix

def norm_1(matrix):
    norm = -9999999999999999999999
    n = len(matrix)
    for i in range (0, n):
        s = 0
        for j in range (0, n):
            s+=abs(matrix[j][i])
        if s > norm:
            norm = s

    return norm


def infinity_norm(matrix):
    norm = -9999999999999999999999
    n = len(matrix)
    for i in range(0, n):
        s = 0
        for j in range(0, n):
            s += abs(matrix[i][j])
        if s > norm:
            norm = s

    return norm


def multiply_matrix_constant(matrix, constant):
    n = len(matrix)
    for i in range (0, n):
        for j in range (0, n):
            matrix[i][j] = matrix[i][j]*constant

    return matrix


def matrix_substract(A, B):
	result = [[A[i][j]-B[i][j] for j in range(0,len(A))] for i in range(0,len(A))]
	return result


def identity_matrix(n):
    In = []
    for i in range (0, n):
        In.append([0]*n)
    for i in range (0, n):
        In[i][i] = 1
    return In


def matrix_product(A, B):
	result = []
	for i in range(0,len(A)):
		result.append([0]*len(A))
	for i in range (0,len(A)):
		for j in range(0,len(A)):
			for k in range(0,len(A)):
				result[i][k] += A[i][j] *B[j][k]
	return result


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


def Schultz(matrix, k_max, epsilon, n):
    print("Metoda Schultz")
    B = []
    for i in range(0, n):
        B.append([0]*n)

    for i in range (0, n):
        for j in range (0, n):
            B[i][j] = -matrix[i][j]

    V0 = multiply_matrix_constant(transpose(matrix), 1/(norm_1(matrix)*infinity_norm(matrix)))
    V1 = V0
    k = 0
   # deltaV = norm_1(matrix_substract(V1,V0))

    V0 = V1
    C = matrix_product(B, V0)
    for i in range (0, n):
        C[i][i] += 2

    V1 = matrix_product(V0, C)
    deltaV = norm_1(matrix_substract(V1, V0))
    k += 1

    while deltaV >= epsilon and k <= k_max and deltaV <= 10**10:
        V0 = V1
        C = matrix_product(B, V0)
        for i in range(0, n):
            C[i][i] += 2

        V1 = matrix_product(V0, C)
        deltaV = norm_1(matrix_substract(V1, V0))
        k += 1

    print("Iteratii efectuate:", k)
    if deltaV < epsilon:
        print("Norma 1:", norm_1(matrix_substract(matrix_product(matrix, V1), identity_matrix(n))))
        return V1
    else:
        return "divergenta"


def Li_Li_1(matrix, k_max, epsilon, n):
    print("Metoda Li si Li (1)")
    B = []
    for i in range(0, n):
        B.append([0] * n)

    for i in range(0, n):
        for j in range(0, n):
            B[i][j] = -matrix[i][j]

    V0 = multiply_matrix_constant(transpose(matrix), 1 / (norm_1(matrix) * infinity_norm(matrix)))
    V1 = V0
    k = 0
    deltaV = norm_1(matrix_substract(V1, V0))

    c = matrix_product(B, V0)
    for i in range(0, n):
        c[i][i] += 3

    V = matrix_product(V0, c)

    C = matrix_product(B, V)
    for i in range(0, n):
        C[i][i] += 3

    V1 = matrix_product(V0, C)
    deltaV = norm_1(matrix_substract(V1, V0))
    k += 1

    while deltaV >= epsilon and k <= k_max and deltaV <= 10**10:
        V0 = V1
        c = matrix_product(B, V0)
        for i in range(0, n):
            c[i][i] += 3

        V = matrix_product(V0, c)

        C = matrix_product(B, V)
        for i in range(0, n):
            C[i][i] += 3

        V1 = matrix_product(V0, C)
        deltaV = norm_1(matrix_substract(V1, V0))
        k += 1

    print("Iteratii efectuate:", k)
    if deltaV < epsilon:
        print("Norma 1:", norm_1(matrix_substract(matrix_product(matrix, V1), identity_matrix(n))))
        return V1
    else:
        return "divergenta"


def Li_Li_2(matrix, k_max, epsilon, n):
    print("Metoda Li si Li (2)")
    B = []
    for i in range(0, n):
        B.append([0] * n)

    for i in range(0, n):
        for j in range(0, n):
            B[i][j] = -matrix[i][j]

    V0 = multiply_matrix_constant(transpose(matrix), 1 / (norm_1(matrix) * infinity_norm(matrix)))
    V1 = V0
    k = 0
    deltaV = norm_1(matrix_substract(V1, V0))

    c = matrix_product(V0, B)
    for i in range(0, n):
        c[i][i] += 3

    d = matrix_product(c, c)

    C = matrix_product(V0, B)
    for i in range(0, n):
        C[i][i] += 1

    V = multiply_matrix_constant(matrix_product(C, d), 1/4)
    for i in range(0, n):
        V[i][i] += 1

    V1 = matrix_product(V, V0)

    deltaV = norm_1(matrix_substract(V1, V0))
    k += 1

    while deltaV >= epsilon and k <= k_max and deltaV <= 10 ** 10:
        V0 = V1
        c = matrix_product(V0, B)
        for i in range(0, n):
            c[i][i] += 3

        d = matrix_product(c, c)

        C = matrix_product(V0, B)
        for i in range(0, n):
            C[i][i] += 1

        V = multiply_matrix_constant(matrix_product(C, d), 1 / 4)
        for i in range(0, n):
            V[i][i] += 1

        V1 = matrix_product(V, V0)
        deltaV = norm_1(matrix_substract(V1, V0))
        k += 1

    print("Iteratii efectuate:", k)
    if deltaV < epsilon:
        print("Norma 1:", norm_1(matrix_substract(matrix_product(matrix, V1), identity_matrix(n))))
        return V1
    else:
        return "divergenta"


def main():
    n, epsilon, k_max, matrix = read_input("input.txt")

    A_1 = Schultz(matrix, k_max, epsilon, n)
    print("Aproximarea A^-1:")
    afis(A_1)
    print()
    A_1 = Li_Li_1(matrix, k_max, epsilon, n)
    print("Aproximarea A^-1:")
    afis(A_1)
    print()
    A_1 = Li_Li_2(matrix, k_max, epsilon, n)
    print("Aproximarea A^-1:")
    afis(A_1)
    print()


if __name__ == "__main__":
    main()
