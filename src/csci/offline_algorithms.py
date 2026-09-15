from dataclasses import dataclass
from typing import Tuple, List, Optional, Dict

from copy import deepcopy


@dataclass
class JobInfo:
    release_time: float
    processing_time: float
    alpha: float

@dataclass
class OpenJob:
    remaining_time: float
    k: int


class CSCI_Instance:

    job_infos = List[JobInfo]

    def __init__(self, job_infos: List[Tuple[float, float, float]]):
        job_infos = [JobInfo(*job_info) for job_info in job_infos]
        self.job_infos = sorted(job_infos, key=lambda x: x.release_time)

    def solve(self) -> Tuple[float, List[Tuple[int, float, float]]]:
        time, jobs = self.next_releases(-1)
        print("Starting solve", time, jobs)
        return self.dfs(time, jobs, None)

    def next_releases(self, time: float) -> Tuple[float, Dict[int, OpenJob]]:
        next_release_time = -1
        new_jobs: Dict[int, OpenJob] = {}
        for i, job_info in enumerate(self.job_infos):
            if next_release_time > -1:
                if job_info.release_time == next_release_time:
                    new_jobs[i] = OpenJob(job_info.processing_time, 0)
                else:
                    break

            if job_info.release_time > time:
                next_release_time = job_info.release_time
                new_jobs[i] = OpenJob(job_info.processing_time, 0)

        if next_release_time > -1:
            return next_release_time, new_jobs
        else:
            return float("inf"), {}

    def add_interruption_penalty(self, open_jobs: Dict[int, OpenJob], interrupted_job_id) -> None:
        open_jobs[interrupted_job_id].k += 1
        k = open_jobs[interrupted_job_id].k
        alpha = self.job_infos[interrupted_job_id].alpha
        p = self.job_infos[interrupted_job_id].processing_time

        open_jobs[interrupted_job_id].remaining_time += (alpha ** (k - 1)) * \
                                                         (alpha - 1) * p

    def dfs(self,
            current_time,
            open_jobs: Dict[int, OpenJob],
            last_job_id: Optional[int])\
        -> Tuple[float, List[Tuple[int, float, float]]]:

        min_completion_time = float("inf")
        optimal_solution = None

        next_release_time, future_jobs = self.next_releases(current_time)
        print(current_time, open_jobs, next_release_time, future_jobs, last_job_id)

        # Nothing to do anymore
        if len(open_jobs) == 0 and len(future_jobs) == 0:
            return 0, []

        for next_job_id, next_job in open_jobs.items():
            finish_time = next_job.remaining_time + current_time
            updated_open_jobs = deepcopy(open_jobs)

            if last_job_id is not None and next_job_id != last_job_id:
                # last job was interrupted
                self.add_interruption_penalty(updated_open_jobs, last_job_id)

            if next_release_time < finish_time:
                # next job released first
                updated_open_jobs[next_job_id].remaining_time -= next_release_time - current_time
                tct, solution = self.dfs(next_release_time, updated_open_jobs | deepcopy(future_jobs), next_job_id)
                solution.append((next_job_id, current_time, next_release_time - current_time))


                if tct < min_completion_time:
                    min_completion_time = tct
                    optimal_solution = solution

            else:
                # current job ended
                del updated_open_jobs[next_job_id]

                if next_release_time == finish_time:
                    # jobs released exactly at the completion time
                    updated_open_jobs |= deepcopy(future_jobs)

                tct, solution = self.dfs(finish_time, updated_open_jobs, None)
                tct += finish_time
                solution.append((next_job_id, current_time, finish_time - current_time))

                if tct < min_completion_time:
                    min_completion_time = tct
                    optimal_solution = solution

        # idle
        if len(future_jobs) > 0:
            idle_open_jobs = deepcopy(open_jobs)

            if last_job_id is not None:
                # idling interrupts the job that was running
                self.add_interruption_penalty(idle_open_jobs, last_job_id)

            tct, solution = self.dfs(next_release_time, idle_open_jobs | deepcopy(future_jobs), None)

            if tct < min_completion_time:
                min_completion_time = tct
                optimal_solution = solution


        return min_completion_time, optimal_solution