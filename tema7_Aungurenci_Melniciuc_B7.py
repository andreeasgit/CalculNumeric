import math
import numpy
import matplotlib.pyplot as plt

def read_input(filename):
    file_object = open(filename, "r")
    n = int(file_object.readline())
    file_object.readline()
    x0 = float(file_object.readline())
    file_object.readline()
    xn = float(file_object.readline())
    file_object.close()

    return n, x0, xn


def read_least_squares_input(filename):
    file_object = open(filename, "r")
    x = [float(i) for i in file_object.readline().split()]
    file_object.readline()
    y = [float(i) for i in file_object.readline().split()]

    file_object.close()
    return x, y


def horner(polynom, x):
    n = len(polynom)
    result = float(polynom[0])
    for i in range(1, n):
        result = result * x + float(polynom[i])
    return result


def delta_f(f, x, h, k):
    if k == 1:
        return horner(f, x+h) - horner(f, x)
    else:
        return delta_f(f, x+h, h, k-1) - delta_f(f, x, h, k-1)


def progressive_newton(f, n, x0, xn, x):

    h = (xn - x0) / n
    # valorile xi, i in (1,n-1)
    nodes = []
    # valorile yi, i in (0, n)
    values = []
    for i in range(1, n):
        xi = x0 + i*h
        nodes.append(xi)

    for i in range(0, n+1):
        yi = horner(f, i)
        values.append(yi)


    t = (x - x0) / h
    ln = values[0] + delta_f(f, x0, h, 1) * t
    p = t
    for k in range(2, n+1):
        delta = delta_f(f, x0, h, k)
        p *= (t - k + 1)
        ln += delta * (p / math.factorial(k))

    return ln


def sk(k, t):
    if k == 1:
        return t
    else:
        return sk(k-1, t) * ((t - k + 1) / k)


def Aitken (f, n, x0, xn, x):
    n += 1
    h = (xn - x0) / n
    # valorile xi, i in (1,n-1)
    nodes = []
    # valorile yi, i in (0, n)
    values = []
    for i in range(1, n):
        xi = x0 + i * h
        nodes.append(xi)

    for i in range(0, n + 1):
        yi = horner(f, i)
        values.append(yi)

    t = (x - x0) / h

    y = [0] * ((n * (n+1))//2)

    i, j = 0, 0
    m = n
    while i<((n * (n+1))//2):
        y[i] = values [j]
        i += m
        m -= 1
        j += 1

    k = 1
    b = n-1
    while k < n:
        j = k
        a = n
        d = b
        while d > 0:
            y[j] = y[j-1+a] - y [j-1]
            j = j+a
            a = a-1
            d = d-1

        b-=1
        k+=1

    i = n
    m = n-1
    p = 0
    while m >= 1:
        y.pop(i-p)
        i += m
        m -= 1
        p += 1

    y = y[0: n]
    ln = y[0]
    for i in range (1, n):
        ln += y[i]* sk(i, t)

    return ln


def least_square_interpolation(x, y, m):
    print ("Metoda celor mai mici patrate")

    B = [[0]*(m+1) for _ in range(len(x))]

    for i in range(0, len(x)):
        B[i][0] = 1

    for i in range(0, len(x)):
        for j in range(1, m+1):
            B[i][j] = (x[i] ** j)

    for i in range(0, len(y)):
        y[i] = [y[i]]
    B = numpy.array(B)
    y = numpy.array(y)

    a = numpy.linalg.solve(numpy.matmul(B.transpose(), B), numpy.matmul(B.transpose(), y))
    #a = numpy.linalg.lstsq(B, y, rcond=None)

    b = []
    for i in a:
        b.append(i[0])

    return b[::-1]


def show_graphic(x, y, f, Sn, k, title):
    copy_x, copy_y = x, y

    copy_x.append(k)
    copy_y.append(horner(f, k))
    X = list(zip(copy_x, copy_y))
    X.sort(key=lambda x: x[0])

    copy_x = [i[0] for i in X]
    copy_y = [i[1] for i in X]

    plt.plot(copy_x, copy_y, "blue")

    copy_x = x
    copy_x.append(k)
    copy_y = []
    for i in x:
        copy_y.append(horner(Sn, i))

    X = list(zip(copy_x, copy_y))
    X.sort(key=lambda x: x[0])

    copy_x = [i[0] for i in X]
    copy_y = [i[1] for i in X]

    plt.plot(copy_x, copy_y, "r-")

    plt.title(title)
    plt.ylabel('f')
    plt.xlabel('x')
    plt.show()


def show_graphic2(x, y, f, title):

    plt.plot(x, y, "r-")

    y = []
    for i in x:
        y.append(horner(f, i))

    plt.plot(x, y, "blue")

    plt.title(title)
    plt.ylabel('f')
    plt.xlabel('x')
    plt.show()


def main():
    k = 1.5
    f = [1, -12, 30, 0, 12]

    print("Formula Newton progresiva pe noduri echidistante")
    n, x0, xn = read_input("input.txt")
    ln = progressive_newton(f, n, x0, xn, k)

    print("Ln(x) =", ln)
    print("|Ln(x) - f(x)| =", abs(ln - horner(f, k)))
    h = (xn - x0) / n
    # valorile xi, i in (1,n-1)
    nodes = [x0]

    for i in range(1, n):
        xi = x0 + i * h
        nodes.append(xi)
    nodes.append(xn)

    # valorile yi, i in (0, n)
    values = []
    for i in nodes:
        values.append(progressive_newton(f, n, x0, xn, i))

    show_graphic2(nodes, values, f, "Formula Newton progresiva pe noduri echidistante")

    print()
    print("Schema lui Aitken")
    ln = Aitken(f, n, x0, xn, k)
    print("Ln(x) =", ln)
    print("|Ln(x) - f(x)| =", abs(ln - horner(f, k)))

    # valorile yi, i in (0, n)
    values = []
    for i in nodes:
        values.append(Aitken(f, n, x0, xn, i))

    show_graphic2(nodes, values, f, "Schema lui Aitken")
    print()

    k = 1.5
    x, y = read_least_squares_input("least_squares_input.txt")
    Sn = least_square_interpolation(x, y, 4)
    for i in range(0, len(y)):
        y[i] = y[i][0]

    f = [1, -12, 30, 0, 12]
    print("Sn:", Sn)
    print("Sn(x) =", horner(Sn, k))
    print("|Sn(x) - f(x)| =", abs(horner(Sn, k) - horner(f, k)))

    show_graphic(x, y, f, Sn, k, "Metoda celor mai mici patrate")


if __name__ == "__main__":
    main()