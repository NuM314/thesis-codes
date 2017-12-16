from fractions import gcd
from math import factorial

def lcm(a, b):
    return a // gcd(a, b) * b

def generate_partitions(n, I=1):
    yield (n,)
    for i in range(I, n // 2 + 1):
        for p in generate_partitions(n - i, i):
            yield (i,) + p

def partition_counts(p, n):
    result = [0] * (n + 1)
    for e in p:
        result[e] += 1
    return result

def calculate_t(p, n):
    t = [[0] * (n + 1) for i in range(n + 1)]
    for j in range(1, n + 1):
        g = [[0] * (n + 1) for i in range(len(p) + 1)]
        g[0][0] = 1
        for i in range(1, len(p) + 1):
            l_i = p[i - 1]
            lc = lcm(l_i, j)
            for k in range(n + 1):
                for l in range(n + 1):
                    to_k = k - l * lc
                    if to_k < 0:
                        break
                    g[i][k] += g[i - 1][to_k] * combs[gcds[l_i][j]][l]
        for i in range(0, n + 1):
            t[j][i] = g[len(p)][i]
    return t

def A(n, k):
    return combs[n][k] * factorials[k]

def calculate_f(p, n):
    t = calculate_t(p, n)
    f = [[0] * (n + 1) for i in range(n + 1)]
    f[0][0] = 1
    for i in range(1, n + 1):
        for j in range(n + 1):
            for k in range(1, i + 1):
                for l in range(j + 1):
                    f[i][j] += A(i - 1, k - 1) * f[i - k][j - l] * t[k][l]
    return f

def calculate_partition_multiplier(p, n):
    p_counts = partition_counts(p, n)
    result = factorial(n)
    for i, c_i in enumerate(p_counts):
        result //= factorial(c_i) * (i ** c_i)
    return result

def calculate_answers(n):
    answers = [0] * (n + 1)
    for p in generate_partitions(n):
        f = calculate_f(p, n)
        multiplier = calculate_partition_multiplier(p, n)
        for i in range(n + 1):
            answers[i] += multiplier * f[n][i]
    for i in range(n + 1):
        answers[i] //= factorial(n) * factorial(n)
    return answers[1:]

n = int(input("Enter n: "))

gcds = [[gcd(i, j) for j in range(n + 1)] for i in range(n + 1)]
factorials = [factorial(i) for i in range(n + 1)]
combs = [[1] + [0] * n for i in range(n + 1)]
for i in range(1, n + 1):
    for j in range(1, n + 1):
        combs[i][j] = combs[i - 1][j] + combs[i - 1][j - 1]

for i, ans in enumerate(calculate_answers(n)):
    print("a(%d) = %d" % (i + 1, ans))
