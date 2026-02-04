import random
import sys
from math import ceil
from time import process_time_ns

from shamirsSecretSharing import createShares, reconstructSecret
from sieveOfEratosthenes import sieveOfEratosthenes

messageSize = 1764

p = sieveOfEratosthenes(messageSize)[-1]

noTrustees = int(sys.argv[2])
thresholdTrustees = ceil(noTrustees / 2)
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


def trusteeFuncSetGen(functionSet):
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
    functionSets = [
        genFunctionSet(functionSetSize, messageSize) for _ in range(noTrustees)
    ]
    prelimSets = [trusteeFuncSetGen(functionSets[i]) for i in range(noTrustees)]

    trusteeFunctionSets = {}

    for i in range(noTrustees):
        trusteeFunctionSets[i] = {}
        for j in range(len(prelimSets)):
            trusteeFunctionSets[i][j] = prelimSets[j][i]

    # Signature Generation

    partSigSets = {}
    cumuSigTime = 0
    trusteePartialSignatures = {}
    for i in range(noTrustees):
        trusteePartialSignatures[i] = {}
        set = trusteeFunctionSets[i]
        sig_start_time = process_time_ns()
        for t in range(noTrustees):
            signature = []
            for function in set[t]:
                signature.append(
                    (
                        function[0],
                        (function[1][0] * messageSize + function[1][1]) % p,
                    )
                )
            trusteePartialSignatures[i][t] = signature
        sig_end_time = process_time_ns()
        cumuSigTime += sig_end_time - sig_start_time

    # print(cumuSigTime, end="\n\n")

    # Signature Verification - Assume Signature Acceptance Parameter Δ = 1 for worst case scenario

    verificationSet = [
        [
            functionSets[i].pop(random.randint(0, len(functionSets[i]) - 1))
            for _ in range(noRecipients * k)
        ]
        for i in range(noTrustees)
    ]

    indeces = [
        [verificationSet[j][i][0] for j in range(len(verificationSet))]
        for i in range(noRecipients * k)
    ]

    ver_start_time = process_time_ns()

    compA = [
        sum([verificationSet[j][i][1][0] for j in range(len(verificationSet))])
        for i in range(noRecipients * k)
    ]

    compB = [
        sum([verificationSet[j][i][1][1] for j in range(len(verificationSet))])
        for i in range(noRecipients * k)
    ]

    combinedFuncs = [
        (
            indeces[i],
            (
                compA[i],
                compB[i],
            ),
        )
        for i in range(noRecipients * k)
    ]

    reconstructPartSig = {}
    for i in range(noTrustees):
        reconstructPartSig[i] = [
            (
                k,
                reconstructSecret(
                    [
                        (j + 1, trusteePartialSignatures[j][i][k][1])
                        for j in range(thresholdTrustees)
                    ]
                )
                % p,
            )
            for k in range((noRecipients**2) * k)
        ]

    signature = [
        (
            indeces[i],
            sum([reconstructPartSig[j][indeces[i][j]][1] for j in range(0, noTrustees)])
            % p,
        )
        for i in range(noRecipients * k)
    ]

    verificationTags = []
    verifiedTags = 0
    for function in combinedFuncs:
        verificationTags.append(
            (function[0], (function[1][0] * messageSize + function[1][1]) % p)
        )
    for tag in verificationTags:
        if tag in signature:
            verifiedTags += 1
    ver_end_time = process_time_ns()
    """if verifiedTags == noRecipients * k:
        print(f"{ver_end_time - ver_start_time}", end="\n\n")"""
    with open(
        f"./data/signingTimes_{noTrustees}Trustee_{noRecipients}Recip.csv", "a"
    ) as f:
        f.write(f"{sig_end_time - sig_start_time}\n")
    with open(
        f"./data/verificationTimes_{noTrustees}Trustee_{noRecipients}Recip.csv",
        "a",
    ) as f:
        f.write(f"{ver_end_time - ver_start_time}\n")
