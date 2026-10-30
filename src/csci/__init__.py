import sys
from sched import scheduler
from typing import List

from .io_util import read_input, JobInterval
from csci.offline.dfs_bruteforce import DFSSolver
from csci.offline.lp_solver import LPSolver
from csci.offline.milp_solver import MILPSolver

SOLVERS = {"lp": LPSolver, "milp": MILPSolver, "dfs": DFSSolver}


def main() -> None:
    _, jobs = read_input(sys.argv[1])
    name = sys.argv[2] if len(sys.argv) > 2 else "lp"
    instance = SOLVERS[name](jobs)

    schedule: List[JobInterval] = []
    tct, schedule = instance.solve()
    print(tct)
    for interval in schedule:
        print(f"{interval.job_id+1}, {interval.start_time}, {interval.duration}")
