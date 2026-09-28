# Current state — course quality continuation

The native browser/container catalog contains four revised engineering curricula:
DSP/Radar **84**, Controls/GNC **68**, Robotics/Autonomy **69**, and Vehicle Dynamics
**67** lessons, plus two examples (**6 courses, 290 interactive modules**). Thirteen
source repositories are pinned; nine remain source-only.

DSP fidelity P01–P84 is implemented and merged through [PR51](https://github.com/tranquilWorks/engineering-learning-platform/pull/51),
merge `b8d760e6721ae0b94aaa503f4ca1599592266442`. Item-level repair completion does
not close aggregate competency or cumulative-assessment acceptance.

The active delivery batch fixes actual math, mobile keyboard/navigation,
revision isolation and numeric browser-control defects, embeds lesson review
notes, and retains per-lesson browser/container checks. Backend contract,
quick/full verification, catalog and focused browser checks passed. The final
all-page desktop/mobile sweep is in progress; see
[delivery evidence](evidence/ELP-COURSE-DELIVERY-QUALITY-01-2026-09-28.md).

Direct semantic inspection reopened twelve lessons: **Controls P66–68,
Robotics P68–69, Vehicle P61–67**. Their specific limitations are visible in the
browser and recorded in [the quality board](COURSE_QUALITY.md). All four courses'
aggregate numerical/curriculum/capstone maturity remains blocked pending the
corresponding reviews. Existing item-level evidence remains available.

The authorized sequence is delivery-quality closure, a separate twelve-lesson
semantic repair, then DSP aggregate competency/cumulative assessment. No new
lesson inventory or source-only conversion is included. Manual screen-reader,
representative learner, MATLAB, physical hardware and production validation
remain unperformed. Hosted CI is separately reported and nonmandatory under the
retained owner direction; required local gates remain mandatory.

The wider model review subsequently found 44 additional issues beyond the first
twelve, for **56 affected lessons**. See
[the additional register](course-quality/additional-semantic-findings.md). The
first twelve-lesson repair contract does not cover those 44; they remain blocked
pending separate scope and implementation. No aggregate acceptance follows from
finishing only the initial group.
