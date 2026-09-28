# DSP aggregate quality revision — verification in progress

Control PR539 merged as 3eb977ec9015b8415426a9c5f3c5bcd639bdec64 after full local
control-plane validation. Hosted control validation did not start because GitHub
reported a payment/spending-limit restriction; no settings change or administrative
merge bypass occurred. Target baseline is merged PR53 b107ac198543e8dfb563c6aae4175cc87da6210d,
tree 21028d29c7e5f139f6907c6fcf7f467d96bbbfe8.

84 individually authored checkpoints, ten cumulative task/rubric portfolios and
the competency/prerequisite map are implemented, with generic markdown navigation
and lesson-specific assessment disclosures. Existing numerical/source payloads
remain unchanged; only referenced assessment target identities are reconciled.
The first replay passed 417 independent cases and 14 focused checks passed.
Explicit same-settings browser fault recovery and reset instructions were then
added; final replay and full local/browser/container checks are pending.

Initial validation caught JSON scientific-notation numbers being treated as YAML
strings. Original manifests/provenance were restored, readers now respect the
actual file format, and strict baseline preservation checks passed after regeneration.
The schema test uses the repository's existing validator; no dependency was added.

All sixty other findings and their course aggregates remain blocked. Human learner,
manual screen-reader, MATLAB, hardware and production acceptance remain not_run.
Final exact results, image identity and merge state will replace this draft.
