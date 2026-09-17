import sys

from .io_util import read_input,read_output
from .offline_algorithms import CSCI_Instance
from testing_tool import test_output


def main() -> None:
    _, jobs = read_input(sys.argv[1])
    instance = CSCI_Instance(jobs)

    tct, schedule = instance.solve()
    print(tct)
    for interval in schedule:
        print(interval)


def test() -> None:
    _, jobs = read_input(sys.argv[1])
    n, score, schedule = read_output(sys.argv[2])
    msgs = test_output(jobs, score, schedule)
    if len(msgs) == 0:
        print("Output is valid")
    else:
        print("Output is invalid:")
        for msg in msgs:
            print(msg)
