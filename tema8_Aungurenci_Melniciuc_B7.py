import random
import math
import cmath

EPSILON = 10**-10


def muller(polynom, k_max):
    A = max(polynom[1:])
    R = (abs(polynom[0]) + A) / abs(polynom[0])

    x0 = float("{0:.2f}".format(random.uniform(-R, R)))
    x1 = float("{0:.2f}".format(random.uniform(-R, R)))
    x2 = float("{0:.2f}".format(random.uniform(-R, R)))

    h0 = x1 - x0
    h1 = x2 - x1

    try:
        delta_0 = (horner(polynom, x1) - horner(polynom, x0)) / h0
        delta_1 = (horner(polynom, x2) - horner(polynom, x1)) / h1
    except:
        return muller(polynom, k_max)

    k = 3

    try:
        a = (delta_1 - delta_0) / (h1 + h0)
    except:
        return muller(polynom, k_max)

    b = a * h1 + delta_1
    c = horner(polynom, x2)

    if b ** 2 - 4 * a * c < 0:
        return muller(polynom, k_max)

    if abs(max(b + math.sqrt(b ** 2 - 4 * a * c), b - math.sqrt(b ** 2 - 4 * a * c))) < EPSILON:
        return muller(polynom, k_max)

    delta_x = 2 * c / (max(b + math.sqrt(b ** 2 - 4 * a * c), b - math.sqrt(b ** 2 - 4 * a * c)))
    x3 = x2 - delta_x
    k += 1
    x0 = x1
    x1 = x2
    x2 = x3

    while abs(delta_x) >= EPSILON and k <= k_max and abs(delta_x) <= 10 ** 8:
        h0 = x1 - x0
        h1 = x2 - x1

        try:
            delta_0 = (horner(polynom, x1) - horner(polynom, x0)) / h0
            delta_1 = (horner(polynom, x2) - horner(polynom, x1)) / h1
        except:
            return muller(polynom, k_max)

        try:
            a = (delta_1 - delta_0) / (h1 + h0)
        except:
            return muller(polynom, k_max)

        b = a * h1 + delta_1
        c = horner(polynom, x2)

        if b ** 2 - 4 * a * c < 0:
            return muller(polynom, k_max)

        if abs(max(b + math.sqrt(b ** 2 - 4 * a * c), b - math.sqrt(b ** 2 - 4 * a * c))) < EPSILON:
            return muller(polynom, k_max)

        delta_x = 2 * c / (max(b + math.sqrt(b ** 2 - 4 * a * c), b - math.sqrt(b ** 2 - 4 * a * c)))
        x3 = x2 - delta_x
        k += 1
        x0 = x1
        x1 = x2
        x2 = x3

    if abs(delta_x) < EPSILON:
        return float("{0:.15f}".format(x3))
    else:
        return "Divergenta..."


def horner(polynom, x):
    n = len(polynom)
    result = float(polynom[0])
    for i in range(1, n):
        result = result * x + float(polynom[i])
    return result


