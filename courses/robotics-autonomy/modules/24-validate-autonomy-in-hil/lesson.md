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
