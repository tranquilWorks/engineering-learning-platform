# P21 course checkpoint

## Predict and derive

Compare the shorter path with the wider, faster path and audit every candidate's track margin.

Use the governing relations below and state the frame, sign convention and units before substituting numbers. Derive a baseline or limiting prediction and identify which plotted quantity could disprove it.

- `R=45+d; L=pi*45/2+0.08*d^2; v=sqrt(mu*g*R); t=L/v+200/45`

## Controlled comparison

- `friction_coefficient`: 1.05 → 0.7. Hold the other controls at baseline; predict and explain the change before executing.
- `track_half_width_m`: 4 → 6. Hold the other controls at baseline; predict and explain the change before executing.

Record the parameter values, prediction and observed change for each comparison. If a quantity does not change, explain whether it is an invariant, an inactive parameter in this regime, or evidence of a defect.

## Diagnose and recover

Enable the named failure with the numeric controls unchanged. Identify the first violated assumption from the actual trace or event evidence, rather than only the mode label. Restore healthy mode and verify deterministic return to the same baseline. Keep the failing trace beside the recovered trace.

## Expected reasoning

At zero offset, the corner contribution is (pi/2)*45/sqrt(mu*g*45). The model also adds a fixed 200/45 s straight. A nonzero offset changes both radius and the 0.08*d² distance penalty. Evaluate time rather than curvature alone, and require width minus absolute offset to remain nonnegative. A candidate one metre outside the track is invalid regardless of its time advantage.

A complete answer connects a numerical value to the governing relation, distinguishes the controlled comparisons, and explains the fault and recovery through an observable mechanism. An unexplained success metric is insufficient evidence.

## Limits and handoff

The 41-candidate offset search is a bounded geometric proxy, not a dynamically continuous or track-ready racing line.

Competency links: VD-PERFORMANCE-OPTIMIZATION. Carry the prediction, two comparisons, failure diagnosis and recovery evidence into the linked cumulative portfolio. No learner completion or score is inferred by the software; this is an authored assessment for a learner or reviewer to perform.

### Reading the fault/recovery comparison

Each bar uses its own field scale: the larger of the absolute recovered value and one in that field’s declared unit. Thus the plotted ratios are dimensionless; their heights do not compare physical importance across unlike quantities. Hover shows the raw value and scale. The diagnostic key is D1: `best_offset_m`, D2: `effective_radius_m`, D3: `corner_path_length_m`, D4: `grip_speed_limit_m_s`, D5: `lap_time_proxy_s`, D6: `gain_from_center_s`, D7: `constraint_margin_m`, D8: `evaluated_candidates`.
