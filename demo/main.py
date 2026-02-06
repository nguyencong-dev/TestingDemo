import math
def isPrime(n):
    if n < 2:
       raise ValueError("Invalid Error")
    else:
        for i in range(2, math.isqrt(n)):
            if n % i == 0:
                return False

    return True