# Optimize a Racing Line

> **Guiding question:** When does a wider-radius line repay its added distance, and how is track-boundary feasibility enforced?

## Physical model, geometry, and units

The teaching corner starts from a 45 m reference radius. A lateral offset `d` changes effective radius to `R = 45 + d`, while the declared path-length approximation is `L = (pi/2)45 + 0.08d²`. The offset-squared term represents extra transition distance: a larger radius is not free. The grip-limited speed is `v = sqrt(mu g R)`. The time proxy adds the corner time `L/v` and a fixed 200 m straight at 45 m/s.

Positive offset is the wider side of the corner. A candidate is feasible only when `|d| <= w`, where `w` is usable half-width. The search evaluates exactly 41 evenly spaced candidates, reports boundary margin `w - |d|`, and compares the optimum with the centre line.

This is a Python-first native P21 design from a scaffold, not source- or MATLAB-runtime equivalence. It is a bounded optimization lesson, not a surveyed circuit or driveable trajectory.

## Predict and sweep one variable at a time

1. Hold width at 4 m and sweep friction from 0.70 through 1.05 to 1.40. Predict absolute time and whether the geometry selected changes.
2. Restore friction 1.05 and sweep half-width from 2 through 4 to 6 m. Predict the gain from centre as more offsets become feasible.

The useful comparison is time, not curvature alone. A line that raises speed but adds too much distance can lose.

## Named broken behavior and exact recovery

**Broken behavior:** score a candidate one metre beyond the declared half-width. It may look fast, but its constraint margin is -1 m and the result is invalid.

**Exact recovery:** generate only the 41 offsets between `-w` and `+w`, retain the distance penalty and grip limit, and select the minimum feasible time. Restore `mu=1.05` and `w=4 m` for the exact baseline.

## Limits and limiting cases

At smaller friction, every candidate’s corner time increases. At zero usable width—which is outside the control range—only the centre would remain. This model omits linked corners, vehicle width, curbs, banking, longitudinal acceleration, transient tires, obstacles, driver consistency, and a dynamically continuous path.

## Common mistakes

- Maximizing radius without accounting for path length.
- Scoring candidates outside track limits.
- Comparing friction cases while silently changing geometry.
- Treating a pointwise offset as a smooth, drivable racing line.
- Reporting a time proxy as measured lap performance.

## Formative checks

1. Derive the speed-limit units from `mu g R`.
2. Compute the feasibility margin for an offset at each boundary.
3. Explain why the centre-line comparison is retained.
4. Identify which omitted constraint would matter first on a linked circuit.

## Teach-back checklist

- [ ] I can explain the radius–distance trade.
- [ ] I predicted both one-variable sweeps.
- [ ] I can audit candidate count and feasibility margin.
- [ ] I diagnosed the named broken behavior and exact recovery.
- [ ] I can state why this is not a track-ready line.

This is not measured-vehicle, driver, browser/learner, track, hardware/HIL, certification, release, or production evidence.
