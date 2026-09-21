# Coordinate Actions with a Behavior Tree

**Guiding question:** What inputs, observable effects, and failure modes matter when you coordinate Actions with a Behavior Tree?

## Concept and prediction

A behavior tree coordinates actions through a small status algebra: SUCCESS, FAILURE, and RUNNING. Sequence nodes advance on success, stop on failure, and resume the running child later. Decorators can modify status, such as retrying a failed grasp within a strict limit.

Predict the completion tick for five navigation ticks, two failed grasp attempts, one successful grasp, and three delivery ticks. Then predict what happens if RUNNING progress is reset on every root tick.

## Model, symbols, and equations

- $$S_{seq}=\begin{cases}FAILURE&\text{first failed child}\\RUNNING&\text{first running child}\\SUCCESS&\text{all children succeed}\end{cases}$$ — sequence status rule.
- $$N_{attempt}\le N_{retry}+1$$ — bounded retry contract.
- $$k_{done}=k_{nav}+N_{attempt}+k_{deliver}$$ — nominal tick accounting for this deterministic tree.

Tick is a dimensionless discrete execution unit. Node codes are 0 Navigate, 1 Grasp, 2 Deliver, 3 Done, and 4 Failed. Progress is local to a node and persists only while that tree instance remains active.

## Manipulation: two one-variable sweeps

1. Sweep `navigate_ticks` through [2,5,10]. Completion time should grow one-for-one while state order remains unchanged.
2. Restore baseline, then sweep `retry_limit` through [0,3,6]. Too few retries cause explicit failure; enough retries allow the scripted grasp success.

The first plot shows which node owns each tick. The mechanism plot makes retained child progress visible.

## Evidence and limiting cases

The independent reference derives the deterministic tick schedule from the composite rules; production executes a separate stateful tick loop.

- A one-tick successful child advances immediately.
- Zero retries allows exactly the first grasp attempt.
- An infinite RUNNING action prevents a sequence from reaching later children unless preempted by a higher-level policy.

This is software behavior-orchestration evidence, not actuator execution, real-time scheduling, robot, HIL, or field validation.

## Intentionally broken assumption

**RUNNING child reset.** Broken mode discards navigation progress each root tick. A five-tick navigation leaf repeatedly returns its first RUNNING result and starves every later action.

## Explanation and recovery

Restore persistent child state, propagate RUNNING without translating it to FAILURE, and keep retries bounded. Completion requires both correct control flow and action-level progress.

## Common mistakes

- Treating RUNNING as FAILURE or SUCCESS at a composite boundary.
- Retrying forever without a fault exit.
- Hiding side effects inside conditions that may be ticked repeatedly.
- Assuming behavior-tree ticks are equivalent to hard real-time deadlines.

## Focused check and teach-back

At baseline, account for every completion tick and grasp attempt. Reproduce the reset stall, recover persistence, and teach back sequence status, retry semantics, units, and the difference between orchestration state and physical action.
