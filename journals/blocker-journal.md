# Meridian Pivot — Assignment 1
# Blocker Journal

This journal records significant errors, dead ends, failed approaches,
investigations, fixes, and lessons encountered during the solo
reconnaissance period.

---

# Blocker 001

## Identification

**Date:**

**Time encountered:**

**Time resolved:**

**Total time blocked:**

**Severity:**
- [ ] Low
- [x] Medium
- [ ] High

---

## Problem

I was trying to create a controlled test where the operation would fail with a timeout on the first attempt and then return a successful result on a later attempt.

### Expected Result

I expected the mocked operation to behave like this:

Attempt 1 → Timeout  
Attempt 2 → Timeout  
Attempt 3 → Success

### Actual Result

The test stopped on the first timeout instead of allowing the retry logic to continue.

### Error / Unexpected Behaviour

The timeout exception was being raised by the mock, but my retry function was not catching the exception correctly.

---

## Investigation

### My Initial Hypothesis

I initially thought the problem was with unittest.mock and that the mock was not correctly applying the sequence of responses.

### What I Tried

1. Checked the mock configuration.
2. Checked the exception type being raised.
3. Checked the try/except section in the retry function.
4. Ran a smaller isolated mock experiment.

### Result of Each Attempt

**Attempt 1:**
I checked the mock configuration and confirmed that the mock was producing the expected timeout.

**Result:**
The mock itself was working correctly.
**Attempt 2:**
I checked the exception handling in the retry function.
**Result:**
I discovered that the exception being raised by the mock was not being handled by the exception type I had originally used.

**Attempt 3:**
I created a smaller test containing only the mock and the exception.
**Result:**
The smaller test helped confirm the type of exception being raised.

## Research

**Resource(s) consulted:**
https://docs.python.org/3/library/unittest.mock.html
**What I discovered:**
The mock can intentionally raise an exception through its
configured behavior. The retry function therefore needs to
handle the appropriate exception type.

**How I determined that this information was relevant:**
The error occurred exactly when the mocked operation raised
the timeout, so understanding the exception being produced
was directly relevant to the failure.


## Resolution

### Root Cause

My retry function was not handling the same timeout exception that the mocked operation was raising.

### Fix
I corrected the exception handling so that the intended timeout exception was caught by the retry logic.

### Result

The first timeout was caught successfully and the retry logic continued to the next attempt.The test then progressed toward the second and third attempts as expected.


## Lesson Learned
I learned that when debugging a retry mechanism, I should first verify exactly what exception is being produced before changing the retry logic.

---

## Prevention
Before modifying retry logic in the future, I will confirm:

1. What exception is being raised.
2. Where it is raised.
3. Whether the retry function is designed to handle that
   specific exception.

# Blocker 002

## Identification

**Date:**19/08/2026

**Severity:**
- [ ] Low
- [x] Medium
- [ ] High

---

## Problem

### What was I trying to accomplish?

I was implementing the linear backoff delay for consecutive retry attempts.

### Expected Result

I expected the delay to increase linearly after each failed attempt.
For example, using a base delay of 1 unit:
Attempt 1 → 1 unit  
Attempt 2 → 2 units  
Attempt 3 → 3 units

### Actual Result

The delay did not increase as expected. My test output showed the same delay being calculated for multiple attempts.

---

## Investigation

### My Initial Hypothesis

I initially thought the problem was caused by the way I was adding jitter to the delay.

### What I Tried

1. Temporarily removed jitter from the calculation.
2. Printed the calculated delay for each attempt.
3. Compared the attempt number used in the calculation.
4. Tested the calculation with fixed values.

### Result of Each Attempt

**Attempt 1:**

I removed jitter temporarily.

**Result:**

The delay was still incorrect, which indicated that jitter was not the main cause.

**Attempt 2:**

I printed the attempt number and calculated delay.

**Result:**

I discovered that I was using the same attempt value for multiple calculations.

**Attempt 3:**

I corrected the attempt tracking and reran the test.

**Result:**

The delay increased as expected.

---

## Research

**Resource(s) consulted:**
https://strandsagents.com/docs/api/typescript/LinearBackoff/

**What I discovered:**

Linear backoff increases the delay according to a consistent increment rather than increasing exponentially.

**How I determined that this information was relevant:**

The expected delay pattern gave me a reference against which I could compare the values produced by my implementation.

---

## Resolution

### Root Cause

The retry attempt number was not being updated correctly when calculating the delay.

### Fix

I corrected the attempt tracking used by the backoff calculation.

### Result

The calculated delay increased consistently between retry attempts.

## Lesson Learned

I learned that separating the retry attempt count from the backoff calculation makes it easier to reason about the behavior. I also learned that temporarily removing additional complexity, such as jitter, can help isolate the source of a problem.

---

## Prevention
When implementing similar logic, I will test the basic backoff calculation independently before combining it with jitter and retry behavior.
# Blocker 003

## Identification

**Date:** 19/08/2026

**Severity:**
- [x] Low
- [ ] Medium
- [ ] High

---

## Problem

### What was I trying to accomplish?

I was running the unit tests for the retry mechanism.

### Expected Result

I expected the test suite to execute quickly.

### Actual Result

The test took several seconds because the implementation was
actually waiting during the backoff period.

This became inconvenient when repeatedly running the tests.

---

## Investigation

### My Initial Hypothesis

I thought the retry implementation itself might be taking too
long to execute.

### What I Tried

1. Measured the time taken by the test.
2. Checked whether the retry loop was executing more times than
   expected.
3. Investigated how the waiting function could be controlled
   during testing.

### Result of Each Attempt

**Attempt 1:**

Measured the test duration.

**Result:**

The majority of the time was being spent waiting during
backoff.

**Attempt 2:**

Checked the number of retry attempts.

**Result:**

The number of attempts was correct.

**Attempt 3:**

Researched mocking the waiting function.

**Result:**

I learned that the waiting behavior can be replaced during testing so that the test can verify the requested delay without actually waiting for the full duration.

---

## Research

**Resource(s) consulted:**

https://docs.python.org/3/library/unittest.mock.html

**What I discovered:**

Functions used by the retry logic can be replaced during testing with mocks, allowing their calls and arguments to be inspected.

**How I determined that this information was relevant:**

The problem was caused by the test actually waiting, so controlling the waiting function directly addressed the issue.

---

## Resolution

### Root Cause

The unit test was performing real delays instead of isolating the timing behavior.

### Fix

I modified the test approach so that the waiting behavior could be observed without making the test actually wait for the full backoff period.

### Result

The test became much faster while still allowing me to verify that the expected backoff behavior occurred.

# Lesson Learned

I learned that unit tests should isolate the behavior being tested. In this case, I wanted to verify that the correct delay was requested rather than actually waiting for that delay.

## Prevention

When testing time-dependent behavior, I will consider whether the actual passage of time needs to occur or whether the timing dependency can be controlled during the test.
