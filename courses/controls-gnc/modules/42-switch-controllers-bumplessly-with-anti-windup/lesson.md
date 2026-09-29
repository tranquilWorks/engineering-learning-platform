# Switch Controllers Bumplessly with Anti-Windup

Bumpless transfer initializes controller memory to reproduce the command already being applied. Anti-windup then reconciles that memory with actuator saturation. This is a declared 0.01-second sampled Euler plant/controller model with normalized output and command.

## Model and equations

\[
z_{k+1}=z_k+\Delta t\left[k_i(r_k-x_k)+k_{aw}(u_k-u_{raw,k})\right]
\]

`x[k+1]=x[k]+0.01*(-x[k]+u[k])`

`u_raw=2*(r-x)+z; u=clip(u_raw,-limit,limit)`

`z[k+1]=z[k]+0.01*(1.2*(r-x)+k_aw*(u-u_raw))`

Worked example: Manual command is min(0.7,limit). At the three-second switch, setting z=u_manual−2(r−x) makes u_raw equal the preceding manual command exactly. The reference drops from 2 to 0.2 at seven seconds.

## Baseline workflow

Can a saturated actuator hide a requested-command jump? Compare the applied switch bump with the integral and requested-command histories.

Run the default controls, record the metrics, and explain the plotted quantities before changing a setting. The first plot shows output and reference. The second retains actual z, raw command and saturated command. Peak integral state is max|z| in both modes. Recovery requires the output to remain within 0.04 of 0.2 for the rest of the window; an unobserved recovery is labeled a censored five-second lower bound.

## Two one-variable sweeps

Raise anti-windup gain from 4 to 12/s and compare integral unwinding after the reference drop. Reset, then raise actuator limit from 1.2 to 3: compare saturation duration and recovery; faster anti-windup need not minimize every settling measure.

## Intentionally broken case

Broken mode starts z at zero on switching and disables back-calculation. It still obeys actuator limits, so the integrator can accumulate error that the actuator cannot realize.

## Recovery

Disable broken mode, restore gain 4/s and limit 1.2, and verify a zero applied bump plus the actual integral history. Check the recovery-observed indicator before quoting a settling time.

## Limiting cases and invariants

- At k_aw=0 the healthy switch is still bumpless, but no back-calculation acts afterward.
- Both manual and automatic applied commands satisfy the selected limit.
- A peak command is not a peak integral state, and a censored time is not an observed recovery.

## Independent evidence

A separately written piecewise-affine state transition handles unsaturated and saturated regions, independently checking the scalar production recurrence. Five retained scenarios cover baseline, each one-variable sweep, fault and exact recovery. Absolute and relative tolerances remain 1e-8. The reference does not import or consume the production result.

## Common mistakes

Do not compare different quantities across modes. A small final integral state can conceal a large earlier windup peak.

## Teach-back

Why can peak |z| exceed the command limit? What additional evidence is required before reporting a recovery time?

Answer rationale: Only u is clipped; z is controller memory and can be much larger. Inspect recovery-observed and ensure all later samples stay inside the stated band. A censored lower bound cannot be presented as a successful recovery.

Use the Course checkpoint section to assemble your own evidence. These are authored self-checks, not measured learner outcomes or hardware qualification.
