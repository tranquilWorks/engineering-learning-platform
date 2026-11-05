# P16 evidence task

## Reconstruct the default operating point

Before running, calculate dynamic pressure at 40 m/s and the two coefficient-area products at 8 degrees. Carry Pa and m² through the force calculation, then multiply drag by speed to obtain power. Reproduce approximately 731.08 N drag, 646.8 N downforce and 29243.2 W drag power demand. Explain why joining these three numbers on one generic SI axis would obscure their meanings.

Calculate front aero share and divide downforce into front and rear contributions. Add the separate 53/47 static-weight distribution to obtain total axle normal loads. Verify both the aero-force sum and total normal-load sum, and explain what each check can and cannot detect.

## Two controlled sweeps

First hold 8 degrees and compare speeds 20 and 40 m/s. Predict the force and power ratios before inspecting the plots. Check fourfold aerodynamic force and eightfold drag power. Explain why total constant-mu tire capacity does not grow by a factor of four: its static-weight term does not scale with speed.

Then hold 40 m/s and compare wing settings 0, 8 and 18 degrees. Use the common force-axis secondary sweep to distinguish the linear downforce-area trend from the quadratic drag-area trend. Quantify the 8-to-18 degree tradeoff: approximately 441 N additional downforce and 15288 W additional drag power. State why those gains and costs alone do not establish an optimal setting.

## Failure and same-input recovery

At the default setting, activate the fault without moving either control. Record negative drag power, a −129.36 N rear aero contribution, and a still-positive rear total normal load of approximately 5956.764 N. Check that total downforce and aggregate capacity can still sum correctly. Identify the sign and allocation checks needed to detect the error. Disable the fault at the same inputs, verify recovery, and reset separately afterward.

## Reasoning rubric

A complete explanation keeps force and power dimensions separate, derives the speed exponents, accounts for static weight, and distinguishes aero contribution from total normal load. It detects the fault even when aggregate sums agree and names the constant-mu/empirical-coefficient limitations.

An incomplete explanation treats negative rear aero contribution as automatic wheel lift, calls a larger wing setting universally better, or scales total capacity as V². Revise those claims from the declared equations and your selected evidence. This formative task records no completion claim: no learner score is stored, and no measured aero, tire qualification or whole-course acceptance is implied.
