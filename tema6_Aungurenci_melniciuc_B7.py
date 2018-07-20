import sys
import random
from decimal import *
import operator
import numpy

EPSILON = 10 ** -9


def read_info(file_name):
    '''
        citeste din fisierul dat ca parametru dimensiunea datelor (n), elementele vectorului b
        si elementele a_ij != 0 din matricea rara A (matrice)
        returneaza un tuplu (n, b, matrice)
    '''

    file_obj = open(file_name, "r")
    n = int(file_obj.readline())  # dimensiunea
    file_obj.readline()

    matrice = []  # matricea

    while 1:
        a = file_obj.readline().replace('\n', '')
        if a == '':
            break
        linia = int(a.split(', ')[1])
        element = []
        element.append(Decimal(a.split(', ')[0]))
        element.append(int(a.split(', ')[2]))

        try:
            ok = False
            for index_linie, linie in enumerate(matrice):
                if index_linie == linia:
                    for e in linie:
                        if e[1] == element[1]:
                            e[0] += element[0]
                            ok = True

            if element[1] == linia and ok == False:
                try:
                    matrice[linia].append(element)
                except:
                    matrice.append([])
                    matrice[linia].insert(0, element)
            elif ok == False:
                matrice[linia].insert(0, element)
        except:
            if len(matrice) - 1 == linia - 1:
                matrice.insert(linia, [element])
            else:
                while len(matrice) - 1 < linia - 1:
                    matrice.append([])
                    matrice.insert(linia, [element])

    return (n, matrice)


def ran(n):
    M = []
    for i in range(0, n):
        M.append([[0, 0]])

    for i in range(0, n):

        for h in range(0, n):
            x = random.random() * 100
            j = random.randint(0, n - 1)
            if len(M[i]) < 10 and len(M[j]) < 10 and (i < j):
                M[i].append([x, j])
                M[j].append([x, i])
    for i in range(0, len(M)):
        M[i] = M[i][1:]
    for i in range(0, len(M)):
        M[i].sort(key=operator.itemgetter(1))

    return M


def afis_frumos(m, n):
    for i in range(1, n):
        print(m[i])


def metoda_puterii(n, M):
    norma = 0
    x = [1 for i in range(0, n + 1)]
    v = []
    for i in range(0, n):
        norma = norma + x[i] * x[i]
    norma = norma ** (1 / 2)
    for i in range(0, n):
        v.append(1 / norma * x[i])
    # print(v)
    w = inmult(n, M, v)

    lam = prod_sc(w, v)
    k = 0
    v = unu_pe_norma(w)
    w = inmult(n, M, v)
    lam = prod_sc(w, v)
    k = k + 1
    while (norma_dif(v, lam, w) > n * EPSILON and k < 10000):
        # print(norma_dif(v,lam,w))
        v = unu_pe_norma(w)
        w = inmult(n, M, v)
        lam = prod_sc(w, v)
        k = k + 1
    print("k=", k, "Aproximarea valorii proprii de modul maxim(lambda)=", lam, "\n Vectorul asociat:", v)


def inmult(n, a, b):
    rez = []
    for i in range(0, n):
        suma = 0
        for element in a[i]:
            suma = suma + float(element[0]) * b[element[1]]
        rez.append(suma)
    return rez


def prod_sc(w, v):
    rez = 0
    for i in range(0, len(w)):
        rez += (w[i] * v[i])
    return rez


def unu_pe_norma(w):
    norma = 0
    rez = []
    maxim = max(abs(i) for i in w)
    for i in range(0, len(w)):
        norma = norma + float(w[i] / maxim) ** 2
    norma = norma ** (1 / 2) * maxim
    for i in range(0, len(w)):
        rez.append(float(w[i]) * 1 / norma)
    return rez


def norma_dif(v, lam, w):
    rez = []
    norma = 0
    ct = 0
    for i in range(0, len(v)):
        ct += lam * v[i]
    for i in range(0, len(w)):
        rez.append(float(w[i]) - lam * v[i])
    maxim = max(abs(i) for i in rez)
    for i in range(0, len(rez)):
        norma = norma + (rez[i] / maxim) ** 2
    norma = norma ** (1 / 2) * maxim
    return norma


def afis_frumos(v):
    for i in range(0, len(v)):
        sys.stdout.write(str("{0:.4f}".format(round(v[i], 4))) + ' ')
    sys.stdout.write('\n')


