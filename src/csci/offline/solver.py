from abc import ABC, abstractmethod
from typing import List, Tuple

from csci.io_util import JobInfo, JobInterval


class Solver(ABC):

    @abstractmethod
    def __init__(self, job_infos: List[JobInfo]):
        ...

    @abstractmethod
    def solve(self) -> Tuple[float, List[JobInterval]]:
        ...
