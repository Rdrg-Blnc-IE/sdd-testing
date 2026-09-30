# Order Flow: Testing Practice

You are joining a team that already shipped a small order processing service.
The code works. What it does not have is a single test, so nobody dares change
it. Your job is to build the safety net.

This is the inverse of the design patterns exercises: **the production code is
given and you write the tests.**

## What you practice

| Exercise | Topic | File |
| --- | --- | --- |
| 1a | Unit tests, `pytest.raises` | `tests/test_pricing.py` |
| 1b | Unit tests on validation logic | `tests/test_validation.py` |
| 2 | Integration tests, fixtures with teardown | `tests/test_users.py` |
| 3 | Mocking an external API with `@patch` | `tests/test_services.py` |
| 3b | `monkeypatch` for environment config | `tests/test_services.py` |
| 4 | `Mock(spec=...)`, `patch.object`, asserting on calls | `tests/test_services.py` |
| 4b | When not to mock, and `capsys` | `tests/test_services.py` |
| 5 | `parametrize` | `tests/test_pytest_features.py` |
| 6 | TDD: red, green, refactor | `tests/test_password.py` |
| Bonus | `side_effect`, `call_count`, `reset_mock` | `tests/test_mock_practices.py` |

## Architecture

- `orderflow/pricing.py` and `orderflow/validation.py`: pure functions, the
  easiest things in the codebase to unit test.
- `orderflow/users.py`: `Database` plus the `UserRepository` built on it. Two
  collaborating objects, so tests here are integration tests.
- `orderflow/services.py`: `WeatherService` calls a real HTTP API,
  `NotificationService` sends real messages, and `OrderProcessor` orchestrates
  both. Nothing here can be tested for real, so everything gets a test double.
- `orderflow/password.py`: empty on purpose. Exercise 6 fills it in with TDD.

## Project layout

```dir_tree
root_dir
├─ orderflow/
│  ├─ __init__.py
│  ├─ password.py
│  ├─ pricing.py
│  ├─ services.py
│  ├─ users.py
│  └─ validation.py
├─ tests/
│  ├─ conftest.py
│  ├─ test_mock_practices.py
│  ├─ test_password.py
│  ├─ test_pricing.py
│  ├─ test_pytest_features.py
│  ├─ test_services.py
│  ├─ test_users.py
│  └─ test_validation.py
└─ README.md
```

## Setup

