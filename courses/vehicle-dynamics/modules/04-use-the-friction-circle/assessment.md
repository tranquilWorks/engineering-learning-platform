## P04 evidence task

Compare requests (2800, 3500), (1000, 1000), and (0, 0) N. For each, predict scale and whether the fault will be visible. For the overloaded request, verify the applied magnitude and component ratio. Explain why rectangular clipping would fail.

Record one prediction before running, then retain the actual selected input values, the relevant metric units and two observations from the plotted relationship. Use the nominal sweeps to isolate one variable at a time. Compare the fault and nominal responses at fixed inputs before resetting to the worked baseline. If the two curves coincide, decide whether the lesson's benign limit explains that outcome; a coincident curve is not automatically a successful fault test.

### Reasoning rubric

Only the first request is reduced; the other two have scale one and are benign for the bypass fault. The applied overloaded norm equals 3780 N and direction is preserved. A complete explanation checks a vector invariant and the capacity inequality, including the defined zero-request behavior.

A complete explanation links a quantitative check to its governing relation, distinguishes the requested or formal model result from its stated physical validity, and explains the recovery causally. A partially supported answer reports the expected trend but omits units, an input convention or the fault mechanism. An unsupported answer uses the status badge or curve shape alone as proof. Revise the explanation until a reader could reproduce the comparison from your recorded inputs.

### Check your reasoning

At (2800, 3500) N the request magnitude is about 4482.187 N, utilization 1.18576, and scale about 0.843338. The applied components are about (2361.35, 2951.69) N. Their resultant is 3780 N and their ratio remains 2800/3500 = 0.8. Clipping each component independently to ±3780 N would leave this request unchanged and would therefore fail the combined-force limit.

Do not interpret the requested-utilization metric as the applied-utilization verdict. Do not clamp two components independently or add their absolute values: the declared boundary uses Euclidean magnitude.

Before continuing, state one prediction this model cannot support. Use the specific limitations in the lesson, rather than a general statement that every simulation has limits. This checkpoint is a self-check: **no learner score is stored**, and completing it does not establish measured vehicle performance or learner acceptance.
