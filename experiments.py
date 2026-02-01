from subprocess import PIPE, Popen

if __name__ == "__main__":
    for trusteeNo in range(2, 6):
        for recipientNo in range(1, 21):
            sig_times = []
            ver_times = []
            with open(
                f"./data/signingTimes_{trusteeNo}Trustee_{recipientNo}Recip.csv", "rb"
            ) as f:
                num_Siglines = sum(1 for _ in f)
            with open(
                f"./data/verificationTimes_{trusteeNo}Trustee_{recipientNo}Recip.csv",
                "rb",
            ) as f:
                num_Verlines = sum(1 for _ in f)
            while num_Siglines < 200 or num_Verlines < 200:
                with open(
                    f"./data/signingTimes_{trusteeNo}Trustee_{recipientNo}Recip.csv",
                    "rb",
                ) as f:
                    num_Siglines = sum(1 for _ in f)
                with open(
                    f"./data/verificationTimes_{trusteeNo}Trustee_{recipientNo}Recip.csv",
                    "rb",
                ) as f:
                    num_Verlines = sum(1 for _ in f)
                process = Popen(
                    [
                        "python3",
                        "./BasicTimings.py",
                        "0",
                        f"{trusteeNo}",
                        f"{recipientNo}",
                    ],
                    stdout=PIPE,
                    stderr=PIPE,
                )
                process.communicate()
