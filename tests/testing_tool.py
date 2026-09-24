from typing import Tuple, List


epsilon = 1e-8


def eq(a: float, b: float) -> bool:
    return abs(a - b) < epsilon


def test_output(
    jobs: List[Tuple[float, float, float]],
    score: int,
    schedule: List[Tuple[float, float, float]],
) -> [str]:
    n = len(jobs)
    times = [0 for i in range(n)]
    freqs = [0 for i in range(n)]
    last_task_end = [-1 for i in range(n)]
    cur_time = 0
    msgs: [str] = []
    for job, start_time, run_time in schedule:
        if start_time < cur_time - epsilon:
            msgs.append(
                f"Task with start time {start_time} for job {job + 1} starts before the previous has ended"
            )
        release_time, _, _ = jobs[job]
        if start_time < release_time - epsilon:
            msgs.append(
                f"Task with start time {start_time} for job {job + 1} starts before the task is released"
            )

        times[job] += run_time
        cur_time = start_time + run_time
        last_task_end[job] = cur_time
        freqs[job] += 1
    cor_score: float = 0.0
    for i in range(n):
        _, time, a = jobs[i]
        penalties = max(0, freqs[i] - 1)
        correct_time = time * a**penalties
        if not eq(times[i], correct_time):
            msgs.append(
                f"Job {i} is not done for the correct amount of time: time={times[i]}, but should be {correct_time} including {penalties} penalties"
            )
        cor_score += last_task_end[i]

    if not eq(score, cor_score):
        msgs.append(f"Given score is not correct, should be {cor_score}")
    return msgs
