# Predict Road-Input Ride Transmissibility

This competency-derived Python-first lesson is not a source conversion and is not a measured-vehicle result. It is a bounded instructional model with explicit units and assumptions.

## Model and equations

- `f=v/lambda_road`
- `H=(k+j c omega)/(k-m omega^2+j c omega)`
- `a_body=|H| z_road omega^2`

Positive lateral force follows the declared body-axis convention, positive bump is upward wheel travel, positive pitch and roll follow right-hand generalized coordinates, and all trigonometric equations use radians internally.

## Baseline workflow

Set the controls to their defaults, predict the sign and dominant magnitude, run the model, and check the response plot, mechanism plot, scalar metrics, and invariant residual before interpreting the result.

## Two one-variable sweeps

Raise speed alone, then double wavelength alone, to show that both change temporal excitation frequency through different physical inputs.

## Intentionally broken case

Use cycles per second directly as angular frequency, moving the apparent resonance and failing the base-excitation equation.

## Recovery

Compute hertz from road speed and wavelength, convert to radians per second, and reevaluate the complex transfer function.

## Limiting cases and invariants

- At zero temporal frequency, displacement transmissibility tends to one and acceleration tends to zero.
- Far above resonance, sprung displacement attenuates even though acceleration weighting by omega squared can remain important.
- Road spatial frequency becomes temporal hertz through speed divided by wavelength, then angular frequency enters the base-excitation equation as two pi times hertz.

## Independent evidence

The five retained scenarios are recomputed by the course-owned independent analytic and numerical reference. That reference imports no production experiment, consumes no production result, and perturbs no production value.

## Common mistakes

- Using road wavelength as though it were temporal period.
- Comparing displacement transmissibility without acceleration.
- Omitting base-motion forcing from the numerator.

## Formative checks

1. What happens to temporal frequency if speed doubles at fixed wavelength?
2. Why does a smooth curve not catch a hertz-versus-radians defect?

## Teach-back

Trace one road wavelength through spatial frequency, temporal hertz, angular frequency, displacement response, and acceleration. Include the relevant units, coordinate convention, validity boundary, named broken behavior, and exact recovery check.
