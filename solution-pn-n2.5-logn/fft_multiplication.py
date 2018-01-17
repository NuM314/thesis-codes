import numpy as np
from numpy.fft import fft, rfft, ifft, irfft
import gmpy

def is_prime(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def find_next_prime(n):
    while True:
        n += 1
        if is_prime(n):
            return n

primes_list = []

def get_primes(bound):
    global primes_list
    pos = 0
    cur_mult = 1
    last_num = 1000000000
    while cur_mult <= bound or pos == 0:
        if pos >= len(primes_list):
            primes_list.append(find_next_prime(last_num))
        last_num = primes_list[pos]
        cur_mult *= last_num
        pos += 1
    return primes_list[:pos]

def multiply_fft(v1, v2, real=False):
    N = 1
    while N < len(v1):
        N *= 2
    N *= 2
    if real:
        f1 = rfft(v1, n=N)
        f2 = rfft(v2, n=N)
    else:
        f1 = fft(v1, n=N)
        f2 = fft(v2, n=N)
    tmp_res = f1 * f2

    if real:
        mult_res = irfft(tmp_res, n=N)
    else:
        mult_res = ifft(tmp_res, n=N)

    result = mult_res[:len(v1) + len(v2)]
    assert len(result) == len(v1) + len(v2)
    return result

def multiply_1d_modulo(v1, v2, m):
    b = int(np.sqrt(m)) + 1
    t1 = np.array([x % m for x in v1])
    t2 = np.array([x % m for x in v2])

    t11 = np.floor_divide(t1, b)
    t12 = np.mod(t1, b)

    a1 = t11 * 1j + t12

    t21 = np.floor_divide(t2, b)
    t22 = np.mod(t2, b)

    a2 = t21 * 1j + t22

    r = multiply_fft(a1, a2)

    tmp = multiply_fft(t11, t21, True)

    res = np.mod(np.floor(r.imag + 0.5).astype(np.int), m) * b + np.mod(np.floor(r.real + 0.5).astype(np.int), m) + np.mod(np.floor(tmp.real + 0.5).astype(np.int), m) * (b * b + 1)
    res = np.mod(res, m)
    res = [np.asscalar(x) for x in res]

    return res

def multiply_1d(v1, v2):
    assert len(v1) == len(v2)
    assert type(v1[0] == int)
    assert type(v2[0] == int)

    bound = (max(v1) * max(v2)) * (1 + len(v1))

    primes = get_primes(bound)
    modulo_results = []
    for p in primes:
        modulo_results.append(multiply_1d_modulo(v1, v2, p))

    if len(primes) == 1:
        return modulo_results[0]

    total_product = 1
    for p in primes:
        total_product *= p
    coeffs = []
    for p in primes:
        rest = total_product // p
        cur_coeff = rest * gmpy.invert(rest % p, p)
        coeffs.append(cur_coeff)

    result = []
    for i in range(len(modulo_results[0])):
        cur_res = sum([coeffs[j] * modulo_results[j][i] for j in range(len(coeffs))])
        cur_res %= total_product
        result.append(int(cur_res))
    return result