#########################################################

def e_sim(dimensiune_b, B):
    #########################
    for i in range(0, len(B)):
        B[i].sort(key=operator.itemgetter(1))
    file_obj = open("b_normal.txt", "w")

    file_obj.write(str(dimensiune_b) + '\n' + '\n')
    for i in range(0, dimensiune_b):
        for element in B[i]:
            line = str(element[0]) + ', ' + str(i) + ', ' + str(element[1]) + '\n'
            file_obj.write(line)
    file_obj.close()
    B = read_info("b_normal.txt")[1]
    #########################
    file_obj = open("b_transpus.txt", "w")

    file_obj.write(str(dimensiune_b) + '\n' + '\n')

    f = []
    for index_linie_b, linie_b in enumerate(B):
        for element in linie_b:
            line = [element[0]] + [element[1]] + [index_linie_b]
            f.append(line)

        f.sort(key=operator.itemgetter(1))

    for element in f:
        line = str(element[0]) + ', ' + str(element[1]) + ', ' + str(element[2]) + '\n'
        file_obj.write(line)

    file_obj.close()

    b_transpus = read_info("b_transpus.txt")[1]
    # print (b_transpus)
    for i in range(0, dimensiune_b):
        for j in range(0, len(B[i])):
            if (round(B[i][j][0], 9) != round(b_transpus[i][j][0], 9)):
                print(i, j, B[i][j], b_transpus[i][j])
                return False
    return True


def svd():
    p = random.randint(3, 5)
    n = random.randint(3, 5)
    while p <= n:
        p = random.randint(3, 5)

    matrix = numpy.random.random((p, n))
    b = [random.random() for _ in range (p)]
    #b = numpy.random.random((p, 1))
    print("Matricea:", matrix)
    print("Vectorul b:", b)
    print()
    u, singular_values, vt = numpy.linalg.svd(matrix)

    print("Valorile singulare ale matricei:\n", singular_values)

    matrix_rank = 0
    max_singular_value = -9999999999999999
    min_singular_value = 9999999999999999
    for i in singular_values:
        if i > 0:
            matrix_rank += 1
            if i > max_singular_value:
                max_singular_value = i
            if i < min_singular_value:
                min_singular_value = i

    print("Rangul matricei:", matrix_rank)

    print("Numarul de conditionare al matricei:", max_singular_value/min_singular_value)

    SI = [[0] * (p) for _ in range(n)]
    for i in range(0, p):
        for j in range(0, n):
            if i == j:
                SI[i][j] = singular_values[i]

    print("\nPseudoinversa Moore-Penrose a matricei:\n", numpy.matmul(numpy.matmul(vt, SI), u.transpose()))

    x = numpy.linalg.solve(numpy.matmul(matrix.transpose(), matrix), numpy.matmul(matrix.transpose(), b))

    print("\nVectorul x:", x)

    s = 1
    As = [[0] * (n) for _ in range(0, p)]
    for s_ in range(0, s):
        new_u = [[0] * (1) for _ in range(len(u))]
        for i in range(0, len(u)):
            new_u[i][0] = u[i][s_]

        new_v = [[0] * (1) for _ in range(len(vt))]
        for i in range(0, len(vt)):
            new_v[i][0] = vt[i][s_]

        w = [[0] * (n) for _ in range(0, p)]
        for i in range(0, p):
            for j in range(0, n):
                w[i][j] = new_u[i][0] * new_v[j][0] * singular_values[s_]

        As = numpy.add(As, w)

    print("\nMatricea As:", As)
    print("\nNorma infinit |A - As| =", numpy.linalg.norm(numpy.subtract(matrix, As), numpy.inf))


def main():
    print("Generez aleator o matrice rara simetrica...")
    n = 600
    M = ran(n)

    print("Citesc matricea din fisier...")
    a_txt = read_info("m_rar_sim_2018.txt")

    print("Verific daca matricea citita din fisier este simetrica...")
    if e_sim(a_txt[0], a_txt[1]):
        print("Maricea este simetrica.")
    else:
        print("Matricea nu este simetrica.")

    print("\nCalculez valorii proprii pentru matricea din fisier...")
    metoda_puterii(a_txt[0], a_txt[1])

    print("\nCalculez valorii proprii pentru matricea generata aleator...")
    metoda_puterii(n, M)

    print("\nSingular Value Decomposition")
    svd()


if __name__ == "__main__":
    main()