# Current state

`ELP-GNC-GUIDANCE-P63-P65` is the active issue-439 batch from target baseline `be115e914ddcf4aa2a7a8f72146274a832808b3a` (tree `5de83873bb018766aa93069ef3d908ea67210752`) and Portfolio Control merge `6f364109f00a6fd67f5dff8cd96b86bd2227d3a4`.

The reviewed map derives 68 Controls/GNC modules, not a quota. P25-P62 cover control design through navigation and integrity monitoring. P63-P65 now add line-of-sight path following, pursuit and proportional-navigation variants, and terminal guidance under actuator constraints.

Controls/GNC has 65 implemented interactive modules; the five-course catalog has 175 modules and 175 interactive modules. Every native item retains distinct equations, two one-variable sweeps, a broken/recovery path, limiting cases, named invariants, physical axes/units, and separate expected/production evidence for five scenarios.

P66-P68 cumulative capstones remain unimplemented, so curriculum and capstone status remain partial and learner validation remains not run. P01-P62, source/conversion records, other courses, runtime/UI, dependencies, workflows, and deployment files remain unchanged. No MATLAB, browser/accessibility, learner, physical HIL/hardware, certification, release, deployment, credentials/settings, or production result is claimed.
