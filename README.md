# The-Meridian-Pivot-assignment-1
Assignment 1:solo recon
# Transient Failure Retry Prototype

## 1. Overview

This project is a Python prototype designed to simulate **transient network failures** and test how a retry mechanism responds to those failures.

The prototype demonstrates:

* Simulated network timeouts
* Retry logic
* Maximum retry limits
* Linear backoff
* Full jitter
* `unittest.mock` for controlled failure simulation
* Three key failure/recovery scenarios

The purpose of the prototype is to understand and test how a system can recover from temporary network failures without retrying indefinitely or overwhelming a service.

---

## 2. Objectives

The prototype is designed to test the following situations:

### Scenario 1 — Immediate Success

The network request succeeds on the first attempt.

Expected behavior:

```text
Attempt 1 → SUCCESS
```

No retry should occur.

---

### Scenario 2 — Temporary Timeout Followed by Successful Recovery

The first request fails because of a timeout, but the following attempt succeeds.

Expected behavior:

```text
Attempt 1 → TIMEOUT
           ↓
      Backoff + Jitter
           ↓
Attempt 2 → SUCCESS
```

This tests whether the retry mechanism can successfully recover from a transient failure.

---

### Scenario 3 — Repeated Timeout Resulting in Failure

The network request continuously times out.

Expected behavior:

```text
Attempt 1 → TIMEOUT
Attempt 2 → TIMEOUT
Attempt 3 → TIMEOUT
Attempt 4 → TIMEOUT
Attempt 5 → TIMEOUT
              ↓
       Maximum retries
              ↓
           FAILURE
```

This tests whether the retry mechanism correctly stops after reaching the configured retry limit.

---

# 3. Technologies Used

The prototype uses Python and its standard library.

### Python

Python is used to implement the simulated network request, retry mechanism, backoff calculation, jitter, and test scenarios.

### `time`

The `time` module is used to pause execution between retry attempts.

```python
time.sleep(wait_time)
```

### `random`

The `random` module is used to generate the jitter value.

```python
random.uniform(0, backoff)
```

### `unittest.mock`

`unittest.mock` is used to simulate predictable network behavior without requiring a real network connection.

This allows specific failure sequences to be tested.

---

# 4. Project Structure

The prototype currently consists of a single Python file:

```text
Transient failure prototype/
│
└── prototype.py
```

The main components inside `prototype.py` are:

```text
network_request()
        ↓
retry_request()
        ↓
unittest.mock scenarios
```

---

# 5. Simulated Network Request

The first function in the prototype represents the network operation:

```python
def network_request():
    failure_chance = 0.5

    if random.random() < failure_chance:
        raise TimeoutError("Temporary network timeout")

    return "Data received successfully"
```

The function has a 50% probability of producing a timeout.

If the randomly generated value falls below the configured failure probability, a `TimeoutError` is raised.

Otherwise, the function returns a successful response.

This creates a simple simulation of a network operation that may temporarily fail.

---

# 6. Retry Mechanism

The retry mechanism is implemented using:

```python
def retry_request(request, max_retries=5, base_delay=1):
```

The function attempts to execute the supplied network operation.

If the request succeeds, the result is returned immediately.

If a `TimeoutError` occurs, the function calculates a backoff period and waits before trying again.

The retry process continues until:

1. The request succeeds, or
2. The maximum number of attempts is reached.

---

# 7. Linear Backoff

The prototype uses a linear backoff strategy.

The backoff is calculated using:

```python
backoff = base_delay * attempt
```

With a base delay of one second, the theoretical backoff limit increases as follows:

```text
Attempt 1 → 1 second
Attempt 2 → 2 seconds
Attempt 3 → 3 seconds
Attempt 4 → 4 seconds
Attempt 5 → 5 seconds
```

The purpose of increasing the delay is to avoid immediately retrying a failing network operation repeatedly.

---

# 8. Full Jitter

The prototype combines linear backoff with full jitter.

The jittered wait time is calculated using:

```python
wait_time = random.uniform(0, backoff)
```

This means the actual waiting time is randomly selected between zero and the calculated backoff limit.

For example:

```text
Backoff limit: 3 seconds

Possible wait times:
0.00 seconds
0.47 seconds
1.26 seconds
2.15 seconds
2.93 seconds
```

The exact value is different each time because it is randomly generated.

The combination can therefore be represented as:

```text
Linear Backoff
      +
Full Jitter
      ↓
Randomized Retry Delay
```

---

# 9. Why Use Jitter?

If many clients experience the same network failure and all retry at exactly the same time, they can create another sudden burst of traffic.

For example:

```text
100 clients
    ↓
Network failure
    ↓
All wait 2 seconds
    ↓
100 clients retry simultaneously
```

Jitter randomizes the retry timing:

```text
Client 1 → 0.4 sec
Client 2 → 1.1 sec
Client 3 → 1.7 sec
Client 4 → 0.3 sec
Client 5 → 1.9 sec
```

This spreads retry attempts over time and can reduce synchronized retry traffic.

---

# 10. `unittest.mock`

The prototype uses `unittest.mock` to create controlled failure scenarios.

A mock request can be created with:

```python
mock_request = Mock()
```

The behavior of the mock can then be controlled using `side_effect`.

For example:

```python
mock_request.side_effect = [
    TimeoutError(),
    "Data recovered successfully"
]
```

This forces the mock to behave as follows:

```text
First call  → TimeoutError
Second call → Success
```

