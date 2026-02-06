import math
def isPrime(n):
    if n < 2:
        raise ValueError("invalid error")
    else:
        for i in range(math.isqrt(n)):
            if n % i == 0:
                return False

    return True