from fractions import gcd
from math import factorial, sqrt
from fft_multiplication import multiply_1d

def lcm(a, b):
    return a // gcd(a, b) * b

def generate_partitions(n, I=1):
    yield (n,)
    for i in range(I, n // 2 + 1):
        for p in generate_partitions(n - i, i):
            yield (i,) + p

def calculate_comb(n):
    comb = [[0] * (n + 1) for i in range(n + 1)]
    for i in range(n + 1):
        comb[i][0] = 1
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            comb[i][j] = comb[i - 1][j] + comb[i - 1][j - 1]
    return comb

def calculate_t(partition):
    n = sum(partition)
    res_vector = [[0] * (n + 1) for i in range(n + 1)]
    comb = calculate_comb(n)
    # O(n) iterations
    for i in range(1, n + 1):
        dp = [0] * (n + 1)
        dp[0] = 1
        cnt = 0
        # O(sqrt(n)) real iterations as only unique summands are considered
        for j in range(len(partition)):
            cnt += 1
            if not (j == len(partition) - 1 or partition[j] != partition[j + 1]):
                continue
            gc = gcd(partition[j], i)
            lc = lcm(partition[j], i)
            gc *= cnt
            cnt = 0

            poly = [0] * (n + 1)
            for cn in range(gc + 1):
                if cn * lc > n:
                    break
                poly[cn * lc] = comb[gc][cn]

            # O(mul(n))
            tmp = multiply_1d(dp, poly) # bottleneck line. overall complexity: O(p(n) n^2.5 log(n))
            dp = tmp[:n + 1]
        res_vector[i] = dp
    return res_vector

def multiply_2d(v1, v2):
    assert len(v1) == len(v2)
    assert len(v1[0]) == len(v2[0])
    assert len(v1) == len(v1[0])

    n = len(v1)
    N = n + n
    t1 = [0] * (N * N)
    t2 = [0] * (N * N)
    for i in range(n):
        for j in range(n):
            t1[n * N + i * N + n + j] = v1[i][j]
            t2[i * N + j] = v2[i][j]

    mult = multiply_1d(t1, t2)
    res = [[0] * n for i in range(n)]
    for i in range(n):
        for j in range(n):
            res[i][j] = mult[n * N + i * N + n + j]
    return res

def calculate_F(partition):
    n = sum(partition)
    t = calculate_t(partition)

    F = [[0] * (n + 1) for i in range(n + 1)]
    F[0][0] = 1
    add = int(sqrt(n)) + 1

    # O(sqrt(n)) iterations
    for i in range(1, n + 1, add):
        # O(mul(n^2))
        tmp = multiply_2d(F, t) # bottleneck line. overall complexity: O(p(n) n^2.5 log(n))

        # O(sqrt(n)) iterations
        for curi in range(i, min(i + add, n + 1)):
            # O(sqrt(n)) iterations
            for k in range(i, curi):
                # O(mul(n))
                poly = multiply_1d(F[k], t[curi - k]) # bottleneck line. overall complexity: O(p(n) n^2.5 log(n))
                # O(n) iterations
                for j in range(n + 1):
                    tmp[curi][j] = tmp[curi][j] + poly[j]
            for j in range(n + 1):
                F[curi][j] = tmp[curi][j] // curi
    return F

def partition_counts(p, n):
    result = [0] * (n + 1)
    for e in p:
        result[e] += 1
    return result

def calculate_partition_multiplier(p):
    n = sum(p)
    p_counts = partition_counts(p, n)
    result = factorial(n)
    for i, c_i in enumerate(p_counts):
        result //= factorial(c_i) * (i ** c_i)
    return result

def calculate_answers(n):
    answers = [0] * (n + 1)
    num_partitions = 0
    for partition in generate_partitions(n):
        num_partitions += 1
        F = calculate_F(partition)
        mult = calculate_partition_multiplier(partition)
        for i in range(n + 1):
            answers[i] += F[n][i] * mult

    for i in range(n + 1):
        assert answers[i] % factorial(n) == 0
        answers[i] //= factorial(n)
    return answers[1:]

def main():
    n = int(input("Enter n: "))

    for i, ans in enumerate(calculate_answers(n)):
        print("a(%d) = %d" % (i + 1, ans))

if __name__ == '__main__':
    main()
