from math import sqrt

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import rcParams

rcParams["font.family"] = "Times New Roman"


def signingPlots(filepath, proto, device):
    colours = ["#ca0020", "#f4a582", "#92c5de", "#0571b0"]
    fig, ax = plt.subplots()
    for noTrustee in range(2, 6):
        averageList = []
        stdDevList = []
        for noRecipient in range(1, 21):
            data = pd.read_csv(
                f"./{filepath}/signingTimes_{noTrustee}Trustee_{noRecipient}Recip.csv",
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
    ax.set_axisbelow(True)
    ax.xaxis.grid(color="gray", linestyle="dashed", alpha=0.25)
    ax.yaxis.grid(color="gray", linestyle="dashed", alpha=0.25)
    ax.legend()
    plt.title(f"{proto} - Signature Computation Time - {device}")
    plt.savefig(f"./plots/{filepath}_SignatureComputationPlot.svg", format="svg")


def verificationPlots(filepath, proto, device):
    colours = ["#ca0020", "#f4a582", "#92c5de", "#0571b0"]
    fig, ax = plt.subplots()
    for noTrustee in range(2, 6):
        averageList = []
        stdDevList = []
        for noRecipient in range(1, 21):
            data = pd.read_csv(
                f"./{filepath}/verificationTimes_{noTrustee}Trustee_{noRecipient}Recip.csv",
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
    ax.set_axisbelow(True)
    ax.xaxis.grid(color="gray", linestyle="dashed", alpha=0.25)
    ax.yaxis.grid(color="gray", linestyle="dashed", alpha=0.25)
    ax.legend()
    plt.title(f"{proto} - Signature Verification Time - {device}")
    plt.savefig(f"./plots/{filepath}_VerificationPlot.svg", format="svg")


if __name__ == "__main__":
    signingPlots("MACDealerData", "Dealer", "2025 M5 MacBook Pro")
    verificationPlots("MACDealerData", "Dealer", "2025 M5 MacBook Pro")
    signingPlots("MACNonDealerData", "Non-Dealer", "2025 M5 MacBook Pro")
    verificationPlots("MACNonDealerData", "Non-Dealer", "2025 M5 MacBook Pro")
    signingPlots("RPIDealerData", "Dealer", "Raspberry Pi 4 (4GB)")
    verificationPlots("RPIDealerData", "Dealer", "Raspberry Pi 4 (4GB)")
    signingPlots("RPINonDealerData", "Non-Dealer", "Raspberry Pi 4 (4GB)")
    verificationPlots("RPINonDealerData", "Non-Dealer", "Raspberry Pi 4 (4GB)")
