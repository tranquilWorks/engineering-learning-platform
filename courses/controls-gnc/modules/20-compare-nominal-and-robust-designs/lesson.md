# Compare Nominal and Robust Designs

**Guiding question:** What inputs, observable effects, and failure modes matter when you compare Nominal and Robust Designs?

Compare a nominal gain with a conservative design across the same uncertainty envelope. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

The robust design should improve the difficult low-gain/high-drag corner while using more command nominally. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$u=K(r-v)$$ — Both designs share structure; their gain is selected against different plant sets.
- $$J_w=\max_{p\in\mathcal P}J(K,p)$$ — The robust choice reduces worst-case error at the cost of more effort.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `actuator_gain_ratio` through [0.5, 1.0, 1.5]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `drag_ratio` through [0.5, 1.0, 2.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case reverses actuator sign, violating the uncertainty set both designs assumed. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case and restore a plant inside the certified uncertainty family. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P20 lesson: Compare Nominal and Robust Designs

## Guiding question

What inputs, observable effects, and failure modes matter when you compare Nominal and Robust Designs?

## Compounds on P19

P19 held one controller fixed while actuator effectiveness and drag changed. P20 keeps that
transparent uncertain speed plant, then compares one controller tuned for the matched model with a
second controller selected against the declared 25-point positive uncertainty grid.

## Mental model

A nominal design is like choosing cruise-control gains on a calm, level road. A robust design asks
which candidate has the smallest worst tracking-error integral over the roads that were explicitly
put on the test map, while rejecting candidates that exceed the declared command-effort budget.
The answer can be more conservative at the exact center and still be preferable at the difficult
edge. Neither label replaces the need to state the map, objective, constraint, and failure boundary.

The plant still obeys P19's exact held-input recurrence:

```text
alpha = exp(-a*dt),  beta = (b/a)*(1-alpha)
v[k+1] = alpha*v[k] + beta*u[k]
```

The nominal controller uses a model-matched feedforward command plus proportional feedback. The
robust controller uses proportional-integral feedback. Its integral state accumulates tracking
error in metres, so `Kp` has units `1/s`, `Ki` has units `1/s^2`, and both command terms have units
`m/s^2`.

## What the comparison reveals

- At the matched plant, the nominal controller has the smaller tracking ISE and reaches the target
  faster. That is its intended operating point.
- On the 25 declared actuator/drag points, the selected PI candidate has a smaller worst-case
  12-second ISE while every grid scenario remains stable and below the effort limit for the `1 m/s`
  design step at `dt=0.02 s`. Other reference amplitudes are exploratory, not effort guarantees.
- Integral action makes the robust controller's stable positive-plant equilibrium error exactly
  zero, but a finite 12-second run can still end before a slow worst-corner transient settles.
- The robust design can use more effort at the worst corner. Robustness is a trade, not dominance on
  every metric or every plant.

## Deliberately broken assumption

The finite design search includes only positive actuator effectiveness. Reverse actuator polarity
and positive error drives speed in the wrong direction. Both controllers then have a discrete pole
magnitude above one and the bounded simulator terminates a diverging trace before it can consume an
unbounded numerical range. Restoring positive polarity in a fresh call recovers the exact baseline;
no controller state leaks between runs.

## Misconceptions to correct directly

- “Robust” does not mean best at the nominal point.
- A finite uncertainty grid is not proof for values between grid points or outside its limits.
- Zero asymptotic PI error is not the same as zero error at the finite experiment horizon.
- Lower worst-case tracking error does not mean lower command effort.
- Reversed polarity is a structural failure, not a larger positive gain error.
- Explicit enumeration is a transparent comparison, not a toolbox synthesis or universal optimum.
- Independent reference simulation is not MATLAB-runtime, UI, bench, HIL, or field evidence.

Ask one observation question at a time. Request the teach-back only after executable checks pass.

## Source walkthrough

# P20 walkthrough: Compare Nominal and Robust Designs

## Learner sequence

1. Read the guiding question and P19 plant recurrence before running code.
2. Predict only which design has smaller tracking ISE on the exactly matched plant.
3. Visualize baseline speed and command. Observe the nominal design's faster matched response and
   compare tracking ISE with command-effort integral.
4. Read the finite selection table: 12 PI candidates, 25 positive plant scenarios, stability on
   every scenario, and a `90 m^2/s^3` worst-effort limit for a `1 m/s` step, 12-second horizon,
   and `dt=0.02 s`. Other reference amplitudes are exploratory.
5. Sweep only actuator gain ratio while drag stays one. Compare both designs' ISE and final error.
6. Explain the changed view from command effectiveness and integral correction, not from MATLAB
   syntax or the word “robust.”
7. Reset actuator gain to one and sweep only drag. Observe how extra loss changes both finite-time
   tracking and required steady command.
8. Explain why the nominal feedforward is exact only when the model ratio matches and why stable PI
   has zero asymptotic error even though its finite-horizon final error remains visible.
9. Reverse actuator polarity. Identify pole magnitude above one and bounded early termination as a
   structural failure outside the positive design grid, then restore positive polarity.
10. Run `run_module_checks("P20")`, answer one interpretation prompt at a time, and give the required
    two-sentence teach-back.

No MATLAB-runtime, rendered-UI, or physical evidence is claimed by this source walkthrough.

## Source checks

# P20 checks: Compare Nominal and Robust Designs

Run `run_module_checks("P20")`, then answer one prompt at a time:

1. Why can the nominal design have smaller matched-plant ISE while the robust design has smaller
   worst-case ISE over the declared 25-point uncertainty grid?
2. What do the candidate set, 25-scenario grid, stability test, and command-effort limit each add to
   the meaning of “robust” here, and which reference, horizon, and sample interval bound that claim?
3. Why is the robust controller's exact zero steady error compatible with nonzero final error after
   a finite 12-second worst-corner run?
4. Which metrics expose the trade between tracking and command effort?
5. Why does reversed actuator polarity invalidate both designs' positive-gain evidence?

## Teach-back

In exactly two sentences, name the uncertain inputs, observable effects, and nominal-versus-robust
tradeoff. Then state the declared uncertainty boundary and explain the reversed-polarity symptom.

The source and independent oracle provide static and simulated evidence only. No MATLAB-runtime,
rendered-UI, numerical-fidelity, bench, HIL, field, or production validation is claimed.
