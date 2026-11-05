## P08 evidence task

Use the sliders to select understeer and oversteer pairs, then derive a neutral pair algebraically within the allowed stiffness ranges. The slider steps do not generally reach exact neutral steer: report that boundary as a calculated case rather than claiming you selected it. For each case, report K, critical-speed availability and the steering trend with speed. At a fixed non-neutral pair compare nominal and omission at 25 m/s, then explain why the fault is invisible at neutral.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

The sign of K classifies the three setups; only negative K outside the numerical neutral band yields a finite critical speed. Neutral satisfies l_r/C_f = l_f/C_r. The omission removes K a_y from steer and K V² from the denominator. Full reasoning separates formal algebra, stable operation and unavailable metrics.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

With C_f = 90000 and C_r = 100000 N/rad, K = 0.00219715 s²/m and the gradient is about 1.23495 deg/g. At 25 m/s the denominator is 3.94322 m. For a_y = 1 m/s², δ ≈ 0.36149°. There is no oversteer critical speed for this positive K. Neutral steer occurs when C_f/C_r = l_r/l_f ≈ 1.23478, rather than when the two stiffnesses are simply equal.

A displayed internal zero sentinel is not a physical critical speed. Equal axle stiffness is not generally neutral steer, because lever arms and static axle loads differ. Removing K from an equation does not remove the underlying vehicle compliance.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
