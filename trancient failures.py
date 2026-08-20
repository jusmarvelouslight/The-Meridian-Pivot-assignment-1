import time
import random
from unittest.mock import Mock


# ============================================================
# 1. SIMULATED NETWORK REQUEST
# ============================================================
# This represents the operation that normally talks to a
# real network/API.
#
# It has a 50% chance of experiencing a temporary timeout.
# ============================================================

def network_request():
    failure_chance = 0.5

    if random.random() < failure_chance:
        raise TimeoutError("Temporary network timeout")

    return "Data received successfully"


# ============================================================
# 2. RETRY FUNCTION
# ============================================================
# This function is responsible for:
#
# - Calling the network request
# - Detecting a timeout
# - Retrying
# - Applying linear backoff
# - Applying full jitter
# - Stopping after the maximum number of attempts
# ============================================================

def retry_request(request, max_retries=5, base_delay=1):

    for attempt in range(1, max_retries + 1):

        print(f"\nAttempt {attempt}/{max_retries}")

        try:

            # Try the network operation
            result = request()

            # If no exception occurred, the request succeeded
            print("Request succeeded.")
            print(f"Result: {result}")

            return result

        except TimeoutError as error:

            print(f"Request failed: {error}")

            # ------------------------------------------------
            # Check whether we have reached the final attempt
            # ------------------------------------------------

            if attempt == max_retries:

                print("Maximum retry attempts reached.")
                print("Request failed permanently.")

                return None

            # ------------------------------------------------
            # LINEAR BACKOFF
            # ------------------------------------------------
            #
            # Attempt 1 -> 1 second
            # Attempt 2 -> 2 seconds
            # Attempt 3 -> 3 seconds
            # etc.
            # ------------------------------------------------

            backoff = base_delay * attempt

            # ------------------------------------------------
            # FULL JITTER
            # ------------------------------------------------
            #
            # Instead of always waiting exactly the
            # backoff amount, choose a random value between
            # 0 and the backoff limit.
            # ------------------------------------------------

            wait_time = random.uniform(0, backoff)

            print(
                f"Linear backoff limit: {backoff:.2f} seconds"
            )

            print(
                f"Full jitter selected: {wait_time:.2f} seconds"
            )

            # Actually wait before retrying
            time.sleep(wait_time)

            print("Retrying...")


# ============================================================
# 3. REALISTIC RANDOM FAILURE SIMULATION
# ============================================================

print("\n")
print("==============================================")
print("RANDOM TRANSIENT FAILURE SIMULATION")
print("==============================================")

result = retry_request(network_request)

if result is not None:
    print("\nFinal result: SUCCESS")
else:
    print("\nFinal result: FAILURE")


# ============================================================
# 4. unittest.mock CONTROLLED TESTING
# ============================================================
#
# The random simulation above is useful for seeing realistic
# behavior.
#
# But random behavior is not ideal for testing because we
# cannot guarantee exactly when a timeout will happen.
#
# unittest.mock allows us to control the failures.
# ============================================================


# ------------------------------------------------------------
# SCENARIO 1
# Immediate success
# ------------------------------------------------------------

print("\n")
print("==============================================")
print("SCENARIO 1: IMMEDIATE SUCCESS")
print("==============================================")

mock_request_1 = Mock()

mock_request_1.return_value = "Data received successfully"

result = retry_request(mock_request_1)

print("\nExpected:")
print("First attempt succeeds.")
print("No retry should occur.")


# ------------------------------------------------------------
# SCENARIO 2
# Temporary timeout followed by successful recovery
# ------------------------------------------------------------

print("\n")
print("==============================================")
print("SCENARIO 2: TIMEOUT -> SUCCESS")
print("==============================================")

mock_request_2 = Mock()

mock_request_2.side_effect = [
    TimeoutError("Temporary timeout"),
    "Data recovered successfully"
]

result = retry_request(mock_request_2)

print("\nExpected:")
print("Attempt 1 -> timeout")
print("Backoff + jitter")
print("Attempt 2 -> success")


# ------------------------------------------------------------
# SCENARIO 3
# Repeated timeout resulting in failure
# ------------------------------------------------------------

print("\n")
print("==============================================")
print("SCENARIO 3: REPEATED TIMEOUT")
print("==============================================")

mock_request_3 = Mock()

# Every call will produce a TimeoutError
mock_request_3.side_effect = TimeoutError(
    "Persistent network timeout"
)

result = retry_request(
    mock_request_3,
    max_retries=5
)

print("\nExpected:")
print("Every attempt -> timeout")
print("Backoff + jitter after each failed attempt")
print("Maximum retries reached")
print("Final result -> failure")