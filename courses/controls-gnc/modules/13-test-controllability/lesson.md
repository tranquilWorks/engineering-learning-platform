# Test Controllability

**Guiding question:** What inputs, observable effects, and failure modes matter when you test Controllability?

Use rank and reachability energy to distinguish weak from missing control authority. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Zero coupling should make position unreachable even though rate is directly actuated. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$\mathcal C=[B\;AB]$$ — Full row rank is required to reach arbitrary two-state targets.
- $$W_c=\sum A^kBB^T(A^T)^k$$ — The Gramian reveals how much command energy reachability costs.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `input_gain` through [0.25, 1.0, 2.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `coupling` through [0.25, 1.0, 2.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case removes coupling between rate and position, dropping controllability rank. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case to restore the state-to-state path. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P13 lesson: Test Controllability

## Guiding question

What inputs, observable effects, and failure modes matter when you test Controllability?

## Compounds on

P12 — Recover from Integrator Windup. P12 showed that an actuator may apply less effort than a
controller requests. P13 separates another issue: even before limits are imposed, the placement of
an input may leave a state direction unreachable.

## Mental model

Imagine a cart model with normalized position and rate coordinates. The actuator changes rate.
Position changes only because rate is coupled into the position equation. The two columns of
`[B, A*B]` ask:

- where does the input point immediately?
- where do the dynamics carry that input effect next?

Independent columns mean both normalized state directions are controllable. The finite-horizon
matrix in the experiment repeats the same idea for every held command sample and makes the target
transfer visible.

## What the two levers mean

- **Actuator effectiveness** scales how strongly every command sample enters the state. A weak but
  nonzero actuator can retain rank while demanding much more command energy.
- **Maneuver time** changes how many input effects can accumulate and flow from rate into position.
  More time can improve the weakest reachability direction and lower peak command.

Neither lever changes the target, damping, state scales, or the other lever during its sweep.

## Deliberately broken assumption

The broken case sets kinematic coupling to zero. Rate still answers a probe, so the actuator is not
dead, but position is frozen. The controllability rank falls from two to one and a position target
retains a one-metre terminal residual. That equality-constrained target has no minimum-energy
solution—effort is N/A, not zero. Restoring coupling recovers both rank and the transfer.

## Misconceptions to correct directly

- Full rank does not mean low effort, good conditioning, or compliance with an actuator limit.
- A small singular value is coordinate dependent; this lesson declares fixed state scales before
  comparing it.
- Controllability concerns whether input can move state. Whether a sensor can reveal state is the
  observability question in P14.
- `rank(ctrb(A,B))` is not the lesson. The governing columns, state effects, and failed assumption
  must remain visible.

Ask one observation question at a time, then request the teach-back only after executable checks.

## Source walkthrough

# P13 walkthrough: Test Controllability

## Read and predict

Read the guiding question and the two state equations in `README.md`. Make one prediction: can a
command that enters only the rate equation eventually move position when coupling is intact?

## Baseline

Run the baseline sections of `experiment.m`.

1. The minimum-energy command first builds positive rate, then reverses to finish at `1 m` with
   zero rate after `2 s`.
2. A fixed positive probe changes rate immediately; position accumulates afterward through the
   coupling.
3. The two traditional controllability columns and the finite-horizon Gramian both have rank two.
4. The terminal residual is numerical roundoff, while peak command and command-energy remain
   separate feasibility warnings.

Mechanism: every reachability column is one held command's terminal-state effect. The dynamics make
earlier rate changes contribute to position, so the columns span two state directions.

## Lever 1 — actuator effectiveness

Keep coupling at `1`, maneuver time at `2 s`, interval at `0.05 s`, and target at `1 m`.

- Smaller effectiveness shortens every reachability column.
- Rank stays two for the nonzero sweep values.
- The weakest singular value grows with effectiveness, while required energy falls with its square.

Read the explanation only after comparing score and effort.

## Lever 2 — maneuver time

Reset effectiveness to `1 (m/s^2)/command` and sweep `0.5–4 s`.

- Short transfers require large positive and negative commands.
- Longer transfers add useful input opportunities and reduce energy and peak command.
- `A`, `B`, damping, target, and interval stay fixed; only the horizon changes.

## Broken case and recovery

Set coupling to zero while retaining the same actuator and probe.

1. Broken-case rate matches the intact probe response.
2. Broken-case position remains exactly zero.
3. Rank is one and the requested position target retains a `1 m` residual.
4. Restore coupling to one; position responds, rank returns to two, and the target is reconstructed.

## Check and teach back

Run `run_module_checks("P13")`. Answer the interpretation questions in `checks.md`, then give the
two-sentence teach-back. Learner completion remains separate from batch implementation.

## Source checks

# P13 checks: Test Controllability

Run `run_module_checks("P13")` before answering the interpretation prompts.

## Observe

1. In the baseline probe view, which state responds directly to command, and which state responds
   only after the kinematic coupling acts?
2. Why does halving actuator effectiveness increase command-energy demand even though the
   controllability rank remains two?
3. Why does a longer maneuver need less peak command without changing `A`, `B`, damping, target, or
   sample interval?
4. In the broken case, why can rate respond to a probe while position remains frozen?

## Numerical completion contract

The executable checks independently verify:

- exact zero-order-held state and input matrices;
- traditional and finite-horizon controllability identities;
- deterministic state recurrences and target reconstruction;
- isolated actuator-effectiveness and maneuver-time sweeps;
- zero-input and disconnected-coupling limiting cases;
- malformed input, grid alignment, response, and resource bounds;
- recovery when the missing coupling is restored.

## Teach back

In two sentences, answer: “What inputs, observable effects, and failure modes matter when you test
Controllability?” Name the input path, one visible state effect, and why full rank alone does not
guarantee a physically feasible maneuver.
