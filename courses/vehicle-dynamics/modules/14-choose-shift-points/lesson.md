# Distinguish a Force Crossover from a Redline Limit

A shift decision needs a reason. One possible reason is that the next gear now produces at least as much wheel force. Another is that the current gear has reached its permitted engine speed. These are different events. A routine that returns redline whenever it finds no crossover must not describe every returned value as a force crossover.

## Physical model: torque map, ratios and units

This lesson uses the empirical torque map

\[
T(r)=\max\left(120,\;245-6\times10^{-6}(r-5000)^2\right),
\]

where r is the numerical engine speed in RPM and T is in N·m. The quadratic coefficient therefore carries N·m/RPM². This is a teaching curve, not a measured engine calibration. Current engine speed is examined from 2500 to 7400 RPM. Final drive is 4.1, wheel radius is 0.315 m, and efficiency is 0.90.

Let g_c be current ratio, g_n next ratio, and q = g_n/g_c. A valid upshift requires 0 < q < 1. At unchanged vehicle speed, the engine drops to r_next = qr. The wheel forces are

\[
F_c(r)=\frac{T(r)g_c g_f\eta}{R},\qquad
F_n(r)=\frac{T(qr)g_n g_f\eta}{R}.
\]

The reduced engine speed changes torque as well as gearing. Comparing ratios alone, or evaluating both torque values at the old RPM, misses this mechanism. Road speed at a decision is r(2π/60)R/(g_c g_f), in m/s; the RPM conversion is necessary because the torque-map input and angular speed use different units.

## Three honest outcomes

A **force crossover** is a resolved root of F_n − F_c inside the permitted RPM interval. A **redline-limited decision** means no such crossover occurs before 7400 RPM, so the decision reaches the upper speed boundary while the forces can still differ. **Unavailable** means the selected next ratio is equal to or larger than the current ratio, so the pair is not an upshift under this lesson’s convention.

The main panel still shows formal force curves for an invalid pair, but those curves do not make its upshift decision valid. Decision metrics are explicitly unavailable, and nominal decision sweeps omit invalid ratio regions. An empty portion of such a sweep is not a zero-RPM recommendation.

For valid descending ratios, the in-band torque samples lie on the quadratic branch. Factoring the force difference by the positive quantity g_c(1−q) gives

\[
-95-0.06(1+q)r+6\times10^{-6}(1+q+q^2)r^2.
\]

Its zero can be resolved without subtracting almost identical gear forces repeatedly. The executed model uses a bracketed solve; a separately derived quadratic root checks it. The force curves are sampled for display, but the decision is not rounded to a display-grid point. Any algebraic candidate outside the permitted interval is not an in-band crossover.

## Worked comparisons

At the default ratios 2.188 to 1.541, the decision is redline-limited at 7400 RPM. Post-shift RPM is about 5211.79 and road speed about 27.2107 m/s. Current-gear force is about 5393.76 N, next-gear force 4417.81 N, and their next-minus-current gap is −975.95 N. Those separated forces directly refute a crossover claim at the default decision.

Select current ratio 2.09 and next ratio 2.08. Both are reachable with the refined 0.001 slider steps. This near-equal pair crosses at approximately 7399.34147 RPM, with post-shift speed about 7363.93793 RPM and both forces about 5152.63672 N. The small RPM difference from redline matters because the event’s classification is different. Do not infer event type merely from a rounded display value near 7400.

## Predict and sweep

1. Hold next ratio at 1.541 and vary current ratio. Observe the nominal decision sweep only where current ratio exceeds next ratio. Compare an invalid setting, a valid wide ratio separation and a nearly equal pair. Use the force gap and decision label together rather than reading an RPM alone.
2. Hold current ratio at 2.09 and vary next ratio. Compare 1.5, 2.08 and 2.09. Predict redline limitation, an in-band crossover and an unavailable decision respectively. The secondary sweep shows only valid nominal decisions. The force panel reveals why a ratio change alters the comparison across engine speed.

## Named broken behavior and exact recovery

The fault looks up next-gear torque at current RPM while still calculating the kinematic post-shift RPM correctly. At valid descending ratios this wrong force comparison stays below the current-gear force and selects redline. Inspect the same-input next-gear curves and the maximum torque-lookup force error across the displayed interval. A single matching point is insufficient: the quadratic torque curve is symmetric about 5000 RPM, so different RPMs can occasionally produce the same torque.

Disable the fault at unchanged inputs and verify recovery of both the proper next-gear curve and the decision classification. Reset separately to recover the default redline-limited example.

## Limits and limiting cases

This model omits shift duration, traction variation, gear-dependent losses, engine transients and lap-time objectives. A force-based or redline-based rule here does not establish an optimal shift strategy for a real vehicle.

## Common mistakes

A redline return does not prove force equality. Correct post-shift RPM does not prove the torque lookup used it. Equal ratios are not an upshift, even though their nominal force curves coincide.

## Formative checks

What distinguishes the default decision from the 2.09-to-2.08 case? Check your reasoning: the default has a negative force gap at its boundary; the near-equal valid pair has a resolved in-band zero. Explain why a display-grid sample is not the numerical root.

## Teach-back checklist

State all three outcomes, derive the RPM drop, compare actual forces, and diagnose the curve-wide lookup error. Separate a simplified shift rule from a real optimization objective. This is synthetic teaching evidence, not measured-vehicle validation.
