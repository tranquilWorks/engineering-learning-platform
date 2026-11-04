# P55 course checkpoint

## Predict and derive

Explain when a roadmap query fails despite many samples.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `V_free={q_i from a deterministic Halton sequence | d(q_i,O)>r_robot}`
- `E={(i,j) | ||q_i-q_j||<=r_connect and segment(q_i,q_j) subset C_free}`
- `J(path)=sum_{(i,j) in path}||q_i-q_j|| solved by Dijkstra search`

## Controlled comparison

- `sample_count`: 100.0 → 50.0. Hold the other controls at baseline and explain the mechanism before executing.
- `connection_radius_m`: 2.0 → 3.0. Hold the other controls at baseline and explain the mechanism before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

Free nodes need collision-checked connections; connection radius and graph reachability matter independently of sample count.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

A missing path in a finite roadmap does not prove geometric impossibility.

Competency links: GLOBAL-MOTION-PLANNING. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.
