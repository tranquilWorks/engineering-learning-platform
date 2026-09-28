# Construct a force- and power-limited acceleration envelope

Tires share one force budget between turning and accelerating. Aerodynamic drag shifts net longitudinal acceleration, while engine power clips the positive-force side. A symmetric acceleration ellipse cannot express all three effects.

## Model and equations

The illustrative mass is 1450 kg, $g=9.81\,\mathrm{m/s^2}$, air density $1.225\,\mathrm{kg/m^3}$, frontal area $2\,\mathrm{m^2}$, downforce coefficient 1.25, drag coefficient 0.36 and available wheel power 210 kW. These are teaching constants, not measured GR86 calibration.

\[D=\tfrac12\rho A C_Lv^2,\quad F_d=\tfrac12\rho A C_Dv^2,\quad C=\mu(mg+D).\]

All three are forces in newtons. Construct a tire-force circle $F_x=C\cos\theta$, $F_y=C\sin\theta$ and clip positive $F_x$ at $P/v$. Plot net accelerations $a_x=(F_x-F_d)/m$, $a_y=F_y/m$ in m/s². The braking extent is $-(C+F_d)/m$, whereas the forward limit is $(\min(C,P/v)-F_d)/m$.

A demand has utilization $u=\sqrt{F_x^2+F_y^2}/C$ and friction excess $\max(0,u-1)$. Healthy demand uses $F_x=\min(0.6C,P/v)$, $F_y=0.6C$. This point is explicitly shown on the envelope.

## Baseline workflow

At 45 m/s and $\mu=1.2$, compute downforce 3100.78 N and drag 893.03 N. The power limit is only $210000/45=4666.67$ N, so available forward acceleration is about 2.603 m/s². Lateral capacity is about 14.338 m/s². Predict the asymmetric envelope before running.

Read the speed-dependent curves and the actual demand marker. The signature order is forward acceleration, braking magnitude, lateral capacity, downforce, drag and friction excess, with units m/s², m/s², m/s², N, N and 1 respectively.

## Two one-variable sweeps

1. Keep friction 1.2 and reduce speed from 45 to 20 m/s. Explain why lower downforce reduces lateral capacity while increased power-per-speed and lower drag improve forward acceleration.
2. Restore speed 45 m/s and raise friction to 1.5. Compare the shared tire boundary with the power ceiling. More grip would not remove a power bottleneck.

## Intentionally broken case

The fault demands 90% of each independent **tire-force capacity**, $F_x=F_y=0.9C$, bypassing both coupling and power guards. Its measured utilization is $\sqrt{0.9^2+0.9^2}=1.272792$, hence friction excess 0.272792. At baseline it also exceeds available power. This differs from asking for 90% of power-limited forward acceleration, which might remain inside the tire circle.

## Recovery

Disable broken mode without changing speed or friction. The shown demand returns to the guarded force allocation. Compare the marker and measured force residual, not only the unchanged capacity curves.

## Limiting cases and invariants

At zero speed in the internal limit, drag and downforce vanish and the forward force is traction-limited; the implementation avoids dividing by zero. At zero drag, the force-to-acceleration shift vanishes. Every healthy demand lies inside the shared tire-force boundary and below the power limit. No launch gearing or transient tire dynamics are modeled.

## Independent evidence

The reference independently computes normal force, available wheel force, net accelerations and demand utilization. Tests verify force balance, dimensions, the finite zero-speed limit and the broken demand's actual power/friction excess.

## Common mistakes

Do not subtract drag from lateral capacity, use a symmetric net-acceleration ellipse, or claim a demand violates grip by inserting a fixed residual unrelated to its forces.

## Teach-back

- Why does braking magnitude include drag? Drag assists deceleration while opposing forward acceleration.
- Why can greater downforce fail to improve acceleration? The engine can remain power-limited.
- Why is the broken point defined in tire-force coordinates? Coupling applies to tire forces; net acceleration also contains drag.

## Formative checks

At 45 m/s, calculate wheel force from 210 kW and subtract 893.025 N drag before dividing by mass. Answer: $4666.667-893.025=3773.642$ N and approximately 2.603 m/s². Next calculate the utilization of a $(0.9C,0.9C)$ demand. Answer: 1.272792; neither the power ceiling nor drag changes this tire-force norm.

This Python-first native lesson is not a source conversion and does not establish a measured-vehicle result.
