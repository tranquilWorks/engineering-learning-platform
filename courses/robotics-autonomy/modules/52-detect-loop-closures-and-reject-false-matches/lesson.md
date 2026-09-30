# Gate a Loop Candidate and Optimize an Anchored Position Graph



## Model, derivation, and conventions

`objective=0.5*sum(||position_j-position_i-odometry_ij||²/sigma_odom²)+score*Huber(||closure_residual||/sigma_closure)`

`Huber_weight=min(1,delta/||closure_residual||)`

`position_0=[0,0]; appearance>=0.70 and innovation<=0.30 m admit a normal loop`

Nine two-dimensional positions trace eight edges around a square loop. Each half-metre ideal odometry displacement receives a fixed drift [0.02,0.005] m, and the baseline graph integrates those measured edges from the anchored first position [0,0] m. The resulting terminal position does not return exactly to the origin. These are translation factors only: the graph has no rotational state, camera features or three-dimensional pose manifold. It provides a small, explicit graph optimization problem whose entire solution can be independently checked.

The appearance control supplies an external candidate score between zero and one. This lab does not compute image descriptors or learn that score from photographs. The geometric control sets the magnitude of an actual candidate measurement innovation. The closure measurement is constructed from the baseline endpoint minus [selected_residual,0] m, so evaluating the candidate against the baseline produces that horizontal innovation. It is a deliberately controlled factor-consistency experiment. The measurement is not automatically the true physical loop displacement, and inserting it is not automatically an improvement over independent ground truth.

Normal mode first requires appearance score at least 0.70. It then requires measured geometric innovation at most 0.30 m. A rejected candidate contributes no graph factor, so the optimized graph stays at its odometry baseline. Passing both gates inserts a closure factor linking the anchored start and terminal position. The odometry standard-deviation scale is 0.03 m, and the closure scale is 0.08 m. These define the relative weights of the synthetic optimization objective; they are declared model choices, not sensor statistics estimated from experimental data.

The accepted normal closure uses a Huber loss with physical residual transition 0.05 m. Below that transition it behaves quadratically; above it, its influence grows only linearly with residual magnitude. Iteratively reweighted least squares recomputes the residual-dependent weight and solves the actual weighted graph until positions stop changing or the stated budget is reached. All eight odometry factors still constrain the solution. The first node remains exactly anchored, preventing an arbitrary global translation from being confused with a loop-induced deformation.

The fault retains the appearance gate but bypasses geometric rejection and uses an ordinary quadratic closure loss. It does not replace the selected appearance or innovation controls with forced values. A high-appearance, geometrically inconsistent candidate can therefore pull the graph much more strongly. At zero innovation both modes can leave the baseline unchanged. Below the appearance threshold both reject the candidate. Inside the Huber quadratic region, accepted normal and faulty weights may agree. These are meaningful limits of the implemented mechanism, not exceptions to hide from the learner.

The first metric is appearance score multiplied by the final robust weight; it is zero for a rejected factor. This dimensionless influence coefficient is not itself a posterior probability that a loop is correct. The second metric is the actual normalized factor objective evaluated at the final graph, including every odometry residual and the inserted closure's declared loss. The third metric is the maximum Euclidean displacement of any optimized node from its baseline position, in metres. All three are computed from the fitted state and residuals rather than assigned as constant multiples of the selected innovation.

A separate compliance calculation checks the graph solution. Eight equal odometry edges in series have endpoint stiffness 1/(8*0.03²). For a quadratic closure, the competing stiffness is appearance_score/0.08², so the endpoint correction follows their weighted balance. In the robust linear branch, the closure's force-like influence is capped by its Huber transition, and the endpoint correction follows that cap divided by chain stiffness. The interior corrections distribute linearly along the eight equal edges. This closed solution is an independent consequence of this simple chain, not a substitute for the production graph solve.

The map plot overlays baseline and optimized node positions; a second plot shows actual node displacements. Its vertical axis includes at least 0.01 m so a zero-innovation solve cannot magnify floating-point roundoff into apparent physical deformation; raw node values remain unchanged. A loop that bends the map less is not thereby proven correct: robust losses limit influence, while geometric and perceptual validation must establish whether a factor represents the same place. The experiment excludes rotational drift, feature ambiguity, dynamic scenes and a real place-recognition front end. Its value is the traceable relationship among a candidate, two gates, a robust factor and an anchored numerical solution.

