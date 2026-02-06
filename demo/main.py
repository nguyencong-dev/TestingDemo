import math
def isPrime(n):
    if n < 2:
        raise ValueError("invalid error")
    else:
        for i in range(3, math.isqrt(n) + 2):
            if n % i == 0:
                return False

    return True