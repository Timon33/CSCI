from pathlib import Path
from typing import List

import pytest

from csci.io_util import JobInfo, JobInterval, read_input, read_output

EPSILON = 1e-8
EXAMPLES_DIR = Path(__file__).parent.parent / "examples"


def eq(a: float, b: float) -> bool:
    return abs(a - b) < EPSILON


def validate_schedule(
    jobs: List[JobInfo],
    score: float,
    schedule: List[JobInterval],
) -> List[str]:
    n = len(jobs)
    times = [0.0 for _ in range(n)]
    freqs = [0 for _ in range(n)]
    last_task_end = [-1.0 for _ in range(n)]
    cur_time = 0.0
    msgs: List[str] = []
    for interval in schedule:
        if interval.start_time < cur_time - EPSILON:
            msgs.append(
                f"Task with start time {interval.start_time} for job {interval.job_id + 1} starts before the previous has ended"
            )
        release_time = jobs[interval.job_id].release_time
        if interval.start_time < release_time - EPSILON:
            msgs.append(
                f"Task with start time {interval.start_time} for job {interval.job_id + 1} starts before the task is released"
            )

        times[interval.job_id] += interval.duration
        cur_time = interval.start_time + interval.duration
        last_task_end[interval.job_id] = cur_time
        freqs[interval.job_id] += 1

    cor_score = 0.0
    for i in range(n):
        penalties = max(0, freqs[i] - 1)
        correct_time = jobs[i].processing_time * jobs[i].alpha**penalties
        if not eq(times[i], correct_time):
            msgs.append(
                f"Job {i} is not done for the correct amount of time: time={times[i]}, but should be {correct_time} including {penalties} penalties"
            )
        cor_score += last_task_end[i]

    if not eq(score, cor_score):
        msgs.append(f"Given score is not correct, should be {cor_score}")
    return msgs


def _example_cases():
    cases = []
    for out_file in sorted(EXAMPLES_DIR.glob("*.out")):
        in_file = out_file.with_suffix(".in")
        if in_file.exists():
            cases.append(pytest.param(in_file, out_file, id=out_file.stem))
    return cases


@pytest.mark.parametrize("in_file,out_file", _example_cases())
def test_example_schedule_is_valid(in_file: Path, out_file: Path) -> None:
    _, jobs = read_input(str(in_file))
    _, score, schedule = read_output(str(out_file))

    msgs = validate_schedule(jobs, score, schedule)

    assert msgs == []
