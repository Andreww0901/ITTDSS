import random
import sys
from math import floor
from time import process_time_ns

from shamirsSecretSharing import createShares, reconstructSecret
from sieveOfEratosthenes import sieveOfEratosthenes

message = "Newcastle University - School of Computing"
messageSize = len(message) ** 2

p = sieveOfEratosthenes(messageSize)[-1]

noTrustees = int(sys.argv[2])
thresholdTrustees = floor(noTrustees / 2)
noRecipients = int(sys.argv[3])
k = 100

functionSetSize = (noRecipients**2) * k


def genFunctionSet(size, mSize):
    functionSet = set()
    while len(functionSet) < size:
        functionSet.add(
            (
                random.randint(1, mSize),
                random.randint(0, mSize),
            )
        )
    functionSet = list(functionSet)
    return [(i, functionSet[i]) for i in range(len(functionSet))]


def trusteeFuncSetGen():
    trusteeFunctionSets = {}
    for t in range(noTrustees):
        trusteeFunctionSets[t] = []
    for function in functionSet:
        aSecrets = [
            share[1]
            for share in createShares(function[1][0], noTrustees, thresholdTrustees, p)
        ]
        bSecrets = [
            share[1]
            for share in createShares(function[1][1], noTrustees, thresholdTrustees, p)
        ]
        functionSecrets = list(zip(aSecrets, bSecrets))
        for t in range(noTrustees):
            trusteeFunctionSets[t].append((function[0], functionSecrets[t]))
    return trusteeFunctionSets


if __name__ == "__main__":
    # Function Set Creation
    functionSet = genFunctionSet(functionSetSize, messageSize)
    trusteeFunctionSets = trusteeFuncSetGen()

    # Signature Generation
    trusteePartialSignatures = {}
    for t in range(noTrustees):
        signature = []
        sig_start_time = process_time_ns()
        for function in trusteeFunctionSets[t]:
            signature.append(
                (
                    function[0],
                    (function[1][0] * messageSize + function[1][1]) % p,
                )
            )
        sig_end_time = process_time_ns()

        trusteePartialSignatures[t] = signature

    # Signature Verification - Assume Signature Acceptance Parameter Δ = 1 for worst case scenario

    verificationSet = [
        functionSet.pop(random.randint(0, len(functionSet) - 1))
        for _ in range(noRecipients * k)
    ]
    ver_start_time = process_time_ns()
    signature = [
        (
            verificationSet[i][0],
            reconstructSecret(
                [
                    (j + 1, trusteePartialSignatures[j][verificationSet[i][0]][1])
                    for j in range(0, thresholdTrustees)
                ]
            )
            % p,
        )
        for i in range(len(verificationSet))
    ]

    verificationTags = []
    verifiedTags = 0
    for function in verificationSet:
        verificationTags.append(
            (function[0], (function[1][0] * messageSize + function[1][1]) % p)
        )
    for tag in verificationTags:
        if tag in signature:
            verifiedTags += 1
    ver_end_time = process_time_ns()
    with open(
        f"./data/signingTimes_{noTrustees}Trustee_{noRecipients}Recip.csv", "a"
    ) as f:
        f.write(f"{sig_end_time - sig_start_time}\n")
    with open(
        f"./data/verificationTimes_{noTrustees}Trustee_{noRecipients}Recip.csv",
        "a",
    ) as f:
        f.write(f"{ver_end_time - ver_start_time}\n")
