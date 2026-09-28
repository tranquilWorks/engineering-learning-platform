# Calibrate and predict with an illustrative coupled vehicle model

This is a self-contained, synthetic GR86-sized teaching model. It is **not calibrated to a measured GR86**. Tire data, setup relations, torque map, chassis and thermal assumptions are all declared below. The eleven DT checks assess the executed chain within those limits.

## Model and equations

Use mass 1450 kg and reference wheel load $F_{z0}=mg/4$. Synthetic tire measurements at slips 0.005–0.16 rad follow $F_y=\min(C_\alpha\alpha,\mu F_{z0})$ with generating values $C_\alpha=70000$ N/rad and $\mu=1.15$. Fit stiffness from four linear samples and friction from two saturated samples; unused slips 0.04 and 0.07 rad check the fit.

Setup change $d$ scales friction by $1+0.3d$, downforce area to $2.5(1+2d)$ m² and drag area to $0.72(1+d)$ m². Downforce is $D=\rho C_LA\,v^2/2$ N with $\rho=1.225$ kg/m³. Static front weight fraction is 0.53. Lateral transfer is $m a_y h/t=m(v^2\kappa)(0.5)/1.52$ N, split front/rear by $0.55+0.1d$. Four wheel loads must sum to $mg+D$. Load-sensitive capacity is

\[C=\sum_{j=1}^4 \mu F_{z0}(F_{zj}/F_{z0})^{0.9}.\]

A quasistatic roll estimate uses stiffness $100000(1+d)$ N·m/rad. This is a load-transfer/compliance abstraction, not multibody suspension dynamics.

The six illustrative gear ratios are 3.63, 2.19, 1.54, 1.21, 1 and 0.77, with final drive 4.1, wheel radius 0.31 m and efficiency 0.9. A declared piecewise-linear torque map spans 2000–7400 rpm and 170–230 N·m. Select the valid gear with greatest wheel force. These are modeling inputs, not asserted vehicle specifications.

Solve 96 segments on a closed 180-by-110 m ellipse for nine constant offsets within ±1.5 m. Curvature consumes at most $0.8C$ and longitudinal force at most $0.6C$, so the allocated pair lies inside the force circle. Cyclic forward/backward constraints include gearing, drag, rolling force and a brake-force ceiling $7500(1+d)$ N. Negative wheel work heats a 32 kg, 500 J/(kg·K) brake mass with no cooling. Lap time is $\sum ds/v$.

## Baseline workflow

Predict how adding downforce and drag together changes the lap. At 40 m/s and $d=0.08$, downforce is $0.5(1.225)(2.5)(1.16)(40)^2=2842$ N. The physical normal-load sum must be $14224.5+2842=17066.5$ N, exactly once.

Run setup 0.08 and friction uncertainty 0.05. The selected lap is about 26.580 s, roughly 0.269 s faster than the separately executed zero-change setup. The two friction endpoint runs span about 0.749 s. This is a bounded scenario envelope, not a confidence interval or coverage guarantee.

Read all eleven DT quantities: tire held-out force, physical combined utilization, minimum wheel load, propulsion excess, brake temperature, aero/load ledger, total curvature, offset feasibility, cyclic reachability, endpoint-envelope consistency and clean replay discrepancy. The speed and utilization plots expose the actual selected lap.

## Two one-variable sweeps

1. Keep uncertainty 0.05 and reduce setup change to 0.02. Compare the coupled drag/grip/load/gear outcome; the time improvement falls to about 0.077 s. It is calculated by rerunning both models, not multiplying the slider by a fixed benefit.
2. Restore setup 0.08 and increase friction uncertainty to 0.1. The nominal lap stays the same while endpoint width grows to about 1.546 s. Only friction varies in this uncertainty family; do not interpret it as uncertainty in every subsystem.

## Intentionally broken case

The fault counts aerodynamic load twice when computing available grip. The physical ledger still contains one downforce contribution. At baseline the model predicts a faster-looking 25.969 s lap but a maximum normalized load-ledger discrepancy near 0.1931. The real DT-06 check fails. Other conservative constraints can still pass; the code does not force four arbitrary failures.

## Recovery

Restore one downforce contribution at identical controls and rerun the full chain. An internal clean replay is also executed twice and compared, but its passing verdict does not validate the currently broken lap. The displayed recovery check is explicitly labeled internal.

## Limiting cases and invariants

Zero setup change reproduces the nominal setup comparison. Zero internal uncertainty collapses the endpoint width. Every healthy wheel-load sum equals weight plus downforce; wheel loads stay above 200 N. The full cyclic seam obeys force constraints, and grid refinement should stabilize lap time. Bounds are node/segment discretization checks, not continuous physical certification.

## Independent evidence

The reference independently fits scalar tire relations, computes gear forces and wheel loads, then uses scalar Gauss-Seidel reachability instead of the production vectorized Jacobi iteration. Five expected scenarios, force/load invariants, parameter endpoints and refinement checks complement numerical agreement.

## Common mistakes

Do not count aero twice, call synthetic fitting measured calibration, equate a scenario envelope with probability, or treat a clean internal rerun as evidence that a faulted prediction is valid.

## Teach-back

- Why does a fast lap fail the ledger check? Performance computed with unavailable normal load has no valid physical basis.
- Why might utilization still pass in broken mode? Conservative force reserves can mask one consequence while the load conservation defect remains.
- What is the brake temperature claim? A one-lap adiabatic model result, not measured cooling or endurance.

## Cumulative assessment

Trace a fitted tire coefficient through wheel loads, gear selection and one reachable segment. Recompute that segment's wheel work and normal-load sum. Compare setup and friction-endpoint laps, diagnose DT-06 in broken mode, and recover at unchanged controls. A complete answer must state the synthetic and discretization limits.

## Formative checks

At 40 m/s and setup 0.08, calculate the physically available normal-load sum. Answer: 17066.5 N. Counting downforce twice would instead use 19908.5 N, so a faster prediction must be rejected even if another conservative constraint passes. Explain why doubling the uncertainty control can widen the friction scenario envelope without changing the nominal selected lap.

This Python-first native lesson is not a source conversion and does not establish a measured-vehicle result.
