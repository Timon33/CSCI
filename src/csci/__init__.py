from .io_util import read_input
from .offline_algorithms import CSCI_Instance

def main() -> None:
    n, jobs = read_input("examples/input_2.txt")
    instance = CSCI_Instance(jobs)
    print(instance.job_infos)

    tct, solve = instance.solve()
    print(instance.job_infos)
    print(tct)
    for interval in reversed(solve):
        print(interval)