Preferred: [uv](https://docs.astral.sh/uv/). Install uv once per machine (see
uv's docs), then from inside the repo:

```bash
uv venv                              # create a local virtual environment (.venv)
uv pip install -r requirements.txt   # install pytest and its plugins into it
```

From then on, run any Python command through `uv run` so it uses that
environment automatically:

```bash
uv run pytest                                  # run everything
uv run pytest ./tests/test_pricing.py          # run one file
uv run pytest ./tests/test_pricing.py -v       # one test per line
uv run pytest -k email                         # only tests matching "email"
uv run pytest -x                               # stop at the first failure
uv run pytest --cov=orderflow --cov-report=term-missing   # what is still untested
```

<details>
<summary>Alternative: plain venv + pip</summary>

```bash
# Unix
python -m venv .venv && source .venv/bin/activate

# Windows:
python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

python -m pytest
```

</details>

Every test starts as a failing `assert False`, so a red suite on a fresh clone
is expected. Replace one `TODO` block at a time and watch the count go green.

## How to submit

1. Fork this repo to your own GitHub account. Keep the fork **public** (the
   default when forking a public repo) so it can be reviewed without needing
   collaborator access.
2. Clone your fork and work through the exercises below on a branch, e.g.:

   ```bash
   git switch -c solution
   ```

3. Commit your changes and push the branch to your fork:

   ```bash
   git push origin solution
   ```

4. Open a **pull request** from your branch into this repo's `main` branch.
5. Opening the PR automatically runs the suite as a GitHub Actions check. See
   the "Checks" tab on your PR.
6. Submit the link to your pull request on Blackboard. This is your
   submission; the green check confirms the tests pass, but the PR itself
   (with your commits and diff) is what gets graded.

**The check is a coverage gate, not just a pass/fail run.** Because you are
the one writing the tests, a green suite proves nothing on its own: eight
copies of `assert True` also pass. CI therefore runs
`pytest --cov=orderflow --cov-fail-under=90` and fails if your tests leave
more than 10% of `orderflow/` unexercised. Run the `--cov-report=term-missing`
command above locally to see exactly which lines you have not reached yet.

## Exercises

### 1. Unit tests

Functional requirements:

- Cover the happy path of `calculate_total_price`, with and without a discount.
- Cover its edge cases, including a zero quantity.
- Cover every `ValueError` it can raise, asserting on the message with
  `pytest.raises(..., match=...)` rather than just the type.
- Do the same for `validate_email`, covering valid addresses and each distinct
  way an address can be invalid.

```bash
uv run pytest ./tests/test_pricing.py ./tests/test_validation.py
```

Goal --> Pass the unit tests

### 2. Integration tests and fixtures

Functional requirements:

- Build a `database` fixture that connects before the test and disconnects
  after it. Use `yield`, so the teardown runs even when the test fails.
- Build a `user_repo` fixture that depends on the `database` fixture. Fixtures
  composing other fixtures is the point here.
- Test that a user survives a round trip through the repository.
- Test the failure paths: an invalid email, and a database that was never
  connected. Cover both directions against the unconnected database, because
  reads and writes each check the connection separately.

```bash
uv run pytest ./tests/test_users.py
```

Goal --> Pass the integration tests

### 3. Mocking an external API

Functional requirements:

- Patch `requests.get` so no test in this repo ever touches the network. Your
  suite must pass with the wifi turned off.
- Assert on the temperature the service returns, and separately assert that
  the request went to the expected URL with the expected params.
- Cover both sides of the `is_good_weather` threshold.
- Cover the failure path, using `side_effect` to make the API raise.
- Use `monkeypatch` for the `from_env` constructor: one test with the
  environment variable set, one with it absent.

```bash
uv run pytest ./tests/test_services.py
```

Goal --> Pass the weather service tests

### 4. Test doubles and call assertions

Functional requirements:

- Inject `Mock(spec=WeatherService)` and `Mock(spec=NotificationService)` into
  `OrderProcessor`. Always pass `spec=`, so a typo in a method name fails the
  test instead of silently returning another mock.
- Assert on the **behaviour**, not just the return value: the email body must
  mention the weather when it is good, and must not when it is not.
- Do the same flow again with `patch.object`, patching the methods on the real
  classes instead of injecting doubles. Note that stacked decorators apply
  bottom-up, so the bottom one is the first test parameter.
- Cover what the result looks like when sending the notification fails.
- Finally, test `NotificationService.send_email` directly, with no double at
  all, using the `capsys` fixture to capture what it prints. Mocks are for
  collaborators you cannot afford to call; this one is cheap, so calling it
  for real is both simpler and a stronger test. Knowing when *not* to mock
  matters as much as knowing how.

```bash
uv run pytest ./tests/test_services.py
```

Goal --> Pass the order processor tests

### 5. Parametrized tests

Functional requirements:

- Re-express the pricing and email cases as tables of inputs and expected
  outputs, with a single test body driven by `@pytest.mark.parametrize`.
- Compare the failure output to Exercise 1. A parametrized failure names the
  offending case, which is why this scales better than a copy-pasted test.

```bash
uv run pytest ./tests/test_pytest_features.py -v
```

Goal --> Pass the parametrized tests

### 6. TDD: build the password validator

This is the only exercise where you write production code, and the only one
where the test comes **first**. `orderflow/password.py` raises
`NotImplementedError` today.

`validate_password(password)` returns a list of error messages, one per broken
rule, in any order. An empty list means the password is valid. The rules and
their exact messages:

| Rule | Message |
| --- | --- |
| At least 8 characters | `Password must be at least 8 characters long` |
| At least one uppercase letter | `Password must contain an uppercase letter` |
| At least one lowercase letter | `Password must contain a lowercase letter` |
| At least one digit | `Password must contain a digit` |
| At least one character from `!@#$%^&*()-_=+[]{};:,.<>?/` | `Password must contain a special character` |

Work one row at a time, top to bottom:

1. **Red.** Write one test for that rule. Run it. Confirm it fails, and that
   it fails for the reason you expect rather than an import error or a typo.
2. **Green.** Make the smallest change to `password.py` that passes it. Resist
   implementing rules you have not written a test for yet.
3. **Refactor.** With the suite green, tidy the implementation. A table of
   rules beats five stacked `if` statements once the fifth one arrives.

Then add two more tests: a valid password returns an empty list, and a
password breaking several rules at once reports all of them.

Commit after each green step. Your commit history is the evidence that you
worked in the cycle rather than writing the implementation first and the tests
afterwards.

```bash
uv run pytest ./tests/test_password.py -v
```

Goal --> Pass your own password tests, with a history that shows the cycle
