# Robotics and Autonomy authoring contract

This platform-owned derivative follows the pinned `robotics-autonomy-learning` curriculum identity without modifying that source checkout.

- P01 is checked against the implemented differential-drive source design.
- P02-P24 are Python-first native designs because the corresponding source folders are non-runnable scaffolds.
- NumPy performs bounded deterministic calculations; experiments return Plotly-compatible JSON.
- Every lesson exposes equations, units, two one-variable sweeps, one named broken assumption, recovery, limiting cases, and teach-back.
- Independent expected vectors never call the production `experiment.py` implementation.
- MATLAB runtime parity remains `not_run` unless a licensed MATLAB runtime actually executes.
- P24 is software-only HIL methodology; software plots do not establish learner, browser/accessibility, physical robot, physical HIL, bench, field, release, deployment, or production evidence.
