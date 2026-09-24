from typing import List, Tuple

from csci.io_util import JobInfo, JobInterval
from csci.offline.solver import Solver


class LPSolver(Solver):

    job_infos = List[JobInfo]

    def __init__(self, job_infos: List[JobInfo]):
        pass

    def solve(self) -> Tuple[float, List[JobInterval]]:
        pass