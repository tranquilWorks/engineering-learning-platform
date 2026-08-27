# Watch a Mass-Spring-Damper Respond

**Guiding question:** How do mass, stiffness, and damping determine visible motion?

Relate inertia, energy storage, and dissipation to a forced mechanical response. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

More damping should reduce ringing without changing the static displacement F/k. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$m\ddot{x}+c\dot{x}+kx=F$$ — Force divides among inertia, damping, and spring reaction.
- $$\omega_n=\sqrt{k/m},\quad\zeta=c/(2\sqrt{km})$$ — Natural frequency and damping ratio predict the visible motion.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `damping_ns_m` through [0.2, 0.8, 2.5]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `stiffness_n_m` through [1.0, 4.0, 10.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case uses an explicit integration step too large for the fastest mode, so numerical energy grows even though the physical system is damped. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case to restore a time step that resolves the natural period. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# Lesson: Watch a Mass-Spring-Damper Respond

## Guiding question

How do mass, stiffness, and damping determine visible motion?

## Mental model

A mass stores momentum, a spring stores potential energy, and a damper removes energy. Their balance determines oscillation, settling, and overshoot.

## What to manipulate

Use `interactive.m`. Change one lever at a time before combining effects.

## First observation

Lower damping until the response rings, then raise it until motion becomes sluggish. Change mass and stiffness separately and notice that both alter natural frequency in different physical ways.

## Common mistakes

- More damping is not always faster.
- A stable system can still be too slow or too oscillatory.
- The same-looking step response can hide different physical parameters.

## Completion standard

The learner can explain the baseline, identify what each lever changes, diagnose the deliberately broken case, and pass `run_checks.m`.

## Source walkthrough

# Walkthrough: Watch a Mass-Spring-Damper Respond

1. Run `experiment.m` and inspect the baseline before changing anything.
2. State what each axis physically or computationally represents.
3. Open `interactive.m`.
4. Change one lever in the direction suggested by the lesson.
5. Describe what changed and what did not.
6. Return to the baseline.
7. Change a second lever independently.
8. Run the deliberately broken case and identify the violated assumption.
9. Run `run_checks.m`.
10. Give a two-sentence teach-back: mechanism first, consequence second.

## Source checks

# Checks: Watch a Mass-Spring-Damper Respond

## Observation check

Explain which plotted quantity responds first when the primary lever changes and why.

## Broken-case check

Name the exact assumption violated by the deliberately broken case. Do not answer only with “the model is wrong.”

## Transfer check

Describe one professional or physical system where the same mechanism would matter.

## Executable check

Run:

```matlab
run_checks
```

All assertions must pass before the module is marked complete.
