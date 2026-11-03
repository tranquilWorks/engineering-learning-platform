## P49 evidence task

If the first input is unchanged when N grows, what evidence shows the horizon was actually solved? Why is post hoc clipping insufficient in general?

Before running: Does increasing the horizon necessarily change the first move when the actuator is already saturated?

Collect three records: the default plots and metrics; one change from the stated sweeps with the other control fixed; and the fault followed by restored defaults. Record parameter values and units beside each observation.

Prediction and receding horizon contrasts the initial full optimized plan with sixteen executed receding-horizon moves. Executed control moves displays the actual inputs and both bounds. The first-plan objective sums its computed state and input costs. The projected-gradient residual tests optimality for the declared box.

### Reasoning rubric

- Model: use `x[k+1]=x[k]+u[k]; x[0]=1.5; reference=0` to explain the observed quantity rather than repeating a metric label.
- Evidence: Every healthy predicted and applied input obeys its bound. Show where your plot or numerical record tests this statement.
- Diagnosis: Broken mode solves the same horizon objective without bounds and applies that unconstrained move. Constraint violation is measured from applied inputs; at sufficiently large limits this fault need not cause a violation. Identify the measured consequence in your record.
- Recovery and scope: Reenable optimization bounds and reset the controls. Check every applied move against the limits and require a near-zero box KKT residual, not merely a clipped-looking first command. State this limit: For this scalar regulation problem, later optimal moves shrink; this special structure permits an independent Bellman solution, not a shortcut for arbitrary MPC.

### Check your explanation

Inspect the whole optimized plan, its terminal state, objective and KKT residual. Saturation can pin the first move while later moves change. General coupled constraints require solving the constrained objective, not clipping an unconstrained command.

A complete answer includes the calculation or recurrence, an observed comparison with units, fault/recovery evidence and the stated limitation. Revisit the lesson if the explanation depends only on a changing headline number. This is a self-assessment; no learner score is stored.


---

## P49 course checkpoint

**Predict and calculate.** Check applied receding-horizon commands against both optimization feasibility and actual state constraints.

Use `x[k+1]=x[k]+u[k]; x[0]=1.5; reference=0; J=sum_{j=1..N} x[j]^2 + 0.1*sum_{j=0..N-1} u[j]^2; minimize J subject to -limit<=u[j]<=limit; apply first move and re-solve` with the conventions in the lesson. Work one baseline value by hand before running. The live controls are **Prediction horizon**, **Input limit**.

**Collect evidence.** Save the default result, then perform the lesson's two one-variable sweeps separately. Record exact parameters, units, the `response` and `mechanism` plots, and the quantity that discriminates your prediction. Explain what stayed invariant as well as what changed.

**Fault and recovery.** Enable **Enable the intentionally broken case** at the same inputs. Explain which governing term is changed or omitted, show its effect on the actual trajectory, matrix or criterion, then disable it and use **Reset parameters**. Confirm recovery reproduces the baseline rather than merely a more favorable number.

### Expected reasoning

MPC repeatedly solves a constrained horizon problem. A decreasing objective does not excuse an infeasible input or state, and finite horizon plus a fallback is not automatically a stability proof.

### Model boundary

This bounded scalar optimizer is not a general nonlinear MPC implementation.

### Reasoning rubric

1. State the model, units, sign convention and independently worked value.
2. Explain both sweeps using this lesson's governing relation and recorded evidence.
3. Diagnose the actual fault mechanism and exact-input recovery.
4. Defend the stated boundary and link this result to the cumulative portfolio **A-CONSTRAINTS**.

This is authored self-assessment guidance. No learner completion, score or effectiveness result has been recorded.
