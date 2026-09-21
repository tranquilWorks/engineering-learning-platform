# Current state

`ELP-ROB-P01-P24` is the active target batch on
`agent/elp-robotics-p11-p24-20260921`, based directly on target main
`5f6fdae255cf5f188e4ee8a4d50e74949538b8eb` (tree
`568707b6a2db038fd3d3fa66308b8872122f1601`) after P01-P10 merged through PR
#12. Portfolio Control merge `b9437c60a12e6c72918e55b037ef4d49e33166fa`
authorizes P11-P24 as fourteen separately gated work items in one new target
commit and PR #13; merged PR #12 remains immutable.

The platform-owned `robotics-autonomy` course now contains P01-P24 in pinned
curriculum order. P01 implements the differential-drive contract from the
read-only source design. P02-P24 are new native Python designs because their
pinned source folders are explicit non-runnable scaffolds. Every module has
equations, conventions and units, two bounded sweeps, a named broken/recovery
case, deterministic NumPy execution, Plotly-compatible plots, and distinct
expected/actual evidence checked by an oracle that imports no production
experiment.

The Robotics source gitlink remains unchanged at
`f8807640258f1a6c1c77f1dcc9e61734551c585b` (tree
`7f8bc62382ca8d7fbe26ff4413cabf7d00d64bb9`). Robotics coverage is 24 authored,
zero remaining, zero blocked, and zero placeholders. DSP/Radar remains 84/84
and Controls/GNC remains 24/24. The catalog is five courses, 134 modules, and
134 interactive modules.

P11-P24 cover range sensing, extrinsic calibration, odometry, EKF and particle
localization, SLAM, grid and sample-based planning, dynamic-obstacle avoidance,
behavior trees, mission state machines, real-time scheduling, safety monitors,
and deterministic software-only HIL. P24 does not imply a real-time target or
physical hardware loop. MATLAB runtime parity remains `not_run` because no
licensed MATLAB runtime executed and P02-P24 have no runnable MATLAB source.

The claim boundary is twenty-four Python-verified software lessons. Browser and
accessibility acceptance, learner effectiveness, physical robot, motor, sensor,
HIL, bench, field, release, deployment, credentials/settings, and production
operation remain unperformed.
