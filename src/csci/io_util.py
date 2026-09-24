from dataclasses import dataclass
from typing import List, Tuple

@dataclass
class JobInfo:
    release_time: float
    processing_time: float
    alpha: float

@dataclass
class JobInterval:
    job_id: int
    start_time: float
    duration: float


def read_input(filename: str) -> Tuple[int, List[JobInfo]]:
    with open(filename, "r") as f:
        lines = f.readlines()
        n = int(lines[0])
        jobs: List[JobInfo] = []
        for i in range(n):
            r, p, a = lines[i].split(",")
            # TODO: float format can cause precision issues
            jobs.append(JobInfo(float(r), float(p), float(a)))

        assert len(jobs) == n
        return n, jobs


def read_output(filename: str) -> Tuple[int, float, List[JobInterval]]:
    with open(filename, "r") as f:
        lines = f.readlines()
        n = len(lines) - 1
        schedule: List[JobInterval] = []
        for i in range(n):
            job_id, start_time, duration = lines[i].split(",")
            # TODO: float format can cause precision issues
            schedule.append(JobInterval(int(job_id) - 1, float(start_time), float(duration)))
        score = float(lines[-1])
        return n, score, schedule

