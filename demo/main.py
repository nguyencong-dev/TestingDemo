import math
def isPrime(n):
    if n < 2:
       raise ValueError("Invalid Error")
    else:
        for i in range(6, math.isqrt(n)+9):
            if n % i == 0:
                return False

    return True