# Recover from Integrator Windup

**Guiding question:** What inputs, observable effects, and failure modes matter when you recover from Integrator Windup?

Compare PI recovery with and without correctly signed back-calculation. This native lab preserves the source experiment while making the levers, diagnostics, and recovery available directly in the learning platform.

## Predict before running

Correctly signed back-calculation should shorten recovery after the high demand ends. Write down the mechanism you expect—not only the trace direction—before moving a control.

## Model and equations

- $$\dot q=e+K_{aw}(u_{sat}-u_{raw})$$ — Back-calculation drains the integral state while clipped.
- $$u_{raw}=K_pe+K_iq$$ — Stored integral action delays recovery after demand changes.

The GUI evaluates these equations deterministically. Read the metric cards and both plots together: a pleasing response can still conceal poor authority, weak conditioning, stale data, or invalid assumptions.

## Two one-variable sweeps

1. Sweep `anti_windup_gain` through [0.0, 0.5, 2.0]. Hold every other control fixed and explain the causal chain from equation to trace to metric.
2. Sweep `demand_duration_s` through [1.0, 3.0, 5.0]. Compare the changed mechanism plot with your first prediction.

Do not tune both levers at once until you can identify which term each lever changes.

## Intentionally broken case

The broken case reverses the back-calculation sign and drives the integrator farther into windup. Predict the signature before enabling **broken mode**.

## Recovery

Disable the broken case to feed the saturation gap back with the corrective sign. A recovery is complete only when you can name the failed assumption and point to the metric or trace that confirms it.

## Common mistakes

- Treating a simulation trace as proof about hardware or production behavior.
- Changing multiple controls at once and losing causal attribution.
- Reading only the final value while ignoring transient effort, conditioning, delay, or saturation.
- Hiding a failed assumption by retuning instead of reproducing and explaining it.

## Teach-back

In two minutes: state the governing equation, explain what each live lever changes, identify the broken assumption, and justify the recovery with one visible metric and one plot feature.

---

## Source lesson (retained and polished into this GUI)

# P12 lesson: Recover from Integrator Windup

## Guiding question

What inputs, observable effects, and failure modes matter when you recover from Integrator Windup?

## Compounds on

- **P05:** feedback error drives controller effort.
- **P06:** the integral term is controller memory with actuator units.
- **P09 and P10:** a digital controller updates state over explicit held-command intervals.
- **P11:** requested and applied control separate when actuator authority is exhausted.

## One prediction before the baseline

The reference stays at an unreachable `+2 output` for three seconds, then changes to reachable
`-0.5 output`. Two PI loops have identical gains, plant, time grid, and `±1 actuator` limit. One
integrator uses only `Ki*e`; the other also uses the requested-applied command gap. Which loop will
reverse applied control first, and what internal state should explain the difference?

## Mechanism-first explanation

The controller requests

`uRequested = Kp*e + I`,

but the plant receives

`uApplied = clamp(uRequested, -uLimit, +uLimit)`.

With no anti-windup, `I` keeps integrating positive error while `uApplied` is already pinned. The
growing request cannot make the actuator push harder; it only stores a larger obsolete command.
Back-calculation adds

`Kaw*(uApplied-uRequested)`

to the integral derivative. During positive clipping the term is negative, so it opposes windup.
After the reference reverses, less positive memory blocks the needed negative control.

## Levers and observable effects

### Anti-windup gain `Kaw` (1/s)

- `Kaw = 0` is the exact no-protection limiting case.
- Moderate gain lowers integral state at release and post-release integral absolute error.
- Excessive gain can drive the integral state too negative and add an opposite recovery transient.

### High-demand duration (s)

- Longer duration keeps the actuator pinned while the unprotected integral state grows.
- Correct back-calculation uses the persistent command gap to bound stored effort.
- The duration lever changes exposure to saturation, not plant or controller gains.

## Deliberately broken case

The broken case uses `uRequested-uApplied` where the correction needs
`uApplied-uRequested`. Missing positive command then adds more positive integral state. The request
grows, the actuator stays pinned in the old direction after the target changes, and recovery fails.
This is a sign error in a feedback path, not evidence that anti-windup itself creates more authority.

