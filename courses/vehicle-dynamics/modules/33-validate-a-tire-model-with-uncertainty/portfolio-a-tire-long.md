# A-TIRE-LONG integration evidence

Integrate these existing lessons: P05, P26, P27, P29, P30, P31, P32, P33.

Required evidence: Fit and cross-check a longitudinal tire model over load, slip, temperature, and transient sweeps with held-out residuals.

## Derive and predict

Use P05: Explain the sign and local slope of longitudinal tire force and distinguish stiffness from peak force. A signed slip input must produce an odd force response in this symmetric model: reversing slip reverses force. Near zero, differentiate the declared law to obtain stiffness; at larger slip compare force with mu*Fz. Increasing load can raise capacity without changing the interpretation of slip as a dimensionless ratio. Use a negative-slip prediction to expose a sign or percent-versus-fraction error that a positive baseline could hide. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P27: Identify longitudinal stiffness and peak friction from different regimes and reserve unused slip samples for validation. The low-slip slope identifies stiffness while saturated observations identify mu*Fz. A peak alone cannot identify the initial slope. Slip 0.10 is a ratio, not the numeric percent 10; confusing them changes the inferred scale by 100. Fit on the designated observations, then calculate unused-point residuals without refitting. Explain why a dataset entirely inside the linear region cannot independently identify a saturation peak. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P31: Close tire heat balance and apply the gas law using absolute temperature and pressure. With C=15000 J/K and h=35 W/K, thermal time constant is C/h, about 428.57 s. A 900 W constant heat input approaches a 25.71 K temperature rise. Pressure scales with kelvin temperature, so 210 kPa at 293.15 K becomes 210*(T_C+273.15)/293.15 kPa. Celsius ratios can produce nonsense even if the plotted temperature is plausible. Separate the synthetic grip-temperature law from the thermodynamic ledger. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P33: Distinguish residual containment from a conditional prediction interval and prove that validation rows were not fitted. In the one-parameter model y=theta*x+noise, theta_hat=sum(x*y)/sum(x²) on the training prefix only. With declared independent noise sigma, Var(theta_hat)=sigma²/sum(x_train²), and prediction variance at a held-out x is sigma²+x²*Var(theta_hat). The second term widens the predictive band beyond a residual-only 1.96*sigma threshold. Doubling sigma doubles interval widths. Record both containment fractions and the split; fitting validation rows and shrinking sigma changes two distinct assumptions. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Deliver a calibration and validation notebook or table separating low-slip stiffness, saturated peak friction, load exponent, relaxation length and thermal assumptions. Identify which actual observations constrain each parameter and which parameters would be unidentifiable from your chosen data. Carry a normal-load change through peak force, effective friction and paired capacity. Carry a speed change through relaxation time without changing relaxation distance. Close slip-work input against stored and rejected heat. Preserve unused predictions and distinguish the residual-only threshold from a conditional predictive band; deterministic containment is not empirical coverage.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
