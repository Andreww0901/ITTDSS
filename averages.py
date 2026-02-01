from math import sqrt

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams

rcParams["font.family"] = "Times New Roman"

if __name__ == "__main__":
    # Signing Times Averages with error
    colours = ["#ca0020", "#f4a582", "#92c5de", "#0571b0"]
    fig, ax = plt.subplots()
    for noTrustee in range(2, 6):
        averageList = []
        stdDevList = []
        for noRecipient in range(1, 21):
            data = pd.read_csv(
                f"./RPIDealerData/signingTimes_{noTrustee}Trustee_{noRecipient}Recip.csv",
                header=None,
            )
            data = data[:200]
            data = data.div(1000000)
            avg = (sum(list(data[0]))) / 200
            averageList.append(avg)
            print(
                f"Average Signing time for {noTrustee} Trustees & {noRecipient} Recipients: {avg}"
            )
            stdDev = sqrt((sum([(data[0][i] - avg) ** 2 for i in range(200)])) / 200)
            stdDevList.append(stdDev)
            print(
                f"Standard Deviation Signing time for {noTrustee} Trustees & {noRecipient} Recipients: {stdDev}\n"
            )
        ax.errorbar(
            range(1, 21),
            averageList,
            stdDevList,
            capsize=4,
            label=f"{noTrustee} Trustees",
            marker="x",
            linestyle="--",
            linewidth=0.5,
            color=colours.pop(0),
        )
    ax.set_xlabel("No. Recipients")
    ax.set_ylabel("Signing Time (ms)")
    ax.legend()
    plt.title("Signature Computation Time")
    plt.savefig("./plots/RPISigComputationPlot200.svg", format="svg")

    # Verification Times Averages with error
    colours = ["#ca0020", "#f4a582", "#92c5de", "#0571b0"]
    fig, ax = plt.subplots()
    for noTrustee in range(2, 6):
        averageList = []
        stdDevList = []
        for noRecipient in range(1, 21):
            data = pd.read_csv(
                f"./RPIDealerData/verificationTimes_{noTrustee}Trustee_{noRecipient}Recip.csv",
                header=None,
            )
            data = data[:200]
            data = data.div(1000000)
            avg = (sum(list(data[0]))) / 200
            averageList.append(avg)
            print(
                f"Average Verification time for {noTrustee} Trustees & {noRecipient} Recipients: {avg}"
            )
            stdDev = sqrt((sum([(data[0][i] - avg) ** 2 for i in range(200)])) / 200)
            stdDevList.append(stdDev)
            print(
                f"Standard Deviation Verification time for {noTrustee} Trustees & {noRecipient} Recipients: {stdDev}\n"
            )
        ax.errorbar(
            range(1, 21),
            averageList,
            stdDevList,
            capsize=4,
            label=f"{noTrustee} Trustees",
            marker="x",
            linestyle="--",
            linewidth=0.5,
            color=colours.pop(0),
        )
    ax.set_xlabel("No. Recipients")
    ax.set_ylabel("Verification Time (ms)")
    ax.legend()
    plt.title("Signature Verification Time")
    plt.savefig("./plots/RPIVerificationPlot200.svg", format="svg")
