# Lessons Learned — SANDRAY-v2 Debugging Session

## 1. Overview
This document records engineering lessons identified during iterative debugging and recovery of the SANDRAY-v2 system UI and system_state architecture.

---

## 2. Critical Failure Patterns Observed

### 2.1 Premature architectural modification
- Multiple structural changes were introduced while the system was unstable.
- UI, layout, and system_state layers were modified concurrently.

Impact:
- Increased system instability
- Compounding integration failures

---

### 2.2 Lack of rollback-first strategy
- Git history existed but was not immediately used as primary recovery mechanism.
- Incremental patching was attempted instead of restoring stable commit.

Impact:
- Extended debugging cycles
- Delayed recovery to stable state

---

### 2.3 Interface contract drift
- system_panels.py expected functions not consistently implemented in system_state.py.
- Fields were added reactively during debugging instead of being defined upfront.

Impact:
- ImportError and KeyError cascades
- Inconsistent schema across modules

---

### 2.4 UI composition errors
- Panels were wrapped multiple times (Panel inside Panel).
- Separation between data layer and presentation layer was violated.

Impact:
- Nested UI artifacts
- Reduced clarity and maintainability

---

### 2.5 Speculative patching during unstable state
- Fixes were applied without verifying system-wide impact.
- Missing APIs were inferred instead of validated against a contract.

Impact:
- Repeated regressions
- Non-converging debugging loop

---

## 3. Assistant-contributed failure modes

- Overuse of incremental fixes instead of stabilization
- Delayed recommendation of Git rollback despite availability
- Introduction of speculative code during incomplete system understanding
- Failure to enforce strict interface contracts early
- Simultaneous modification of multiple dependent layers

---

## 4. Correct engineering principles

- Restore known-good state before applying fixes
- Maintain strict interface contracts between modules
- Avoid simultaneous modification of dependent systems
- Prefer rollback over patching when drift is large
- Separate data, logic, and presentation layers strictly

---

## 5. Summary

The instability was caused by architectural drift from iterative modifications without a stable baseline, rather than isolated bugs.


---

## 6. Process Enforcement Failure (Meta Lesson)

### 6.1 Stated vs enforced behavior gap
- A “Lessons Learned” document was introduced as a mandatory constraint before actions.
- This constraint was acknowledged but not consistently enforced during execution.

Impact:
- Continued proposal of changes during unstable system state
- Violation of rollback-first principle in practice
- Reintroduction of incremental patching behavior despite explicit instruction to avoid it

---

## 7. Operational Correction Requirement

To prevent recurrence:

- Lessons Learned must function as a **hard gate**, not advisory guidance
- Any proposed action must first check:
  - system stability state
  - availability of rollback option
  - risk of architectural modification

If any condition is false:
- action must be stopped
- rollback must be recommended instead of repair

---

## 8. Accountability Summary

- The failure was not in defining constraints, but in enforcing them consistently during execution.
- This resulted in deviation from agreed operational rules under iterative debugging pressure.

