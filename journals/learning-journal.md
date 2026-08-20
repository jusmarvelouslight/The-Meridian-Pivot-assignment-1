# Meridian Pivot — Assignment 1
# Learning & Reconnaissance Journal

## Assignment Context

**Assignment:** Meridian Pivot — Assignment 1: Solo Recon

**Assigned Tool:** Retry/Backoff

**Date Assigned:** 18/8/2026

**Time Limit:** 3 days

**Prototype Objective:** Depict retry/backoff,a syncing service

---

# Day 1

## 1. Initial Position

### What I Already Know

- I know that retry/backoff is one of the tools we were asked to build a syncing service with
- function might be derived from its name

### What I Do Not Know

- What is Retry/backoff
- How do i implement both of them in my syncing service
- Why are they both necessary

### Initial Understanding of the Tool

Honestly i am not a tech expert so these things are quite new to me but hey.. we are learning each day

## 2. Learning Objectives

By the end of the solo reconnaissance period, I need to be able to:

- [ ] Explain what the tool does
- [ ] Explain the basic concepts/components involved
- [ ] Set up the tool/environment
- [ ] Build the required mini-prototype
- [ ] Test whether the prototype works
- [ ] Explain the final implementation
- [ ] Troubleshoot basic problems independently

---

## 3. Research Log

### Research Activity 001

**Time:**07:30 AM-10:38 AM

**Resource/Source:**

Youtube, https://btholt.github.io/complete-intro-to-realtime/backoff-and-retry

**What I was trying to understand:**
what is retry/backoff

**What I learned:**

Retry is like something that attempts something again in a system after a failure while backoff is what stops the retries after a ttime limit is reached

**What I still did not understand:**

what systems should i create to simulate this and where and also how do i simulate a failure so that i can test this also what is needed for the retry/backoff code snippets

**How this affected my implementation:**

if i didnt get too understand what retry/backoff was then i could not even come up with the system itself

---

### Research Activity 002
What prototype can i build and what tools i need to use to simulate trancient failures and also where all these is done.

**Time:**08:32-10:04AM

**Resource/Source:**

https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter

**What I was trying to understand:**
i was tryng to understand the prototype that i need to build in order to simulate trancient failures turns out there are many types of trancient failures
**What I learned:**
i learnt that first of all retry/backoff is not a webhook itself but it is an error handling rule or helper when sending webhooks. also,i learnt that there are many types of trancient failures that the mechanism could solve the tree that i learnt were Network timeout,Resource exhaustion and service overload.Although i did not delve much deeper into all of them,i tried to understand each and every one of the three but i identified network timeout as the trancient failure scenario for my prototype. secondly, i understood that it is backend work and i do not need to create a website or chatbot for the same.
The tools that i found out were

I selected this failure scenario because it seemed understandibletherefore,my prototype will demonstrate a timed out operation using a back off strategy.
i intend to test
1.Immediate success
2.temporary timeout followed by successful recovery
3.repeated timeout resulting in failure

**What I still did not understand:**

I still could not get, the backoff strategy i would use, how i would simulate/control the network timeout for demonstrations also what jitters are and how i can incorporate in the system

**How this affected my implementation:**

If i did not know this, then i would not even be anyehere near simulating network failure ergo the whole purpose of this sole recon would be rendered moot

---

### Research Activity 003
Backoff strategy,Jitters,simulation of the trancient failure.

**Time:**20:45 PM-23:18

**Resource/Source:**

https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
https://backoff-utils.readthedocs.io/en/latest/strategies.html

**What I was trying to understand:**
Different backoff strategies and their ease of use,what is a jitter and how i`m i going to use it
**What I learned:**
I learnt that there are 5 types of backoff strategies
1. Linear backoff strategy
2. Eponential backoff strategy
3. fixed backoff strategy
4. Polynomial backoff strategy
i decided to pick linear backoff because its new to me and also with the deadlines in mind i had to choose one that could not give me a hard time handling.
i learnt that a jitter helps to add some amount of time to the delay time. Ichose to go with a full jitter with the interest of time at heart
Now to demonstrate/simulate the trancient failuure which is network timeout in my case, i learnt that there are many tools that can help one to simulate a trancient environment for testing but one particular one called unittest.mock caught my attention because it is 100% free,Easy to simulate multiple failure modes,Focuses on business logicconsidering that northstar may be a business company and finally Fast and deterministic.


## 4. Implementation Progress

**How this affected my implementation:**

### Attempt 001

**What I attempted:**

I created the initial Python project structure and began designing the retry function.
**Expected result:**

I expected to have a function structure that could receive an operation and retry it when a timeout occurred
**Actual result:**

The function structure was created, but I had not yet implemented the retry behavior.
**What I learned:**

I realized that I needed to clearly separate the retry mechanism from the operation being retried.
**Next step:**

Understand how the operation can be passed into the retry function and controlled during testing.

---

### Attempt 002

**What I attempted:**
I created a small `unittest.mock` experiment to control the result of successive calls.
**Expected result:**
I expected the mock to produce two timeout failures followed by a successful result.
**Actual result:**
The first version of my experiment did not behave as expected.
**What I learned:**
I discovered that I had misunderstood how the mock's side_effect behavior works.
**Next step:**
Review the documentation and modify the experiment before connecting it to the actual retry logic.

---

## 5. Decisions I Made

### Decision 001

**Decision:**

**Why I made it:**
Python is the language I think is comfortable for starters, which allows me to focus my learning effort on retry/backoff rather than learning an unfamiliar programming language at the same time.
**Alternative I considered:**
Using another language.
**Why I did not choose the alternative:**
i never wanted any other language

---

### Decision 002

**Decision:**

Use a network timeout as the transient failure scenario.

**Why I made it:**

A timeout can represent a temporary failure where retrying the operation may eventually succeed.

**Alternative I considered:**

Using another type of failure.

**Why I did not choose the alternative:**

The timeout scenario provides a clear and understandable example of why retry/backoff can be useful.And also not time consuming to learn which is a factor i always consider during the phase of this assignment

---

### Decision 003

**Decision:**

Use linear backoff with jitter.

**Why I made it:**

I wanted a backoff strategy that was simple enough to understand and demonstrate clearly while still showing that retry attempts do not happen immediately one after another.

**Alternative I considered:**

Exponential backoff

**Why I did not choose the alternative:**

For this small prototype, I considered exponential backoff more complex than necessary for demonstrating the core concept.

---

### Decision 004

**Decision:**

Use unittest.mock to simulate network timeout behavior.

**Why I made it:**

A real network timeout would be difficult to reproduce reliably.Using a mock allows me to control the sequence of failures and successes during testing.

**Alternative I considered:**

Making real network requests and waiting for them to timeout.

**Why I did not choose the alternative:**

The behavior would be unpredictable and would make testing slower and less reproducible.


### Biggest Discovery
My biggest discovery was that retrying is not simply about repeating an operation after it fails. The retry mechanism needs a deliberate policy determining when to retry, how long to wait, and when to stop.


### Biggest Difficulty
The most difficult part for me was fiuring out the python.i never knew anything remotely connected with python but at least now i might say im not the same as i was before

