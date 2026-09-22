# Validate Autonomy in HIL

**Guiding question:** What inputs, observable effects, and failure modes matter when you validate Autonomy in HIL?

## Concept and prediction

Hardware-in-the-loop validation is a controlled argument: defined interfaces connect production-representative software and hardware to a plant representation, faults are injected, timing and safety monitors are observed, and predeclared verdict criteria decide the result. This lesson implements only a deterministic software analogue of that workflow.

Predict when a telemetry dropout beginning at 2 s will cross a 120 ms freshness watchdog, what safe command should follow, and what evidence is required to call that software test a pass.

## Model, symbols, and equations

- $$\dot y=(-y+u)/\tau$$ — first-order virtual plant.
- $$u=\operatorname{sat}(K_pe+K_i\int e\,dt)$$ — bounded nominal controller.
- $$a_{sig}=t-t_{last},\quad a_{sig}>T_w\Rightarrow u=0$$ — freshness monitor and safe command.
- $$PASS=[fault\ detected]\land[finite\ response]\land[safe\ command\ observed]$$ — lesson verdict.

Time uses seconds internally; interface latency and watchdog controls use milliseconds. Plant output, reference, and effort are normalized dimensionless signals. A FIFO models telemetry latency, and dropout holds the last received value.

## Manipulation: two one-variable sweeps

1. Sweep `io_latency_ms` through [0,30,100]. Nominal phase lag grows and consumes timing margin without itself creating a dropout.
2. Restore baseline, then sweep `fault_duration_s` through [0.2,1,2]. A fault shorter than the watchdog may not trigger; longer faults should create a bounded safe-command interval.

The response plot overlays reference, virtual plant, and controller effort. The mechanism plot exposes telemetry age, watchdog threshold, and monitor state.

## Evidence and limiting cases

The independent reference implements the stated plant, latency queue, dropout, and watchdog recurrence separately from the production experiment.

- With zero latency and no dropout, the loop approaches its reference subject to controller/plant dynamics.
- A dropout shorter than the watchdog is intentionally tolerated by this requirement.
- An infinite watchdog is equivalent to disabling freshness supervision.

The evidence is software simulation only. No real-time processor, I/O hardware, motor, sensor, robot, bench, physical HIL loop, or production system executed.

## Intentionally broken assumption

**Freshness watchdog disabled.** Broken mode continues using stale telemetry during the injected dropout. The trajectory may remain numerically bounded, but the required detection and safe-command evidence does not exist, so the verdict fails.

## Explanation and recovery

Enable the watchdog, command safe when signal age exceeds the requirement, prevent integral windup during the safe interval, and retain exact injection, detection, response, and verdict timestamps. Physical HIL would additionally require measured I/O timing, target builds, calibrated plant interfaces, and bench safety controls.

## Common mistakes

- Calling a software plant “physical HIL.”
- Injecting a fault without a predeclared expected monitor response and verdict.
- Recording only the command while omitting interface age and actual plant response.
- Passing a test because nothing crashed even though the safety requirement was not observed.

## Focused check and teach-back

At baseline, cite injection time, detection time, safe duration, and verdict. Disable the watchdog, recover it, and teach back units, interface latency, fault model, monitor requirement, verdict logic, and the physical evidence still missing.


## Deep derivation and conventions

The depth target for this module is to **derive the sampled virtual-plant, transport queue, watchdog, and verdict logic**. Start from the physical or geometric constraint, not from the plotted curve. State which quantities are inputs, which are states, and which are observations; then carry the coordinate, sign, frame, sampling, or energy convention through every substitution. The retained convention is: Positive normalized command increases virtual-plant output toward a unit reference. Telemetry age is nonnegative elapsed time since the last delivered sample.

The governing relations are:

- $$y_{k+1}=y_k+\Delta t(-y_k+u_k)/\tau$$ — The software-only virtual plant follows a bounded first-order recurrence.
- $$a_k=t_k-t_{last};\quad a_k>T_w\Rightarrow u_k=0$$ — Telemetry age beyond the watchdog threshold forces the modeled safe command.