## Correct these misconceptions directly

- **“The integrator makes the actuator stronger.”** No. Applied effort remains within `±1 actuator`.
- **“Any large anti-windup gain is better.”** No. Over-aggressive correction can over-unwind state.
- **“Clipping alone is windup.”** No. P11 clipped a P controller with no integral state. Windup is
  incompatible stored controller memory during clipping.
- **“Low output after reversal proves plant delay.”** Not by itself. Inspect integral state and
  applied-command direction to distinguish controller memory from the one-second plant time constant.

## Teach-back

In two sentences, explain why an unprotected PI controller can keep applying effort in the old
direction after a reference reversal, and how correctly signed back-calculation changes the
integral-state update without violating the actuator limit.

## Source walkthrough

# P12 walkthrough: Recover from Integrator Windup

## Read

Read the guiding question and the two integral-state equations in `README.md`. Recall from P11 that
the command gap is requested effort minus applied effort. Predict once which loop reverses applied
control first when the target changes sign.

## Baseline

Run the first four sections of `experiment.m`.

1. In the output view, both paths initially rise under the same `+1 actuator` clamp.
2. At `3 s`, the reference changes from `+2` to `-0.5 output`.
3. The protected path turns its applied command negative immediately; the unprotected path retains
   a positive integral state near `3.95 actuator` and delays reversal by about `2.02 s`.
4. The protected path has lower post-release integral absolute error.

Mechanism: the negative correction `Kaw*(uApplied-uRequested)` acted while positive command was
missing. It reduced controller memory before the target changed.

## Lever 1 — anti-windup gain

Run the `Kaw` sweep while demand duration remains `3 s`.

- At `Kaw=0`, protected and unprotected paths coincide exactly.
- Moderate correction reduces stored positive state and recovery error.
- Larger values can push release state negative; observe that recovery quality is not monotonic.

Read the explanation only after comparing the output and metric views.

## Lever 2 — high-demand duration

Reset `Kaw=1 1/s`, then run the duration sweep.

- The unprotected integral state at reversal grows with every longer high-demand interval.
- Its post-release error also grows.
- The protected release state and error stay bounded because the command gap is fed back during
  saturation.

Duration changes how long windup can accumulate. It does not change actuator limit, PI gains, plant,
or time-step mechanics.

## Broken case and recovery

Run the wrong-sign section.

1. The broken integral state grows rapidly because unavailable command reinforces itself.
2. After the reference reverses, applied control remains positive and output stays on the wrong side.
3. Restore the sign to `+1`; the correction drains unavailable effort and recovery resumes.

## Check and teach back

Run `run_module_checks("P12")`. Answer the interpretation questions in `checks.md`, then give the
two-sentence teach-back. Personal completion is separate from batch implementation and should be
recorded only after the executable checks and teach-back.

## Source checks

# P12 checks: Recover from Integrator Windup

Run from MATLAB:

```matlab
run_module_checks("P12")
```

The executable checks cover deterministic repeatability, the explicit clamp, exact held-input plant
motion, both integral-state recurrences, event-aligned and partial time intervals, the `Kaw=0`
limiting case, both independent sweeps, wrong-sign failure and recovery, malformed inputs, and
sample/response resource bounds.

## Interpretation questions

1. During positive saturation, why is `uApplied-uRequested` negative, and what should that do to a
   positive integral state?
2. Why do protected and unprotected paths coincide exactly when `Kaw=0`?
3. Why can longer high-demand duration worsen unprotected recovery without changing the plant?
4. Why can excessive correction gain produce a different recovery penalty even though it prevents
   positive windup?
5. What output, integral-state, and applied-command symptoms identify the wrong-sign broken case?

## Teach-back

In two sentences, answer the guiding question: explain the inputs that control windup recovery, the
observable effects of stored integral effort, and the failure caused by reversing the command-gap
feedback sign. Mention that anti-windup changes controller memory, not actuator authority.
