# Assignment 1 — Mini-Prototype

## Assigned Tool

[Retry/backoff]

## Prototype Objective

[To demonstrate how retry/backoff tool works in trancient or temporary failures]

## Problem Being Demonstrated

[This prototype shows how retry/backoff mechanism works to solve a specific trancient failure called network failure]

## Technologies Used

- [Retry/backoff]
- [Python]

## Prototype Structure

The prototype is built around four main components:

1. **Network Request Function** — Simulates a network operation that can randomly experience a temporary timeout.
2. **Retry Function** — Detects timeouts and retries the request up to a defined maximum.
3. **Linear Backoff + Full Jitter** — Controls how long the system waits before each retry.
4. **`unittest.mock`** — Creates controlled failure scenarios for testing.

The structure separates the simulated network operation from the retry logic, making the prototype easier to test and understand.


## How It Works

The prototype first attempts the network request.

If the request succeeds, the result is returned immediately.

If a timeout occurs:

1. The failure is detected.
2. A linear backoff delay is calculated.
3. Full jitter randomly selects the actual waiting time.
4. The system waits.
5. The request is retried.

The process continues until the request succeeds or the maximum retry limit is reached.


## How to Run

The prototype is written in Python and can be run using VS Code.

1. Open the project folder in VS Code.
2. Open `prototype.py`.
3. Open the VS Code terminal.
4. Run:

```powershell
python prototype.py
```

The program will display the retry attempts, timeout failures, backoff values, jitter delays, and final result in the terminal.

# How It Was Tested

The prototype was tested using `unittest.mock` to create controlled network behaviors.

Three scenarios were tested:

1. **Immediate Success** — The request succeeds on the first attempt.
2. **Temporary Failure** — The first request times out, followed by a successful retry.
3. **Repeated Failure** — Every request times out until the maximum retry limit is reached.

These tests verify that the retry mechanism can recover from temporary failures and correctly stop when failures persist.


## Known Limitations

* **Simulated failures:** The network failures are simulated rather than caused by a real network service.
* **Limited error handling:** The prototype mainly handles `TimeoutError` and does not cover other network or HTTP errors.
* **Fixed configuration:** The failure probability, retry limit, and backoff settings are manually configured.
* **Real waiting time:** `time.sleep()` makes the prototype wait during retries, which can slow down testing.
* **No production environment:** The prototype has not been tested under real network traffic or high-load conditions.
* **Basic testing:** Only three main scenarios are tested: immediate success, temporary failure, and repeated failure.
* **No performance metrics:** The prototype does not measure factors such as total retry time, success rate, or network load.

