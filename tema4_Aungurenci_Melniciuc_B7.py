from decimal import *
import operator


EPSILON = 10**-int(open("EPSILON.txt", "r").read())

getcontext().prec = 16

def read_info(file_name):
    '''
        citeste din fisierul dat ca parametru dimensiunea datelor (n), elementele vectorului b
        si elementele a_ij != 0 din matricea rara A (matrice)
        returneaza un tuplu (n, b, matrice)
    '''

    file_obj = open(file_name, "r")
    n = int(file_obj.readline()) #dimensiunea
    file_obj.readline()

    b = [] #vectorul b
    for i in range (int(n)):
        x = file_obj.readline().replace('\n','')
        b.append(Decimal(x))


    file_obj.readline()

    matrice = [] #matricea

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
                        if e [1] == element[1]:
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

    return (n, b, matrice)

n, b, a = read_info("m_rar_2018_5.txt")

def diag(a):
    for i in range(0, n - 1):
        ok = 0
        # print (a[i])
        for rsub in a[i]:
            # print (rsub)
            if (i == rsub[1]):
                ok = 1
                break
        if ok == 0:
            return False
    return True


def sol(b, a):
    file_obj = open("rezultat.txt", "w")
    c = 20
    xc = [0]
    xp = [0]
    for i in range(1, n + 1):
        xc.append(0)
    dx = 0
    k = 0
    aii = 0
    '''for i in range(0,n):
        suma1=0
        for j in range(0,i-1):
            for element in a[i]:
                print(element)
                if element[1]==j:
                    suma1+=element[0]*xc[j]
        suma2=0
        aii=0
        for element in a[i]:
            if element[1]==i:
                aii=element[0]
        xc.append((b[i]-(suma1)-(suma2))//aii)#a[i][i]'''
    while ((dx <= 10**8 and dx>=EPSILON) or k==0) and k <= 10000:
        xp = xc
        # print(xc)
        xc = [0]
        for i in range(0, n):
            suma1 = 0
            # rprint('s1')
            for j in range(0, i):
                for element in a[i]:
                    # print(element)
                    if element[1] == j:
                        suma1 += element[0] * xc[j + 1]
                    # print (str(element[0])+'*'+str(xc[j+1])+'+\n')
            suma2 = 0
            # print('s2')
            for j in range(i + 1, n):
                for element in a[i]:
                    if element[1] == j:
                        suma2 += element[0] * xp[j + 1]
                    # print (str(element[0])+'*'+str(xp[j+1])+'+\n')
            aii = 0
            for element in a[i]:
                if element[1] == i:
                    aii = element[0]
            # print('===========\n'+str(b[i])+'-'+str(suma1)+'-'+str(suma2)+'/'+str(aii)+'\n===========')
            xc.append((b[i] - (suma1) - (suma2)) / aii)  # a[i][i]
        dx = 0
        # dx=abs(xp-xc)
        diferenta = [0]
        for element in range(1, n + 1):
            diferenta.append(abs(xp[element] - xc[element]))

        dx = max(diferenta[1:])
        k = k + 1

    print("Numar iteratii efectuate:", k)
    for i in range(1, n + 1):
        linie = str(xc[i]) + '\n'
        # print(xc[i])
        file_obj.write(linie)
    file_obj.close()
    return xc


def aproape0(dx, c):
    for i in dx:
        if i > EPSILON * c and i<10**8:
            return True
    return False


def matrix_prod(A, B, file_name_result):
    '''
        primeste ca parametri doua matrici rare A si B
        scrie produsul celor doua matrici in fisierul "rezultat_aorib.txt"
    '''

    dimensiune_a = len(A)
    dimensiune_b = len(B)

    file_obj = open("b_transpus.txt", "w")

    file_obj.write(str(dimensiune_b) + '\n' + '\n')

    for i in range(0, dimensiune_b):
        file_obj.write(str(i) + '\n')

    file_obj.write('\n')

    f = []
    for index_linie_b, linie_b in enumerate(B):
        for element in linie_b:
            line = [element[0]] + [element[1]] + [index_linie_b]
            f.append(line)

    f.sort(key = operator.itemgetter(1))

    for element in f:
        line = str(element[0]) + ', ' + str(element[1]) + ', ' + str(element[2]) + '\n'
        file_obj.write(line)

    file_obj.close()

    b_transpus = read_info("b_transpus.txt")[2]

    file_obj = open(file_name_result, "w")

    file_obj.write(str(dimensiune_a) + '\n' + '\n')

    for i in range(0, dimensiune_a):
        file_obj.write(str(i) + '\n')

    file_obj.write('\n')

    for index_linie_a, linie_a in enumerate(A):
        for index_linie_b, linie_b in enumerate(b_transpus):
            s = 0
            for element_a in A[index_linie_a]:
                for element_b in b_transpus[index_linie_b]:
                    if (element_a[1] == element_b[1]):
                        s += element_a[0] * element_b[0]

            if s != 0 :
                linie_prod = str(s) + ', ' + str(index_linie_a) + ', ' + str(index_linie_b) + '\n'
                file_obj.write(linie_prod)

    file_obj.close()


def matrix_sub(A,B):
    '''
        primeste ca parametri doua matrici rare A si B
        scrie diferenta celor doua matrici in fisierul "rezultat_axminusb.txt"
    '''

    file_obj = open("rezultat_axminusb.txt","w")

    file_obj.write(str(len(A)) + '\n' + '\n')

    for i in range(0, len(A)):
        file_obj.write(str(i) + '\n')

    file_obj.write('\n')

    for index_linie_a, linie_a in enumerate(A):
         for index_linie_b, linie_b in enumerate(B):
             if index_linie_a == index_linie_b:
                 for element_a in linie_a:
                     s = element_a[0]
                     for element_b in linie_b:
                         if element_a[1] == element_b[1]:
                             s -= element_b[0]
                     linie_suma = str(s) + ', ' + str(index_linie_a) + ', ' + str (element_a[1]) + '\n'
                     file_obj.write(linie_suma)

    file_obj.close()


def main():
    print("Verific daca elementele de pe diagonala principala sunt nenule...")
    if diag(a) == True:
        print("Elementele de pe diagonala principala sunt nenule.")
        print("Calculez solutia sistemului...")
        x_gauss_seidel = sol(b, a)[1:]
        print("Vezi solutia in fisierul \"rezultat.txt\".")

        vector_x = []
        for index_linie,item in enumerate(x_gauss_seidel):
            element = []
            element.append(item)
            element.append(0)
            vector_x.append([element])

        matrix_prod(a, vector_x, "rezultat_aorix.txt")

        vector_b = []
        for index_linie, item in enumerate(b):
            element = []
            element.append(item)
            element.append(0)
            vector_b.append([element])

        a_ori_x = read_info("rezultat_aorix.txt")[2]
        matrix_sub(a_ori_x, vector_b)

        a_ori_x_minus_b = read_info("rezultat_axminusb.txt")[2]

        norma_inifinit = -99999999999999999999999999999999999
        for index_linie, linie in enumerate(a_ori_x_minus_b):
            for element in linie:
                if abs(element[0]) > norma_inifinit:
                    norma_inifinit = element[0]

        print("Norma infint A * x_gs - b:",norma_inifinit)
    else:
        print("Diagonala principala contine elemente nule.")

if __name__ == "__main__":
    main()