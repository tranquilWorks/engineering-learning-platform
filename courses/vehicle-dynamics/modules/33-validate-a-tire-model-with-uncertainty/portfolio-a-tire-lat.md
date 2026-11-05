# A-TIRE-LAT integration evidence

Integrate these existing lessons: P06, P26, P28, P29, P30, P31, P32, P33.

Required evidence: Fit and cross-check a lateral/combined-slip tire model over slip angle, camber, load, and relaxation sweeps.

## Derive and predict

Use P06: Translate slip angle into radians and derive the small-angle lateral-force prediction. Four degrees is 0.0698132 rad. A stiffness stated in N/rad must multiply that number, not 4. The force sign follows the lesson's explicitly declared slip convention; it should reverse under an angle sign reversal. Compare the linear tangent with the saturation boundary as normal load changes. A factor of about 57.3 is a unit defect, not evidence for a different tire stiffness. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P28: Show why slip-angle and camber excitation must be distinguishable to estimate two stiffnesses. The design matrix has columns alpha and gamma, both in radians, and force is C_alpha*alpha+C_gamma*gamma. If gamma is proportional to alpha, the columns lose rank and only a combination of stiffnesses is identifiable. One degree is pi/180 rad, so a 70000 N/rad coefficient predicts about 1221.73 N per degree in the uncapped linear region. Check held-out predictions and units for both coefficients. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P31: Close tire heat balance and apply the gas law using absolute temperature and pressure. With C=15000 J/K and h=35 W/K, thermal time constant is C/h, about 428.57 s. A 900 W constant heat input approaches a 25.71 K temperature rise. Pressure scales with kelvin temperature, so 210 kPa at 293.15 K becomes 210*(T_C+273.15)/293.15 kPa. Celsius ratios can produce nonsense even if the plotted temperature is plausible. Separate the synthetic grip-temperature law from the thermodynamic ledger. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P33: Distinguish residual containment from a conditional prediction interval and prove that validation rows were not fitted. In the one-parameter model y=theta*x+noise, theta_hat=sum(x*y)/sum(x²) on the training prefix only. With declared independent noise sigma, Var(theta_hat)=sigma²/sum(x_train²), and prediction variance at a held-out x is sigma²+x²*Var(theta_hat). The second term widens the predictive band beyond a residual-only 1.96*sigma threshold. Doubling sigma doubles interval widths. Record both containment fractions and the split; fitting validation rows and shrinking sigma changes two distinct assumptions. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Construct a lateral-force evidence chain from angle convention and camber through two-column fitting, load sensitivity, combined slip and transient response. Retain the design-matrix rank or singular values and a deliberately confounded excitation example. Transfer the fitted stiffness with its N/rad units into a declared small-angle prediction; convert degrees exactly once. Compare the pure-slip pair with the projected shared-capacity pair and demonstrate why individual component limits are insufficient. Include an unused-point residual, a force-direction check and an explicit boundary between this synthetic tire model and measured characterization.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
