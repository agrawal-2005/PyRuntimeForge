# PyRuntime Forge Test Cases

This folder contains simple test cases you can use to validate the main behaviors of PyRuntime Forge.

## How To Use

For multi-step tests:

1. Open the app.
2. Login to the same user session.
3. Copy the contents of `step1` into the command box and run it.
4. Clear the box.
5. Copy the contents of `step2` into the command box and run it.

## Included Tests

- `filesystem_statefulness_step1.py`
  Creates a CSV file in the user's container.
- `filesystem_statefulness_step2.py`
  Reads the CSV file from a second execution to prove filesystem persistence.
- `ram_statefulness_step1.py`
  Stores a Python variable in memory.
- `ram_statefulness_step2.py`
  Tries to read that variable in a second execution. This should fail in the current implementation.
- `interactive_guess_game.py`
  A guessing game that uses `input()` to validate interactive stdin support.
- `data_science_demo_step1.py`
  Saves a small analytics dataset in the user's container.
- `data_science_demo_step2.py`
  Loads that saved dataset and calculates summary values.

## Expected Results

### Filesystem Statefulness

Expected:

- `step1` creates `sales.csv`
- `step2` can still read `sales.csv`

This proves the container filesystem is persistent between executions.

### RAM Statefulness

Expected:

- `step1` prints `Stored x = 12345`
- `step2` fails with `NameError`

This proves the current implementation is not RAM-stateful because each click starts a fresh `python -c` process.

### Interactive Input

Expected:

- the app prints prompts like `Take a guess:`
- you can reply using the input box shown below the `Execute` button
- the game continues normally

### Data Science Demo

Expected:

- `step1` writes `global_sales.csv`
- `step2` loads the file and prints totals without recreating the dataset

This is a good demo of the project's stateful container behavior.