## Predict before running

Predict whether a high appearance score is enough to justify moving a map, and distinguish rejecting a loop from reducing the influence of an accepted loop. Record the expected direction of change and an invariant before reading the computed result. State a condition under which the fault could be hidden, rather than assuming every faulty setting must look worse.

## Baseline workflow

Reset controls and disable the named fault. Use Candidate appearance score = 0.78 1; Baseline loop innovation = 0.12 m. Read the response curve, then connect it to the mechanism curve using the governing equations.

Anchored position graph plots World y (m) against World x (m). Its series are Baseline, Updated. Loop-induced displacement plots Displacement (m) against Node index (1). Its series are Shift.

The default record is Final closure influence: 0.512315 1; Optimized factor objective: 0.445225 1; Maximum node displacement: 0.043875 m. These computed values are a worked example for these settings, not acceptance limits for every experiment. Keep parameter values and units beside the result. A near-zero residual has meaning only in relation to the stated model and numerical precision.

## Two one-variable sweeps

1. Increase appearance score while holding innovation fixed, including values on both sides of 0.70. Separate the discrete insertion decision from the continuous influence of an accepted factor.

2. Increase geometric innovation at a fixed high appearance score. Compare the normal 0.30 m gate, the Huber transition after fitting and the ungated quadratic fault; reconstruct map displacement from the node arrays.

Return to defaults between sweeps. Hold the other control fixed and record both a changing output and an expected invariant. Explain the physical or numerical path from the selected input to the observed response.

## Intentionally broken case

The system keeps the appearance gate but skips geometric rejection and replaces robust closure influence with a quadratic loss. Both selected controls and all odometry factors remain intact.

Run the same parameter values with the fault enabled. Compare complete curves as well as summary metrics. Identify the actual operation that changed and calculate why it affects the measured result. A changed warning label is not numerical evidence.

## Recovery

Restore geometric gating and Huber influence, solve again from the same odometry graph and confirm the anchor, residuals and node displacements.

Repeat a saved nominal setting and confirm that its values and curves return. Recovery must restore the governing mechanism and its evidence, not merely clear a warning.

## Alternative and limiting cases

This is an anchored two-dimensional translation graph with an externally supplied appearance score, not full rotational SLAM or image-based loop recognition. Rejected factors and zero innovation leave the baseline unchanged. A robust loss limits damage but does not prove that an accepted factor identifies the correct physical place.

## Independent evidence and MATLAB-style design boundary

The reference separately constructs the drifted chain and uses its endpoint compliance with the analytic Huber branch solution, then distributes the correction along the equal edges. Production solves the weighted graph by IRLS. Full node positions, anchor, residuals and stationarity are checked.

Five retained cases cover baseline, two single-control sweeps, the named fault and recovery. Expected values come from the independent formulation; actual values come from the executable lesson. Absolute and relative comparison tolerances remain 1e-8. Full-state or geometric checks supplement these three-number signatures, which alone cannot establish correctness. MATLAB has not been executed and no MATLAB equivalence is claimed. Browser and container evidence is recorded separately. Agreement between synthetic implementations does not establish empirical model validity.

## Engineering review checklist

Reconstruct one displayed quantity from the actual state or geometric arrays. Check coordinate ordering, signs and units before comparing numbers. Explain which assumption each check constrains, and identify a defect that another check could miss. Preserve the baseline, one controlled sweep, fault and recovery as a reproducible evidence sequence. State the model boundary before making a broader engineering recommendation.

## Common mistakes

Do not infer correctness from a changing headline alone. This is an anchored two-dimensional translation graph with an externally supplied appearance score, not full rotational SLAM or image-based loop recognition.

Do not change both sliders at once and attribute the result to one cause. Separate a model assumption from a measured property, and a finite-horizon observation from a universal guarantee. Floating-point roundoff is not a physical effect; equally, an attractive plot is not a substitute for the governing calculation.

## Focused check and teach-back

Why are geometric rejection and a robust loss complementary rather than interchangeable?

Answer rationale: A gate decides whether a factor enters the graph at all; a robust loss controls how an inserted factor influences the fitted states. Neither alone proves place identity, and a high appearance score cannot replace geometric consistency.

Use the embedded Course checkpoint to explain your default, sweep, fault and recovery records to a colleague. Include one calculation with units, the causal diagnosis and an explicit untested boundary. This is a self-assessment; no learner score is stored.
