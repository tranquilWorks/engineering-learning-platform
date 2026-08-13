# Course roots

This directory contains built-in fixtures and examples. Production courses should generally remain independent repositories and be mounted read-only through `ELP_COURSE_PATHS`.

- `_template/` — minimal authoring seed; underscore prefix excludes it from discovery.
- `platform-showcase/` — exercises advanced generic plots and tables.
- `demo-radar/` — real interactive echo-ranging vertical slice derived from the DSP/radar curriculum.

A mounted path can be a single course root containing `course.yaml` or a collection whose immediate children contain `course.yaml`.
