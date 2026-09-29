### DSP-F33 · Carry range and Doppler through a radar design

**Competency DSP-C33:** Cosine receive weighting lowers sidelobes while broadening the mainlobe and losing output SNR. Weak-target margin compares its peak with strong-target leakage.

**Builds on:** [P12 — Separate Leakage from Noise](/courses/dsp-radar/modules/12-separate-leakage-from-noise); [P32 — Perform LFM Pulse Compression](/courses/dsp-radar/modules/32-perform-lfm-pulse-compression).

**Predict and investigate.** Compare taper_strength=0 and 1 at fixed separation_samples. Use taper_width, taper_cost and scene to decide whether the weaker target benefits.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The failure forces full Hann weighting and seven-sample separation: low sidelobes alone do not reveal a target inside the broadened response.
- Recover: Disable the failure and restore 17-sample separation with full taper; inspect margin, local peak and width together.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `normalized_taper_noise_loss=N sum(w^2)/(sum w)^2 for equal-amplitude samples`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Lower sidelobes can reveal a neighbor, but the widened mainlobe may merge close targets and tapering costs matched-filter SNR. A favorable PSLR alone does not settle the detection outcome.

**Limit the claim.** Keep strong-target normalization and weak-target offset fixed during the comparison; otherwise visibility changes have multiple causes.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
