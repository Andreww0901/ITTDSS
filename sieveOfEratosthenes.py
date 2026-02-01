from math import sqrt, ceil
from typing import List

def sieveOfEratosthenes(N: int) -> List[int]:
    primes = [1]
    i = 1
    while primes[-1] < N:
        numbers = list(range(2, N+i))
        x = 2
        primes = numbers
        while x <= ceil(sqrt(N)):
            for num in numbers:
                if num % x == 0 and num != x:
                    primes.remove(num)
            x += 1
        i += 1
    return primes