Read those equations as a chain of claims. The first relation establishes the mechanism; subsequent relations map it into a prediction that the experiment can expose. A derivation is incomplete if it drops a frame label, silently changes a sign, or combines unlike units. Here the unit ledger is: virtual-plant time constant, fault timing, and plotted time: s; I/O latency, watchdog threshold, and plotted signal age: ms; plant signals: normalized. Before running Python, identify the dimensional unit of every term on both sides of one equation. If the units do not close, a numerical match is accidental.

For a local linearization, discrete update, or geometric approximation, also state its domain. “Correct at the baseline” is weaker than “correct for the declared range under the declared assumptions.” This distinction matters because a robot can produce a smooth and plausible trajectory while violating the modeled constraint. The experiment therefore pairs the response plot with a mechanism or residual plot: one shows what happened, while the other tests why the explanation is credible.

## Alternative formulation and limiting analysis

The required comparison is to **compare software-only, zero latency, short dropout, and long dropout**. Work this comparison before tuning. An alternative formulation should agree on an invariant even if its intermediate coordinates differ; a limiting case should emerge continuously as a parameter approaches its boundary. A branch switch, singular limit, or zero denominator must be handled explicitly rather than hidden by clipping.

Retained limiting checks:

- Zero interface latency removes queue delay but does not remove the sampled-data step.
- A dropout shorter than the watchdog may be tolerated without entering the modeled safe state.

Use at least one as a pencil-and-paper oracle. Substitute the limiting input into the displayed equations, predict the sign and scale of the result, and then inspect the relevant metric. If the limiting result disagrees, first test the convention and the limit-taking step; do not immediately retune an unrelated parameter. This procedure separates a model defect from a parameter choice.

## Practical failure analysis and recovery

The engineering failure to diagnose is **calling software simulation physical HIL or omitting fail-zero evidence**. In the executable counterexample, **Freshness watchdog disabled** is triggered by: Set broken_mode true. Its observable failure is: The controller acts on stale telemetry through the dropout and cannot produce required safe-state evidence. This is not merely a worse numerical score. It violates an assumption that must be named before the model can support a decision.

The recovery is: Enable the watchdog, inhibit integral growth, and command the virtual plant safe after the age bound. Recovery has three parts: remove the fault mechanism, restore the exact baseline inputs, and recheck the original invariant. A curve that looks calmer is not sufficient. The diagnostic signature must return within its retained independent-reference tolerance, and the mechanism plot must again satisfy the relevant sign, conservation, constraint, residual, timing, or consistency condition.

In practice, instrument the variable nearest the violated assumption. For geometry, log frame-resolved residuals; for dynamics and contact, log energy, effort, and saturation; for estimation, log innovations and covariance consistency; for planning and autonomy, log feasibility, guard, collision, or timing decisions. This makes the failure falsifiable and prevents a downstream controller or filter from masking it.

## Evidence workflow and formative check

Run the baseline, then preserve it while changing exactly one control per sweep:

- `io_latency_ms` at [0, 30, 100]: More interface delay increases phase lag and changes closed-loop peak response.
- `fault_duration_s` at [0.2, 1, 2]: Longer dropout holds the software safe command for more samples after watchdog detection.

Before each run, write a directional prediction from one equation: increase, decrease, unchanged, or branch change. After the run, cite one metric and one plotted feature, including units. Then perform these checks:

1. **Numerical prediction:** calculate one baseline quantity to one or two significant figures without using the experiment output.
2. **Dimensional check:** show that one governing equation has consistent units.
3. **Invariant check:** identify a sign, bound, conservation relation, residual, or ordering that should survive the sweep.
4. **Counterexample:** enable the named broken case and explain which assumption fails before describing the visual symptom.
5. **Recovery:** disable the fault, restore the exact defaults, and verify the signature returns rather than merely improves.

Teach it back without referring to the plot first: state the convention, derive the relationship, predict one sweep, identify the practical failure, and explain why the recovery repairs the violated assumption. Only then use the plots as evidence. A strong answer distinguishes model validity, numerical agreement, and physical validation; none is a substitute for the others.

## Boundary and onward links

P67 adds replay/diagnostics; physical HIL remains an explicit external validation step. This lesson establishes its named Robotics competency and provides prerequisites for later mapped modules; it does not absorb the adjacent course's broader theory. The Python result remains deterministic software evidence. It does not claim MATLAB runtime equivalence, learner effectiveness, browser accessibility, physical robot or HIL operation, safety certification, or production readiness.
