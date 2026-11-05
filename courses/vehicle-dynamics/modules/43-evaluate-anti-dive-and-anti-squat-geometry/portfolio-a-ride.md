# A-RIDE integration evidence

Integrate these existing lessons: P09, P10, P11, P12, P38, P39, P40, P41, P42, P43.

Required evidence: Compare modal, road-input, damping, roll-transfer, kinematic, compliance, and anti-geometry consequences with physical axes and limits.

## Derive and predict

Use P09: Use virtual work and spring energy to derive the squared motion-ratio law. With motion ratio defined as spring travel divided by wheel travel, spring displacement is r*z. Energy is k_s*(r*z)²/2, so wheel rate is k_s*r². At r=0.9 and k_s=35000 N/m, wheel rate is 28350 N/m. Using r instead of r² violates energy equivalence even if units still look correct. Explicitly distinguish this convention from the reciprocal convention used in some suspension references. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Compare connected mechanisms

Use P12: Separate camber-induced lateral force from the energy lost through toe scrub. Camber thrust follows the signed camber angle in the linear approximation. Scrub power is dissipative and should remain nonnegative when toe reverses: the relevant force and lateral sliding velocity reverse together. Convert degrees once and retain the per-wheel versus axle convention. A sign-preserving force prediction and an even power prediction provide different tests of the same alignment change. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Diagnose and recover

Use P40: Translate a spatial road wavelength into excitation frequency and derive absolute body transmissibility. Road frequency is f=v/lambda and omega=2*pi*f. At 22 m/s over an 8 m wavelength, f=2.75 Hz and omega is about 17.2788 rad/s. For base excitation, H=(k+j*c*omega)/(k-m*omega²+j*c*omega); omitting the numerator's damper term changes the physical forcing. Body acceleration amplitude is omega²*abs(H)*road amplitude. Very slow excitation gives displacement ratio near one, not zero. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Integrate and defend the boundary

Use P43: Show that anti geometry changes the path carrying pitch transfer rather than the total transfer itself. Total longitudinal transfer is m*a*h/L. The declared anti-dive fraction is 0.70*tan(angle)*L/h, while anti-squat omits the 0.70 brake-distribution factor. Geometric and spring-supported contributions must sum to total transfer even when a fraction exceeds one and the spring contribution changes sign. At 5 degrees, use tan(5*pi/180), not tan(5). Explain why changing height affects both the total demand and the anti percentage. Connect this result to at least one other listed lesson, identifying the exact quantity, units and assumption transferred across their interface.

## Required integration artifact

Create a force, energy and modal ledger spanning motion ratio, wheel rate, corner spring geometry, modal kinetic-energy fractions, road transmissibility, damper dissipation and load transfer. Derive the squared motion-ratio relation and demonstrate modal fractions summing to one. At a chosen speed and road wavelength, transfer frequency in Hz into angular frequency before predicting body acceleration. For roll transfer, use wheel loads W/2 +/- T and test the lift-off boundary. Separate travel-dependent alignment from force compliance and explain why anti geometry redistributes pitch-transfer paths rather than eliminating total transfer.

## Four-criterion rubric

1. Governing reasoning: equations, units and frame/sign conventions justify a numerical prediction; naming an algorithm alone earns no evidence.
2. Controlled comparison: two isolated sweeps and at least one limiting case distinguish mechanisms and make a falsifiable claim.
3. Diagnose and recover: identify the first failing assumption from actual outputs, restore it and demonstrate deterministic recovery.
4. Integration and scope: show the value passed between stages, an independently checked result, and a limitation that prevents a broader claim.

Retain inputs, selected outputs and your explanation as a cumulative artifact. No learner completion, automatic score, physical qualification or production acceptance is recorded.
