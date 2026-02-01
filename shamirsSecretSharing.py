import random
from typing import List, Tuple

def generateCoefficients(secret: int, threshold: int, p: int) -> List[int]:
    coefficients = [secret]
    for _ in range(threshold - 1):
        coefficients.append(random.randint(0, p))
    return coefficients

def createShares(
    secret: int, total_shares: int, threshold: int, p: int
) -> List[Tuple[int, int]]:
    coefficients = generateCoefficients(secret, threshold, p)
    shares = []
    for x in range(1, total_shares + 1):
        y = sum(coeff * (x**exp) for exp, coeff in enumerate(coefficients))
        shares.append((x, y))
    return shares

def basisPolynomial(j: int, x: int, x_s: List[int]) -> int:
    num = 1
    den = 1
    for m in range(len(x_s)):
        if m != j:
            num *= x - x_s[m]
            den *= x_s[j] - x_s[m]
    return num // den

def lagrangeInterpolation(x: int, x_s: List[int], y_s: List[int]) -> int:
    result = 0
    for j in range(len(y_s)):
        result += y_s[j] * basisPolynomial(j, x, x_s)
    return result

def reconstructSecret(shares: List[Tuple[int, int]]) -> int:
    x_s, y_s = zip(*shares)
    return lagrangeInterpolation(0, x_s, y_s)
