from dataclasses import dataclass
from typing import Tuple, List, Optional, Dict

from copy import deepcopy
from math import isclose

from csci.io_util import JobInfo


@dataclass
class OpenJob:
    remaining_time: float
    k: int

class DFSSolver:

    job_infos = List[JobInfo]

    def __init__(self, job_infos: List[JobInfo]):
        # `release` needs job_infos sorted by release time, so internal job ids
        # are positions in the sorted list. `original_ids` maps them back to the
        # order the jobs were given in, for the output. The sort is stable, so
        # jobs released simultaneously keep their input order.
        self.original_ids = sorted(range(len(job_infos)),
                                   key=lambda i: job_infos[i].release_time)
        self.job_infos = [job_infos[i] for i in self.original_ids]

    def solve(self) -> Tuple[float, List[Tuple[int, float, float]]]:
        """Total completion time and the schedule, in chronological order."""
        if len(self.job_infos) == 0:
            return 0, []

        tct, schedule = self.dfs(self.job_infos[0].release_time, {}, None, 0)

        # dfs builds the schedule back to front as the recursion unwinds
        schedule.reverse()

        return tct, self.merge_intervals(
            [(self.original_ids[job_id], start, duration)
             for job_id, start, duration in schedule])

    @staticmethod
    def merge_intervals(schedule: List[Tuple[int, float, float]]) \
            -> List[Tuple[int, float, float]]:
        """Join back-to-back intervals of the same job into one.

        A gap between two intervals of the same job means it was interrupted
        and idled over, which stays two intervals.
        """
        merged: List[Tuple[int, float, float]] = []

        for job_id, start, duration in schedule:
            if merged:
                last_id, last_start, last_duration = merged[-1]

                if last_id == job_id and isclose(last_start + last_duration, start,
                                                 rel_tol=1e-9, abs_tol=1e-9):
                    # recompute the length from the ends, so repeated merges do
                    # not accumulate rounding error
                    merged[-1] = (last_id, last_start, start - last_start + duration)
                    continue

            merged.append((job_id, start, duration))

        return merged

    def release(self, time: float, released_count: int) -> Tuple[Dict[int, OpenJob], int]:
        """All jobs released at or before `time` that are not released yet.

        `released_count` is the number of jobs already released; since
        `job_infos` is sorted by release time, it is a frontier into the list
        and each job is handed out exactly once.
        """
        new_jobs: Dict[int, OpenJob] = {}
        i = released_count

        while i < len(self.job_infos) and self.job_infos[i].release_time <= time:
            new_jobs[i] = OpenJob(self.job_infos[i].processing_time, 0)
            i += 1

        return new_jobs, i

    def next_release_time(self, released_count: int) -> float:
        if released_count < len(self.job_infos):
            return self.job_infos[released_count].release_time
        else:
            return float("inf")

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
            last_job_id: Optional[int],
            released_count: int)\
        -> Tuple[float, List[Tuple[int, float, float]]]:

        min_completion_time = float("inf")
        optimal_solution = None

        # Whatever became available at or before now is ours to schedule, no
        # matter which branch jumped us here. Never mutate `open_jobs` itself,
        # the union below shares its OpenJob values with the caller.
        new_jobs, released_count = self.release(current_time, released_count)
        open_jobs = open_jobs | new_jobs

        next_release_time = self.next_release_time(released_count)

        # Nothing to do anymore
        if len(open_jobs) == 0 and next_release_time == float("inf"):
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
                tct, solution = self.dfs(next_release_time, updated_open_jobs, next_job_id, released_count)
                solution.append((next_job_id, current_time, next_release_time - current_time))


                if tct < min_completion_time:
                    min_completion_time = tct
                    optimal_solution = solution

            else:
                # current job ended
                del updated_open_jobs[next_job_id]

                tct, solution = self.dfs(finish_time, updated_open_jobs, None, released_count)
                tct += finish_time
                solution.append((next_job_id, current_time, finish_time - current_time))

                if tct < min_completion_time:
                    min_completion_time = tct
                    optimal_solution = solution

        # idle
        if next_release_time < float("inf"):
            idle_open_jobs = deepcopy(open_jobs)

            if last_job_id is not None:
                # idling interrupts the job that was running
                self.add_interruption_penalty(idle_open_jobs, last_job_id)

            tct, solution = self.dfs(next_release_time, idle_open_jobs, None, released_count)

            if tct < min_completion_time:
                min_completion_time = tct
                optimal_solution = solution


        return min_completion_time, optimal_solution