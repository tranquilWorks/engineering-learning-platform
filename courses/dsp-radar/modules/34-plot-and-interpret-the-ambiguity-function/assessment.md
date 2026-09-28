### DSP-F34 · Carry range and Doppler through a radar design

**Competency DSP-C34:** Delay-Doppler sums use only zero-filled overlap. Rectangle, LFM and a seeded 13-chip code expose different cuts; the LFM ridge follows fd divided by chirp rate.

**Builds on:** [P08 — Use Correlation to Find a Hidden Pattern](/courses/dsp-radar/modules/08-use-correlation-to-find-a-hidden-pattern); [P32 — Perform LFM Pulse Compression](/courses/dsp-radar/modules/32-perform-lfm-pulse-compression); [P33 — Control Pulse-Compression Sidelobes](/courses/dsp-radar/modules/33-control-pulse-compression-sidelobes).

**Predict and investigate.** Compare the delay and Doppler cuts of the rectangular pulse and LFM response. Predict the LFM ridge direction under the displayed Doppler sign convention.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: Circularly wrapping the rectangular pulse produces unit correlation even at extreme delay, inventing overlap that propagation cannot supply.
- Recover: Disable the failure to restore finite zero-filled overlap; the extreme-delay magnitude returns to 1/N.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `chi(tau,nu)=integral s(t) conjugate(s(t-tau)) exp(-j 2 pi nu t) dt`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Delay/Doppler mismatch changes both overlap and coherent phase. LFM couples delay with Doppler along a ridge, whereas a finite pulse's overlap must decay near extreme delay. Circular correlation would invent overlap across record boundaries.

**Limit the claim.** The ambiguity surface describes a waveform and convention, not a complete detector or multi-target scene.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).
