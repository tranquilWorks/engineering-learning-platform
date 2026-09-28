### DSP-F10 · Sample, identify and reconstruct

**Competency DSP-C10:** Explain folded and image components during rate changes, and identify the filtering required before decimation and after interpolation.

**Builds on:** [P03 — Make Aliasing Visually Obvious](/courses/dsp-radar/modules/03-make-aliasing-visually-obvious); [P09 — Compare FIR and IIR Filters by Behavior](/courses/dsp-radar/modules/09-compare-fir-and-iir-filters-by-behavior).

**Predict and investigate.** Move high_tone_hz while leaving the rate-change factors fixed, then change reconstruction_taps. Locate the unwanted output component in decimation and explain its cause.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode.
- Diagnose: Drop samples without anti-alias filtering and leave inserted zeros without reconstruction filtering.
- Recover: Low-pass before decimation and after zero insertion, then measure folded and image components.

**Browser recovery.** Turn **Violate the central model assumption** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `fs_out=fs_in/M`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Downsampling folds frequencies into the reduced Nyquist interval unless filtering suppresses them first. Interpolation inserts images that the reconstruction filter must suppress; adding display samples alone does not restore discarded information.

**Limit the claim.** A finite filter has transition bands and edge transients. Do not claim perfect rejection or reconstruction from a single interior trace.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).

### Cumulative assessment DSP-A01 — Sample, identify and reconstruct

Explain a sampled-system result using complex phase, aliasing, noise, convolution and filtering assumptions.

**Evidence portfolio.** Work through the tasks below using the linked laboratories. Keep predictions, settings, dimensioned observations, failure diagnoses and recoveries together.

1. P01–P03: draw the complex rotation and predict the signed alias for 700 Hz at 1000 samples/s. Record P03 signed_alias and apparent_frequency in Hz, then use phase_check to explain why the positive-frequency cosine needs reversed phase.
2. P04–P05: report quantizer step in V, clipped-sample count and noise correlation. Separate overload, finite-bit error, colored noise and a coherent interferer; propose the correct mechanism for each rather than calling all of them noise.
3. P06–P09: use the impulse-response, echo-sum, correlation and filter views to explain a causal signal path. Account for sample delay, initial state, convolution boundaries and ringing.
4. P10: change high_tone_hz and reconstruction_taps separately. Record the decimation and interpolation evidence; enable broken_mode, identify the unwanted component, disable it and verify the original baseline returns.

**Assessment rubric.** All four criteria must be supported by your recorded evidence; a missing criterion means revise that part of the explanation.

- Correct signed alias (-300 Hz), apparent real frequency (300 Hz) and phase convention, with the sampling rate stated.
- A dimensioned quantization/noise diagnosis that distinguishes clipping from ordinary error and coherent interference from random noise.
- A causal explanation linking response, delay and filtering; no claim that added display samples reconstruct lost information.
- Baseline, one-variable sweeps, broken and recovered evidence with explicit finite-filter and observation limits.

**Laboratories:** [P01 — Build a Sinusoid and a Complex Phasor](/courses/dsp-radar/modules/01-build-a-sinusoid-and-a-complex-phasor); [P02 — See Sampling as Taking Measurements](/courses/dsp-radar/modules/02-see-sampling-as-taking-measurements); [P03 — Make Aliasing Visually Obvious](/courses/dsp-radar/modules/03-make-aliasing-visually-obvious); [P04 — Quantize a Signal and Hear/See the Error](/courses/dsp-radar/modules/04-quantize-a-signal-and-hear-see-the-error); [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P06 — Use an Impulse to Reveal a System](/courses/dsp-radar/modules/06-use-an-impulse-to-reveal-a-system); [P07 — Understand Convolution as Echo Addition](/courses/dsp-radar/modules/07-understand-convolution-as-echo-addition); [P08 — Use Correlation to Find a Hidden Pattern](/courses/dsp-radar/modules/08-use-correlation-to-find-a-hidden-pattern); [P09 — Compare FIR and IIR Filters by Behavior](/courses/dsp-radar/modules/09-compare-fir-and-iir-filters-by-behavior); [P10 — Decimate and Interpolate Without Creating Artifacts](/courses/dsp-radar/modules/10-decimate-and-interpolate-without-creating-artifacts).

**Boundary.** This is a portfolio across separate sampled-system experiments, not a newly executed joint hardware chain. This rubric is authored self-assessment guidance, not a record of learner validation.
