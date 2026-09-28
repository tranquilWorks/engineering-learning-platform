# Current engineering-learning position — 2026-09-28

All 288 native engineering lessons and two examples are embedded in Engineering
Learning: six courses, 290 interactive modules. Nine other pinned sources remain
source-only. Inventory does not establish course-wide quality acceptance.

The twelve-lesson revision is implemented and locally verified in
[PR53](https://github.com/tranquilWorks/engineering-learning-platform/pull/53):
Controls P66–P68, Robotics P68–P69 and Vehicle P61–P67 now execute the declared
bounded mechanisms and expose computed requirements. Sixty independent comparisons,
40 physical/preservation tests, mandatory contract/quick/full gates, 290 container
HTTP checks, 580 desktop/mobile pages and 36 interactions passed. Generic 2D plots
fall back to SVG when WebGL initialization fails; actual curves and label spacing
were reviewed. See the exact [evidence](evidence/ELP-SEMANTIC-QUALITY-12-2026-09-28.md).

The browser retains **60 additional blocked findings**: Controls 19, Robotics 25,
Vehicle 16. These are separate repair scopes; the twelve fixes do not promote
those course aggregates. The initial audit found 72 affected lessons.

Next is the separately contracted DSP aggregate review: embed all 84 authored
checkpoints, ten cumulative assessments and their competency/prerequisite map,
replay the 417 retained independent comparisons, and verify actual browser access.
These drafts are not yet embedded or accepted. Start from the actual PR53 merge.

Representative learner, manual screen-reader, MATLAB, measured vehicle/hardware
and production validation remain not_run. Concurrent-user capacity is not
certified; browser experiment requests are paced one at a time. Hosted CI is
reported separately and is not claimed green. No production deployment occurred.

Browser recheck boundary: the final all-page invocation exited 1 after one
Robotics P58 mobile request exceeded its unchanged three-second deadline. It
retained 579 initial passes. Three isolated desktop/mobile repetitions on the
same image passed all six checks; the reconciled 580 identities retain the
original failed row and links to every recheck. This is not an initial clean
sweep or concurrent-capacity certification; the timeout cause is not proven.
