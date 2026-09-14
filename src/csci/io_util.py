from typing import List, Tuple


def read_input(filename: str) -> Tuple[int, List[Tuple[float, float, float]]]:
    with open(filename, "r") as f:
        lines = f.readlines()
        n = int(lines[0])
        jobs: List[Tuple[float, float, float]] = []
        for i in range(n):
            jobs.append(tuple(map(float, lines[i + 1].split(","))))
            assert len(jobs[-1]) == 3

        assert len(jobs) == n
        return n, jobs

