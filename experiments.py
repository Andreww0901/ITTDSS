from subprocess import PIPE, Popen

if __name__ == "__main__":
    for trusteeNo in range(2, 6):
        for recipientNo in range(1, 21):
            sig_times = []
            ver_times = []
            for _ in range(200):
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
