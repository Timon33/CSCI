from typing import List, Tuple, Dict, Optional
from itertools import batched, accumulate

from csci.io_util import JobInfo, JobInterval
from csci.offline.solver import Solver

from scipy.optimize import linprog

class LPSolver(Solver):

    job_infos = List[JobInfo]

    def __init__(self, job_infos: List[JobInfo]):
        self.job_infos: List[JobInfo] = job_infos

    @staticmethod
    def distribute_interrupts(remaining_k: int, n: int):
        if n == 0:
            yield []
        else:
            for k in range(remaining_k + 1):
                for k_js in LPSolver.distribute_interrupts(remaining_k - k, n - 1):
                    yield [k] + k_js

    @staticmethod
    def valid_shapes(last_job: Optional[int], remaining_k: Dict[int, int]):
        if len(remaining_k) == 0:
            yield [], {}
        else:
            for job_id in remaining_k.keys():
                if last_job is None or job_id != last_job:
                    last_interval = {}
                    new_remaining_k = remaining_k.copy()
                    new_remaining_k[job_id] -= 1

                    # remove task if its max interrupts have been reached
                    if new_remaining_k[job_id] < 0:
                        last_interval[job_id] = 0
                        del new_remaining_k[job_id]

                    for s, last_index_map in LPSolver.valid_shapes(job_id, new_remaining_k):
                        last_index_map = {job_id: li + 1 for job_id, li in last_index_map.items()} | last_interval
                        yield [job_id] + list(s), last_index_map



    def solve(self) -> Tuple[float, List[JobInterval]]:

        N = len(self.job_infos)
        best_tct = float('inf')
        best_schedule = None
        best_ordering = None

        # iterate over all possible distribution of N - 1 interrupts among N tasks
        for k_distribution in self.distribute_interrupts(N - 1, N):
            print("Now working on k_dist:", k_distribution)
            processed = 0
            ks = {k: v for k, v in enumerate(k_distribution)}

            # calculate total penalized processing times
            qs = [job.alpha ** ks[j_id] * job.processing_time
                  for j_id, job in enumerate(self.job_infos)]

            # optimization: if the lower bound of the optimum is larger than best, skip this shape
            if best_tct is not None and list(accumulate(qs))[-1] >= best_tct:
                print("Skip k_dist. Optimum LB", list(accumulate(qs))[-1])
                continue

            # generate all valid shapes where task k is interrupted v times
            for ordering, last_interval_index in LPSolver.valid_shapes(None, ks):
                # construct the LP
                # A_ub @ x <= b_ub
                # A_eq @ x == b_eq
                # lb <= x <= ub

                # x = [s_1, t_1, s_2, t_2, ...], len(x) = 2 * len(ordering)


                # 1. total processing time constraints
                b_eq = qs
                A_eq = [[0] * (len(ordering) * 2) for _ in range(N)]
                for i, job_id in enumerate(ordering):
                    A_eq[job_id][i * 2 + 1] = 1

                # 2. non overlapping intervals
                A_ub = [[0] * (len(ordering) * 2) for _ in range(len(ordering) - 1)]
                for i in range(len(ordering) - 1):
                    A_ub[i][i * 2] = 1
                    A_ub[i][i * 2 + 1] = 1
                    A_ub[i][i * 2 + 2] = -1

                b_ub = [0] * (len(ordering) - 1)

                # 3. release times
                bounds = []
                for i in ordering:
                    bounds.append([self.job_infos[i].release_time, None])
                    bounds.append([0, None])

                # construct the tct optimization target vector
                c = [0] * (len(ordering) * 2)
                for last_interval_idx in last_interval_index.values():
                    c[last_interval_idx * 2] = 1
                    c[last_interval_idx * 2 + 1] = 1

                # print("ordering:", ordering)
                # print("Optimize: c =", c)
                # print("A_eq:")
                # for r in A_eq:
                #     print(r)
                # print("b_eq: ", b_eq)

                # print("A_ub:")
                # for r in A_ub:
                #     print(r)
                # print("b_ub: ", b_ub)
                # print("bound:", bounds)

                lp = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds,
                             method="highs")

                if lp.success:
                    if lp.fun < best_tct:
                        best_tct = lp.fun
                        best_schedule = lp.x
                        best_ordering = ordering
                        print("best solution improved to: ", best_tct)
                        print("ordering:", best_ordering)
                        print("x:", best_schedule)
                else:
                    print("No solution found", ordering)

                processed += 1

            print("processed jobs:", processed)

        best_schedule = [JobInterval(best_ordering[i], s, t) for i, (s, t) in
                         enumerate(batched(best_schedule, 2))]
        return best_tct, best_schedule

