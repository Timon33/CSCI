import sys

from .io_util import read_input
from csci.offline.dfs_bruteforce import DFSSolver
from csci.offline.lp_solver import LPSolver


def main() -> None:
    _, jobs = read_input(sys.argv[1])
    instance = LPSolver(jobs)

    tct, schedule = instance.solve()
    print(tct)
    for interval in schedule:
        print(interval)
