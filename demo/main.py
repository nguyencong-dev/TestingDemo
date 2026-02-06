import math
def isPrime(n):
    if n < 2:
        raise ValueError("invalid error")
    else:
        for i in range(2, math.isqrt(n) + 1):
            if n % i == 0:
                return False

    return True