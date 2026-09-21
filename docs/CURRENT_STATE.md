# Current state

ELP-ROB-P01-P10 is the active target batch on
`agent/elp-robotics-p01-p10-20260921`, based on exact target main
`71e3842f0839d9534a1c77e9d95d84a929489aff` (tree
`d7716986417df16aeaf1171bd5cc3e40bd3f4295`). Portfolio Control merges
`7dd1278760bda63ea87646738a78c55ff677d69c` and
`d434e7a36dccc9c85577798c80a5e05b0dbfc677` authorize the lane and its narrow
catalog-assertion correction.

The platform now contains a platform-owned `robotics-autonomy` course with
P01-P10 in pinned curriculum order. P01 implements the differential-drive
contract from the read-only source design. P02-P10 are new native Python
designs because their pinned source folders are explicit non-runnable
scaffolds. Every module has equations, declared frames and units, two bounded
sweeps, a named broken/recovery case, deterministic NumPy execution,
Plotly-compatible plots, and distinct expected/actual evidence.

The Robotics source gitlink remains unchanged at
`f8807640258f1a6c1c77f1dcc9e61734551c585b` (tree
`7f8bc62382ca8d7fbe26ff4413cabf7d00d64bb9`). Robotics coverage is 10 authored,
14 remaining, zero blocked, and zero placeholders. DSP/Radar remains 84/84 and
Controls/GNC remains 24/24. The catalog is five courses, 120 modules, and 120
interactive modules.

Python correctness is checked against an oracle module that imports no
production experiment: closed-form and invariant references for kinematics,
trajectory, encoder, and IMU items; continuous-time linear references for the
motor and contact items; and a separately formulated sampled recurrence for
the wheel-speed loop. MATLAB runtime parity remains `not_run` because no
licensed MATLAB runtime is available and P02-P10 have no runnable MATLAB source.

The claim boundary is ten Python-verified software lessons. Browser and
accessibility review, learner effectiveness, physical robot/motor/encoder/IMU,
bench, HIL, field, release, deployment, credentials/settings, and production
operation remain unperformed.
