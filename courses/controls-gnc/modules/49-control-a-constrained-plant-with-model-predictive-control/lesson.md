# Control a Constrained Plant with Model-Predictive Control

Model predictive control optimizes a sequence, applies its first move, observes the new state and solves again. The bounded scalar integrator isolates this mechanism without claiming general nonlinear MPC. Sample index, state and input are normalized; no physical sampling period is implied.

## Model and equations

\[
\min_{|u_j|\leq u_{max}}\sum_{j=1}^{N}x_j^2+0.1\sum_{j=0}^{N-1}u_j^2,\qquad x_{j+1}=x_j+u_j
\]

`x[k+1]=x[k]+u[k]; x[0]=1.5; reference=0`

`J=sum_{j=1..N} x[j]^2 + 0.1*sum_{j=0..N-1} u[j]^2`

`minimize J subject to -limit<=u[j]<=limit; apply first move and re-solve`

Worked example: At x=1.5, N=6 and limit 0.8, the unconstrained first move is about −1.3741, so the constrained optimum starts at −0.8. Its next predicted state is 0.7. The solver optimizes the remaining moves as well; terminal error is computed from their accumulated effect.

## Baseline workflow

Does increasing the horizon necessarily change the first move when the actuator is already saturated?

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Prediction and receding horizon contrasts the initial full optimized plan with sixteen executed receding-horizon moves. Executed control moves displays the actual inputs and both bounds. The first-plan objective sums its computed state and input costs. The projected-gradient residual tests optimality for the declared box.

## Two one-variable sweeps

Increase horizon from 6 to 20: compare first move, predicted terminal error and objective. Reset, then raise the input limit from 0.8 to 2: inspect when the first move becomes unconstrained.

## Intentionally broken case

Broken mode solves the same horizon objective without bounds and applies that unconstrained move. Constraint violation is measured from applied inputs; at sufficiently large limits this fault need not cause a violation.

## Recovery

Reenable optimization bounds and reset the controls. Check every applied move against the limits and require a near-zero box KKT residual, not merely a clipped-looking first command.

## Limiting cases and invariants

- Every healthy predicted and applied input obeys its bound.
- The prediction satisfies x[j+1]=x[j]+u[j] at every step.
- For this scalar regulation problem, later optimal moves shrink; this special structure permits an independent Bellman solution, not a shortcut for arbitrary MPC.

## Independent evidence

Production solves bounded least squares for the complete horizon. An independent scalar Bellman/Riccati construction derives the saturated/free policy and predicted terminal state. Tests check the full objective gradient and state recurrence. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

Clipping a fixed move and dividing error by horizon is not horizon optimization. A feasible input alone does not establish optimality.

## Teach-back

If the first input is unchanged when N grows, what evidence shows the horizon was actually solved? Why is post hoc clipping insufficient in general?

Answer rationale: Inspect the whole optimized plan, its terminal state, objective and KKT residual. Saturation can pin the first move while later moves change. General coupled constraints require solving the constrained objective, not clipping an unconstrained command.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
