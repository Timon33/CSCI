from .io_util import read_input


def main() -> None:
    n, jobs = read_input("examples/input_1.txt")
    print(n)
    print(jobs)
