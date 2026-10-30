## Setup

Install dependencies (including dev dependencies like `pytest`):
```
uv sync
```

## Run

Solve a scheduling instance from an input file:
```
uv run csci <inputfile>
```

Example:
```
uv run csci examples/input_1.txt
```

The dfs solver exists for legacy reasons, use the lp solver (default if not overwritten)

## Test

Run the test suite:
```
uv run pytest
```
