"""
A script to run pylint on the app directory and check the score.
"""

import subprocess
import sys


class PylintChecker:
    """
    A class to encapsulate the functionality of running pylint and checking the score.
    """

    def __init__(self, threshold=9.8):
        """
        Initialize the PylintChecker with a score threshold.

        :param threshold: The minimum acceptable pylint score. Default is 9.8.
        :type threshold: float
        """
        self.threshold = threshold

    def run_pylint(self):
        """
        Run pylint on the app directory using the configuration file.

        :return: The stdout output and return code from running pylint.
        :rtype: tuple(str, int)
        """
        result = subprocess.run(
            ["pylint", "--recursive=true", "--rcfile=.pylintrc", "app"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False
        )
        return result.stdout, result.returncode

    def check_score(self, output):
        """
        Check the pylint score from the output and exit with an appropriate code.

        :param output: The stdout output from running pylint.
        :type output: str
        """
        print("Pylint output:\n", output)

        score_found = False
        for line in output.split("\n"):
            if "Your code has been rated at" in line:
                score_found = True
                score = float(line.split("/")[0].split()[-1])
                if score < self.threshold:
                    print(f"Pylint score is below {self.threshold}: {score}")
                    sys.exit(1)
                else:
                    print(f"Pylint score is sufficient: {score}")
                    sys.exit(0)

        if not score_found:
            print("Pylint score not found.")
            sys.exit(1)

    def run(self):
        """
        Run the pylint checker and handle the results.
        """
        output, returncode = self.run_pylint()
        if returncode != 0:
            print("Pylint encountered issues:")
            print(output)
        self.check_score(output)


if __name__ == "__main__":
    checker = PylintChecker(threshold=9.8)
    checker.run()
