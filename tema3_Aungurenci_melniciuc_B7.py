
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

def check_matrix(matrice):
    '''
        primeste ca parametru o matrice memorata economic si verifica daca aceasta are
        cel mult 10 elemente nenule pe fiecare linie
        daca o linie din matrice nu respecta conditia se afiseaza linia
        altfel se afiseaza mesajul: "Matricea are cel mult 10 elemente nenule pe fiecare linie."
    '''

    check = True
    for index, element in enumerate(matrice):
        if len(element) > 10:
            print ("Linia", index, "are mai mult de 10 elemente nenule!")
            print ("Linia", index, ":")
            print(element)
            check = False

    if check == True:
        print("Matricea are cel mult 10 elemente nenule pe fiecare linie.")

def matrix_sum(A,B):
    '''
        primeste ca parametri doua matrici rare A si B
        scrie suma celor doua matrici in fisierul "rezultat_aplusb.txt"
    '''

    file_obj = open("rezultat_aplusb.txt","w")

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
                             s += element_b[0]
                     linie_suma = str(s) + ', ' + str(index_linie_a) + ', ' + str (element_a[1]) + '\n'
                     file_obj.write(linie_suma)

    file_obj.close()



def convert_nr_to_prec (nr, prec):
    '''
        returneaza nr cu prec cifre
    '''

    prec -= 1
    if len(str(nr)) > prec:
        nr = str(nr)[0:prec]
        p = len(nr) - len(nr[0:nr.find('.')]) - 1
        nr = round(float(nr), p-1)

    return Decimal(nr)

def check_result(file_name_result, file_name_correct_result):
    '''
        verifica daca matricea din fisierul "file_name_result" este egala cu cea din "file_name_correct_result"
        returneaza True daca sunt egale, altfel False
    '''

    rezultat_corect = read_info(file_name_correct_result)[2]
    rezultat = read_info(file_name_result)[2]

    for index_linie_a, linie_a in enumerate(rezultat_corect):
         for index_linie_b, linie_b in enumerate(rezultat):
             if index_linie_a == index_linie_b:
                 for element_a in linie_a:
                     for element_b in linie_b:
                        if element_a[1] == element_b[1] and abs(convert_nr_to_prec(element_a[0], 16) - convert_nr_to_prec(element_b[0], 16)) >= EPSILON:
                            print(index_linie_a, element_b[1],element_a[0], element_b[0])
                            return False

    return True


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

def get_vector_coloana(dimensiune):
    vector_coloana = [[]]

    for i in range(dimensiune, 0, -1):
        element = []
        element.append(i)
        element.append(0)
        vector_coloana.insert(dimensiune-i,[element])

    return vector_coloana

def check_ax(file_name_result, b):
    rezultat_aorix = read_info(file_name_result)[2]

    for index_linie, linie in enumerate(rezultat_aorix):
        for element in linie:
            if abs(convert_nr_to_prec(element[0], 16) - convert_nr_to_prec(b[index_linie], 16)) >= EPSILON:
                print(index_linie, b[index_linie], element[0])
                return False

    return True


def main():
    ### citesc matricile din fisier
    a_txt = read_info("a.txt")
    b_txt = read_info("b.txt")
    dimensiune_a = a_txt[0]
    b_a = a_txt[1]
    matrice_a = a_txt[2]

    dimensiune_b = b_txt[0]
    b_b = b_txt[1]
    matrice_b = b_txt[2]


    ### verific daca matricea A are cel mult 10 elemente nenule pe fiecare linie
    print("Verific daca matricea A are cel mult 10 elemente nenule pe fiecare linie...")
    check_matrix(matrice_a)

    print("\n")
    ### verific daca matricea B are cel mult 10 elemente nenule pe fiecare linie
    print("Verific daca matricea B are cel mult 10 elemente nenule pe fiecare linie...")
    check_matrix(matrice_b)

    print("\n")
    
    print("Calculez A + B...")
    matrix_sum(matrice_a, matrice_b)

    print("Vezi rezulatul in fisierul \"rezultat_aplusb.txt\". ")
    print("Verific A + B...")

    check_sum = check_result("rezultat_aplusb.txt", "aplusb.txt")

    if check_sum == True:
        print("Suma matricilor este corecta!\n")
    else:
        print("Suma matricilor este incorecta!\n")

    print("Calculez A * B...")

    matrix_prod(matrice_a, matrice_b, "rezultat_aorib.txt")

    print("Vezi rezulatul in fisierul \"rezultat_aorib.txt\". ")
    print("Verific A * B...")

    check_prod = check_result("rezultat_aorib.txt", "aorib.txt")
    if check_prod == True:
        print("Produsul matricilor este corect!\n")
    else:
        print("Produsul matricilor este incorect!\n")

    print("\nVerific A * x = b...")
    matrix_prod(matrice_a, get_vector_coloana(dimensiune_a), "rezultat_aorix.txt")
    if check_ax("rezultat_aorix.txt", b_a) == True:
        print("A * x = b")
    else:
        print("A * x != b")

    print("Verific B * x = b...")
    matrix_prod(matrice_b, get_vector_coloana(dimensiune_b), "rezultat_borix.txt")
    if check_ax("rezultat_borix.txt", b_b) == True:
        print("B * x = b")
    else:
        print("B * x != b")


if __name__ == '__main__':
    main()