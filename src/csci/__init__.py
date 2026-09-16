import sys

from .io_util import read_input
from .offline_algorithms import CSCI_Instance

def main() -> None:
    _, jobs = read_input(sys.argv[1])
    instance = CSCI_Instance(jobs)

    tct, schedule = instance.solve()
    print(tct)
    for interval in schedule:
        print(interval)
