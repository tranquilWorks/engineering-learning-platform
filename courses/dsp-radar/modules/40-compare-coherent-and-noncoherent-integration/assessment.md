### DSP-F40 · Carry range and Doppler through a radar design

**Competency DSP-C40:** Known phase alignment gives coherent SNR Nρ. Noncoherent power has a different distribution: its standardized separation is √Nρ. The Gaussian-jitter sweep is an ensemble expectation.

**Builds on:** [P05 — Explore White, Colored, and Impulsive Noise](/courses/dsp-radar/modules/05-explore-white-colored-and-impulsive-noise); [P27 — Use Monte Carlo Trials Instead of One Lucky Run](/courses/dsp-radar/modules/27-use-monte-carlo-trials-instead-of-one-lucky-run); [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase); [P37 — Build a Pulse-Doppler Data Matrix](/courses/dsp-radar/modules/37-build-a-pulse-doppler-data-matrix).

**Predict and investigate.** Double pulse_count and compare coherent and noncoherent evidence at fixed input_snr_db. Then break phase alignment and explain the change.

**Evidence to keep.** Write your prediction before manipulating controls. Record baseline settings, one-variable comparisons, the plotted quantity and its units, and the result after restoring the same settings. Use the existing lesson's named failure and recovery:

- Trigger: Enable broken_mode at baseline controls.
- Diagnose: The prescribed 0°,90°,180°,-90° error cycle cancels the clean nominally aligned sum while preserving pulse energy. It is not a typical random-jitter realization.
- Recover: Track and derotate the actual pulse errors to restore unit coherent signal fraction; disable the demonstration to replay the baseline. Recovery assumes known phase errors.

**Browser recovery.** Turn **Enable the named failure** on to capture the fault, then off while holding the other controls at the same values. Compare the recovered evidence with that same-settings healthy run. Use **Reset parameters** to restore the original baseline.

**Explain the relation.** `coherent_power_gain=N for aligned phase and independent noise`. Relate each symbol to a displayed quantity and distinguish samples, seconds, frequency, phase and any power normalization that applies.

**Check your reasoning.** Aligned coherent signal sums linearly while independent noise power sums linearly, producing N-fold SNR gain. Noncoherent energy integration has a different H0 statistic and normalization; raw output heights are not directly comparable detection probabilities.

**Limit the claim.** Coherence and independent noise are assumptions. A drifting target or oscillator can prevent the nominal gain.

**Completion standard.** A satisfactory explanation connects a prediction to measured browser evidence, uses the correct units, explains the failure causally, and identifies a model limit. Merely reproducing a favorable plot or reading this answer is not an assessment pass. No learner score or completion is stored.

Continue the domain assessment at [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).

### Cumulative assessment DSP-A04 — Carry range and Doppler through a radar design

Connect radar power, waveform delay/compression, pulse ambiguity and coherent integration using consistent signs and units.

**Evidence portfolio.** Work through the tasks below using the linked laboratories. Keep predictions, settings, dimensioned observations, failure diagnoses and recoveries together.

1. P29–P31: calculate the power cost of doubled range, the range-bin spacing at 20 MHz and the bandwidth-controlled resolution scale. Use power, ranging and pair to separate sensitivity, accuracy and resolution.
2. P32–P34: vary bandwidth, duration and taper separately. Explain matched-replica conjugation, noise normalization, width/sidelobe tradeoffs and the signed LFM ambiguity ridge.
3. P35–P39: predict the folded range of the 18 km target at 20 kHz, state the Doppler sign convention, identify the matrix dimensions and demonstrate a blind-speed recovery using a genuinely diverse PRF.
4. P40: record coherent_output_snr in dB and active_signal_power_fraction before and after broken_mode. Contrast coherent and noncoherent statistics, restore the same controls, and verify recovered_signal_power_fraction.

**Assessment rubric.** All four criteria must be supported by your recorded evidence; a missing criterion means revise that part of the explanation.

- Two-way range and R^-4 power factors are correct; sample spacing, response width and ambiguity intervals remain distinct.
- Compression and window choices include normalization and a measured cost, not only a favorable peak.
- Doppler phase, matrix axes and PRF diversity explain the observed failures.
- Coherent gain is conditioned on phase alignment and noise assumptions; recovery and finite-record limits are retained.

**Laboratories:** [P29 — Build a Radar Power-Budget Experiment](/courses/dsp-radar/modules/29-build-a-radar-power-budget-experiment); [P30 — Measure Range from Echo Delay](/courses/dsp-radar/modules/30-measure-range-from-echo-delay); [P31 — Separate Range Resolution from Range Accuracy](/courses/dsp-radar/modules/31-separate-range-resolution-from-range-accuracy); [P32 — Perform LFM Pulse Compression](/courses/dsp-radar/modules/32-perform-lfm-pulse-compression); [P33 — Control Pulse-Compression Sidelobes](/courses/dsp-radar/modules/33-control-pulse-compression-sidelobes); [P34 — Plot and Interpret the Ambiguity Function](/courses/dsp-radar/modules/34-plot-and-interpret-the-ambiguity-function); [P35 — Create Unambiguous-Range Aliasing](/courses/dsp-radar/modules/35-create-unambiguous-range-aliasing); [P36 — Measure Doppler from Pulse-to-Pulse Phase](/courses/dsp-radar/modules/36-measure-doppler-from-pulse-to-pulse-phase); [P37 — Build a Pulse-Doppler Data Matrix](/courses/dsp-radar/modules/37-build-a-pulse-doppler-data-matrix); [P38 — Implement a Two-Pulse and Three-Pulse MTI Canceller](/courses/dsp-radar/modules/38-implement-a-two-pulse-and-three-pulse-mti-canceller); [P39 — Expose Blind Speeds and Use Staggered PRF](/courses/dsp-radar/modules/39-expose-blind-speeds-and-use-staggered-prf); [P40 — Compare Coherent and Noncoherent Integration](/courses/dsp-radar/modules/40-compare-coherent-and-noncoherent-integration).

**Boundary.** The portfolio connects design reasoning across retained labs; it is not a measured radar or a newly implemented transmitter/receiver chain. This rubric is authored self-assessment guidance, not a record of learner validation.
