# Enforce Safety with a Control Barrier Filter

A control barrier filter limits closing velocity using the current clearance, not just the initial clearance. The experiment uses a sampled integrator with initial h=0.4 m and no disturbances or actuator dynamics.

## Model and equations

\[
h_{k+1}\geq (1-\alpha\Delta t)h_k\geq 0\quad\text{if }0\leq\alpha\Delta t\leq1
\]

`h=x-x_min; dh/dt=u; u_nom=-v_close`

`u[k]=max(u_nom,-alpha*h[k]); h[k+1]=h[k]+dt*u[k]`

`dt=0.01 s; h[k+1]>=(1-alpha*dt)*h[k]`

Worked example: At alpha=2/s and nominal closing speed 1.5 m/s, the initial command is max(−1.5,−0.8)=−0.8 m/s. One sample later h=0.392 m and the bound changes to −0.784 m/s. Reusing −0.8 indefinitely would violate safety.

## Baseline workflow

Should the safe trajectory cross h=0 if every command is reevaluated? State the sample-period condition your answer requires.

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. Safety margin over time includes the zero boundary. State-dependent barrier filter shows applied and nominal velocities and u+alpha*h. A nonnegative residual certifies the sampled step under the declared integrator assumptions.

## Two one-variable sweeps

Raise barrier gain from 2 to 8/s: the nominal command may initially be allowed, then intervention begins as clearance falls. Reset, then raise closing speed from 1.5 to 4 m/s: compare requested and applied speeds.

## Intentionally broken case

Broken mode bypasses the filter and continuously applies the selected nominal closing speed. At the default speed, clearance crosses zero within three seconds; slower closing can stay positive throughout this finite window. No control setting is secretly replaced.

## Recovery

Disable broken mode and reset controls. Inspect the entire clearance history, not just its first sample, and verify a nonnegative minimum barrier residual.

## Limiting cases and invariants

- For alpha*dt<=1, nonnegative current clearance implies nonnegative next clearance.
- At h=0 the healthy controller refuses negative velocity.
- If nominal velocity already satisfies the barrier, intervention is zero; this does not remove the need to reevaluate it later.

## Independent evidence

A closed-form linear approach followed by a geometric decay independently predicts the sampled clearance sequence and signature. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

A safe first command is not a safe fixed command forever. The continuous inequality also needs a sample/update argument before claiming discrete-time safety.

## Teach-back

Derive h[k+1]>=(1−alpha*dt)h[k] and explain why this browser range satisfies it. What physical effects are excluded?

Answer rationale: Substitute u>=−alpha*h into the Euler integrator. Here alpha*dt<=0.08, so the multiplier stays nonnegative. Delay, disturbances and actuator lag are excluded; the demonstration does not certify a real robot.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