This is useful because random failure simulation cannot guarantee a specific sequence.

---

# 11. Test Scenarios

## Scenario 1: Immediate Success

```python
mock_request_1 = Mock()

mock_request_1.return_value = "Data received successfully"

retry_request(mock_request_1)
```

Expected result:

```text
Attempt 1 → SUCCESS
```

The retry mechanism should not perform another attempt.

---

## Scenario 2: Temporary Timeout

```python
mock_request_2 = Mock()

mock_request_2.side_effect = [
    TimeoutError("Temporary timeout"),
    "Data recovered successfully"
]

retry_request(mock_request_2)
```

Expected result:

```text
Attempt 1 → TIMEOUT
              ↓
       Linear backoff
              ↓
         Full jitter
              ↓
Attempt 2 → SUCCESS
```

This confirms that the system can recover after a temporary failure.

---

## Scenario 3: Repeated Timeout

```python
mock_request_3 = Mock()

mock_request_3.side_effect = TimeoutError(
    "Persistent network timeout"
)

retry_request(
    mock_request_3,
    max_retries=5
)
```

Because the mock continuously raises `TimeoutError`, every attempt fails.

Expected result:

```text
Attempt 1 → TIMEOUT
Attempt 2 → TIMEOUT
Attempt 3 → TIMEOUT
Attempt 4 → TIMEOUT
Attempt 5 → TIMEOUT
              ↓
       Retry limit reached
              ↓
           FAILURE
```

This verifies that the retry mechanism does not retry forever.

---

# 12. Complete Retry Flow

The overall retry process can be represented as:

```text
                Start
                  │
                  ▼
          Execute network request
                  │
                  ▼
              Did it fail?
             /           \
           No             Yes
           │               │
           ▼               ▼
        Success      Is max retry reached?
                         /       \
                       Yes        No
                       │           │
                       ▼           ▼
                    Failure   Calculate linear
                              backoff
                                  │
                                  ▼
                             Apply full
                               jitter
                                  │
                                  ▼
                               Wait
                                  │
                                  ▼
                                Retry
```

---

# 13. Running the Prototype

Make sure Python is installed and available in VS Code.

From the project directory, run:

```powershell
python prototype.py
```

If your system uses `python3`, run:

```powershell
python3 prototype.py
```

The program will first run the random transient-failure simulation and then execute the three controlled `unittest.mock` scenarios.

---

# 14. Example Output

An example execution may look like:

```text
==============================================
RANDOM TRANSIENT FAILURE SIMULATION
==============================================

Attempt 1/5
Request failed: Temporary network timeout
Linear backoff limit: 1.00 seconds
Full jitter selected: 0.62 seconds
Retrying...

Attempt 2/5
Request succeeded.
Result: Data received successfully

Final result: SUCCESS
```

The controlled tests will then demonstrate:

```text
SCENARIO 1
Immediate success
```

```text
SCENARIO 2
Timeout → Backoff + Jitter → Success
```

```text
SCENARIO 3
Timeout → Backoff + Jitter → Timeout
→ Backoff + Jitter → Timeout
→ Maximum retries → Failure
```

The exact jitter values will vary between executions because they are randomly generated.

---

# 15. Key Design Principles

The prototype separates the network operation from the retry mechanism.

The network operation is responsible for:

```text
Simulating network behavior
```

The retry function is responsible for:

```text
Detecting timeout
       ↓
Retrying
       ↓
Calculating backoff
       ↓
Applying jitter
       ↓
Waiting
       ↓
Stopping after maximum retries
```

`unittest.mock` is responsible for:

```text
Creating deterministic test scenarios
```

This separation makes the prototype easier to understand, test, and extend.

---

# 16. Limitations

This is a prototype and does not represent a production-ready network retry implementation.

Some limitations include:

* The network failure is simulated rather than generated by a real network service.
* Only `TimeoutError` is handled.
* There is no HTTP status-code handling.
* There is no logging framework.
* Retry configuration is hard-coded in the prototype.
* `time.sleep()` makes the demonstration wait in real time.
* There is no automated test report.
* The random failure probability is fixed at 50%.
* The prototype does not distinguish between retryable and non-retryable failures.

---

# 17. Possible Future Improvements

The prototype could be extended by adding:

* Automated `unittest.TestCase` tests
* Configurable failure probability
* Exponential backoff
* Maximum backoff limits
* Additional retryable exceptions
* HTTP status-code handling
* Structured logging
* Metrics for retry count and total delay
* Configurable retry policies
* A real API/network endpoint
* Comparison between different backoff strategies

Possible future backoff strategies to compare include:

```text
Fixed Backoff
Linear Backoff
Exponential Backoff
Exponential Backoff + Full Jitter
```

---

# 18. Conclusion

This prototype demonstrates how a system can respond to transient network failures using a controlled retry strategy.

The core process is:

```text
Network Request
      ↓
Failure?
      ↓
Retry
      ↓
Linear Backoff
      ↓
Full Jitter
      ↓
Wait
      ↓
Retry Again
      ↓
Success OR Maximum Retry Failure
```

The prototype also uses `unittest.mock` to reproduce specific failure patterns, allowing the retry behavior to be tested consistently.

The three primary scenarios are:

1. **Immediate success**
2. **Temporary timeout followed by successful recovery**
3. **Repeated timeout resulting in failure**

Together, these scenarios provide a basic test of whether the retry mechanism behaves correctly under both successful and transient-failure conditions.
