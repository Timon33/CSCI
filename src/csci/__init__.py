from .io_util import read_input
from .offline_algorithms import CSCI_Instance

def main() -> None:
    n, jobs = read_input("examples/input_2.txt")
    instance = CSCI_Instance(jobs)

    tct, schedule = instance.solve()
    print(tct)
    for interval in schedule:
        print(interval)
