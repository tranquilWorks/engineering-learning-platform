# Course roots

This directory contains built-in fixtures and examples plus the independently
versioned engineering curricula. The production curricula are Git submodules,
so their source repositories remain canonical while this platform pins a
reviewed revision of each course.

- `_template/` — minimal authoring seed; underscore prefix excludes it from discovery.
- `platform-showcase/` — exercises advanced generic plots and tables.
- `demo-radar/` — real interactive echo-ranging vertical slice derived from the DSP/radar curriculum.

The pinned course repositories are:

- `controls-gnc-learning`
- `distributed-realtime-learning`
- `dsp-radar-learning`
- `embedded-rt-hil-learning`
- `flight-dynamics-learning`
- `fpga-data-path-learning`
- `hwil-systems-learning`
- `numerical-optimization-learning`
- `reliability-fdir-learning`
- `rf-lab-learning`
- `robotics-autonomy-learning`
- `stats-estimation-learning`
- `vehicle-dynamics-learning`

Initialize them after cloning the platform with:

```bash
git submodule update --init --recursive
```

A mounted path can be a single course root containing `course.yaml` or a collection whose immediate children contain `course.yaml`.
