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
