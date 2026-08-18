# Meridian Pivot — Assignment 1
# Learning & Reconnaissance Journal

## Assignment Context

**Assignment:** Meridian Pivot — Assignment 1: Solo Recon

**Assigned Tool:** [Retry/Backoff]

**Date Assigned:** [18/8/2026]

**Time Limit:** [3 days]

**Prototype Objective:** [Depict retry/backoff,a syncing service]

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

[In your own words, explain what you currently think the tool is
and what]

---Honestly i am not a tech expert so these things are quite new to me but hey.. we are learning each day

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

**Time:**07:30

**Resource/Source:**
Youtube, https://btholt.github.io/complete-intro-to-realtime/backoff-and-retry

**What I was trying to understand:**
what is retry/backoff

**What I learned:**
Retry is like something that attempts something again in a system after a failure while backoff is what stops the retries after a ttime limit is reached
**What I still did not understand:**
what systems should i create to simulate this and where and also how do i simulate a failure so that i can test this also what is needed for the retry/backoff code snippets
**How this affected my implementation:**

---

### Research Activity 002
What prototype can i build and what tools i need to use to simulate trancient failures and also where all these is done
**Time:**08:32-10:04

**Resource/Source:**

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
I still could not get, the backoff strategy i would use, how i would simulate/control the network timeout for demonstrations
**How this affected my implementation:**

---

### Research Activity 003

**Resource/Source:**

**What I was trying to understand:**

**What I learned:**

**What I still did not understand:**

## 4. Implementation Progress

**How this affected my implementation:**

### Attempt 001

**What I attempted:**

**Expected result:**

**Actual result:**

**What I learned:**

**Next step:**

---

### Attempt 002

**What I attempted:**

**Expected result:**

**Actual result:**

**What I learned:**

**Next step:**

---

## 5. Decisions I Made

### Decision 001

**Decision:**

**Why I made it:**

**Alternative I considered:**

**Why I did not choose the alternative:**

---

## 6. End-of-Day Reflection

### What I Understand Now

- 
- 
- 

### What I Still Need to Solve

- 
- 
- 

### Biggest Discovery

[What was the most important thing you learned today?]

### Biggest Difficulty

[What challenged you most?]

### Next Priority

[What is the single most important thing to accomplish next?]