def secant_method(f, k_max, v, derivative_method):
    h = 10 ** -5

    x0 = float("{0:.2f}".format(random.uniform(-v, v)))
    x1 = float("{0:.2f}".format(random.uniform(-v, v)))
    x = x1

    if derivative_method == "G1":
        g_x1 = (3 * horner(f, x) - 4 * horner(f, x - h) + horner(f, x - 2 * h)) / (2 * h)
        g_x0 = (3 * horner(f, x0) - 4 * horner(f, x0 - h) + horner(f, x0 - 2 * h)) / (2 * h)
    elif derivative_method == "G2":
        g_x1 = (- horner(f, x + 2 * h) + 8 * horner(f, x + h) - 8 * horner(f, x - h) + horner(f, x - 2 * h)) / (12 * h)
        g_x0 = (- horner(f, x0 + 2 * h) + 8 * horner(f, x0 + h) - 8 * horner(f, x0 - h) + horner(f, x0 - 2 * h)) / (12 * h)

    while (g_x1 - g_x0) == 0:
        x0 = float("{0:.2f}".format(random.uniform(-v, v)))
        x1 = float("{0:.2f}".format(random.uniform(-v, v)))
        x = x1
        if derivative_method == "G1":
            g_x1 = (3 * horner(f, x) - 4 * horner(f, x - h) + horner(f, x - 2 * h)) / (2 * h)
            g_x0 = (3 * horner(f, x0) - 4 * horner(f, x0 - h) + horner(f, x0 - 2 * h)) / (2 * h)
        elif derivative_method == "G2":
            g_x1 = (- horner(f, x + 2 * h) + 8 * horner(f, x + h) - 8 * horner(f, x - h) + horner(f, x - 2 * h)) / (12 * h)
            g_x0 = (- horner(f, x0 + 2 * h) + 8 * horner(f, x0 + h) - 8 * horner(f, x0 - h) + horner(f, x0 - 2 * h)) / (12 * h)

    delta_x = (x - x0) * g_x1 / (g_x1 - g_x0)

    if (g_x1 - g_x0) >= -EPSILON and (g_x1 - g_x0) <=EPSILON:
        delta_x = 10 ** -5
    x = x - delta_x

    k = 2

    while abs(delta_x) >= EPSILON and k <= k_max and abs(delta_x) <= 10 ** 8:
        if derivative_method == "G1":
            g_x1 = (3 * horner(f, x) - 4 * horner(f, x - h) + horner(f, x - 2 * h)) / (2 * h)
            g_x0 = (3 * horner(f, x0) - 4 * horner(f, x0 - h) + horner(f, x0 - 2 * h)) / (2 * h)
        elif derivative_method == "G2":
            g_x1 = (- horner(f, x + 2 * h) + 8 * horner(f, x + h) - 8 * horner(f, x - h) + horner(f, x - 2 * h)) / (12 * h)
            g_x0 = (- horner(f, x0 + 2 * h) + 8 * horner(f, x0 + h) - 8 * horner(f, x0 - h) + horner(f, x0 - 2 * h)) / (12 * h)

        delta_x = (x1 - x0) * g_x1 / (g_x1 - g_x0)
        if (g_x1 - g_x0) >= -EPSILON and (g_x1 - g_x0) <= EPSILON:
            delta_x = 10 ** -5
        x = x - delta_x

        k += 1

    if abs(delta_x) < EPSILON:
        F = (- horner(f, x + 2 * h) + 16 * horner(f, x + h) - 30 * horner(f, x) +16 * horner(f, x - h) - horner(f, x - 2 * h)) / (12 * h ** 2)
        if F > 0:
            return float("{0:.8f}".format(x))
        else:
            return secant_method(f, k_max, v, derivative_method)
    else:
        return "Divergenta"


def main():
    polynom = [1, -6, 11, -6]
    k_max = 1000
    roots = []
    i = 0
    while i < k_max:
        root = muller(polynom, k_max)
        if not isinstance(root, str):
            roots.append(root)
        i += 1

    file_roots = []
    for v1 in roots:
        duplicate = False
        for i, v2 in enumerate(file_roots):
            if abs(v1 - v2) <= EPSILON:
                duplicate = True
                break

        if not duplicate:
            file_roots.append(v1)

    print("Radacinile polinomului gasite cu metoda Muller:", file_roots)

    file_object = open("radacini_muller.txt", "w")
    for i in file_roots:
        file_object.write(str(i))
        file_object.write("\n")
    file_object.close()

    f = [1, -6, 13, -12, 4]
    minim = []
    i = 0
    while i < 100:
        m = secant_method(f, k_max, 2, "G1")
        if not isinstance(m, str) and m not in minim:
            minim.append(m)
        i += 1

    print("\nPuncte de minim gasite folosind prima metoda de aproximare a derivatei:", minim)

    minim = []
    i = 0
    while i < 100:
        m = secant_method(f, k_max, 2, "G2")
        if not isinstance(m, str) and m not in minim:
            minim.append(m)
        i += 1

    print("\nPuncte de minim gasite folosind a doua metoda de aproximare a derivatei:", minim)


if __name__ == "__main__":
    main()