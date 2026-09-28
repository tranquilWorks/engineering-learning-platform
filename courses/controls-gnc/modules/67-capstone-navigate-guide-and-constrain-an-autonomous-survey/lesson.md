# Navigate and constrain a timed survey

A planar vehicle follows three waypoint legs while a GNSS outage interrupts correction of its inertial estimate. This 30-second simulation demonstrates navigation, line-of-sight guidance and a sampled freshness hold. It is not an aircraft model or proof that the complete survey finishes.

## Model and equations

Waypoints are $(0,0),(30,0),(30,20),(0,20)$ metres. The vehicle starts at $(0,1)$ m and travels at $2\,\mathrm{m/s}$ when allowed. For a constant turn rate $\omega$ over $\Delta t=0.05\,\mathrm{s}$,

\[\Delta\mathbf p=v\Delta t\,\operatorname{sinc}(\omega\Delta t/2)\begin{bmatrix}\cos(\psi+\omega\Delta t/2)\\\sin(\psi+\omega\Delta t/2)\end{bmatrix},\quad \Delta\psi=\omega\Delta t.\]

Here sinc means $\sin z/z$. The implementation converts to NumPy's normalized sinc. Position is in metres, speed in m/s, heading in radians and turn rate in rad/s; the control displays degrees/s.

Project the estimated position onto the current leg, target a point 4 m ahead, and command $\omega_c=1.5\,\operatorname{wrap}(\psi_{target}-\hat\psi)$ per second. The healthy actuator clips this to the selected limit. A leg changes when its along-track coordinate reaches one metre before the endpoint.

GNSS updates arrive every 0.5 s except during $[5,5+T_{outage})$. Small deterministic position/heading errors accompany each fix. Between fixes, dead reckoning uses a gyro bias of $0.3^\circ/\mathrm{s}$. Once fix age exceeds 3 s, healthy forward speed becomes zero until a fresh fix arrives. Turning in place remains allowed in this kinematic model.

## Baseline workflow

Predict whether the 4-second outage will activate the hold. It does: the final pre-outage fix is at 4.5 s, so age exceeds 3 s before fixes resume at 9 s. For an estimated point 1 m above a straight leg and target 4 m ahead, $\psi_{target}=-\arctan(1/4)=-14.04^\circ$; the demanded rate is $-21.05^\circ/\mathrm{s}$, clipped to $-12^\circ/\mathrm{s}$.

Run the baseline, compare actual and estimated paths, and inspect the age plot. The maximum cross-track distance is about 8.32 m around a corner. The separate teaching requirements allow 12 m cross-track distance, zero turn-rate excess and zero motion decisions after expiry. These deliberately broad bounds are not a field navigation specification.

## Two one-variable sweeps

1. Keep the turn limit at 12°/s and extend dropout to 20 s. Predict less mission progress. The long hold can reduce maximum cross-track error because the vehicle barely reaches the corner; a smaller error is not automatically better mission performance.
2. Restore the 4-second dropout and raise the limit to 30°/s. Compare the corner trace and the measured turn-rate excess. The vehicle can turn more sharply while still respecting its selected bound.

## Intentionally broken case

Broken mode bypasses both the turn clamp and the freshness hold. Guidance commands still drive the actual unicycle. The measured rate excess and stale moving samples fail the requirements; no control value is silently replaced and no error curve is prescribed.

## Recovery

Restore healthy mode at the same dropout and limit. The age threshold and actuator clamp return, and deterministic paths/metrics must reproduce the baseline.

## Limiting cases and invariants

With zero dropout, regular fixes prevent a freshness hold. With zero turn rate, the exact arc tends to straight motion of length $v\Delta t$. A stopped vehicle can have low path error while making no along-track progress. The maximum applied healthy rate stays within its bound to floating-point tolerance.

## Independent evidence

The reference represents position in the complex plane and advances an exact exponential arc. It separately replays fixes, waypoint changes and holding, then measures the same physical quantities. Five scenario vectors are generated from that reference, not from plotted curves.

## Common mistakes

Do not equate alarm activation with failure: the alarm is the intended protective response. Do not infer survey completion from the three plotted legs or treat the simplified inertial update as a full GNSS/INS filter.

## Teach-back

- Why can longer dropout lower maximum error? Holding prevents entry into difficult geometry but sacrifices progress.
- Why do degrees/s need conversion? The propagation equations use radians, and a unit error changes the physical arc.
- Which result rejects the broken run even if cross-track error is small? Its nonzero actuator excess and stale moving-sample count.

## Cumulative assessment

Use the fix schedule to calculate the hold interval, derive the first straight-leg turn demand, and compare both sweeps using error and mission progress. Explain exactly which measured requirements make the broken run unacceptable. A complete answer must include the timing and units, not merely the alarm flag.
