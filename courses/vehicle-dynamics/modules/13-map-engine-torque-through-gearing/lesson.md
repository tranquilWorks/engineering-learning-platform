# Account for Gearing, Traction and Delivered Power

A larger gear ratio multiplies wheel torque, but it does not create power. A traction limit adds another distinction: the driver can request more engine torque than this algebraic model transmits. Before reading a number, decide whether it describes a request, an applied force, a delivered power, or a loss. Those are different accounting roles even when two happen to agree at the default setting.

## Physical model and units

Vehicle speed is fixed at 20 m/s, wheel radius is 0.315 m, final-drive ratio is 4.1, mass is 1320 kg, and nominal transmission efficiency is 0.90. The selected gear ratio is dimensionless. Requested engine torque is in N·m. With wheel angular speed V/R, engine angular speed is

\[
\omega_e=\frac{V}{R}g_g g_f,\qquad
F_{\mathrm{request}}=\frac{T_{\mathrm{request}}g_g g_f\eta}{R}.
\]

Angular speed is in rad/s; multiply it by 60/(2π) to obtain RPM. The teaching traction cap is F_max = μmg, with μ = 1. Applied wheel force is the smaller of the modeled request and this cap. This deliberately lumped capacity uses the entire vehicle weight; it is not a rear-drive axle load-transfer calculation.

The model assumes instantaneous torque curtailment when capacity is reached. Delivered engine torque is the smaller of requested torque and F_max R/(g_g g_f η). There is no simulated wheelspin, throttle controller or rotational acceleration. This assumption is what allows a consistent fixed-speed power balance even after the requested force exceeds capacity.

\[
P_{\mathrm{request}}=T_{\mathrm{request}}\omega_e,
\quad P_{\mathrm{delivered}}=T_{\mathrm{delivered}}\omega_e,
\quad P_{\mathrm{wheel}}=F_{\mathrm{applied}}V.
\]

Nominal drivetrain dissipation is 0.10 P_delivered. The curtailed request is P_request − P_delivered. Verify two separate balances: requested power equals delivered power plus the curtailed request, and delivered power equals wheel power plus drivetrain loss. A curtailed request is not energy dissipated inside the gearbox. It represents power that the simplified actuator never delivered.

## Worked baseline and saturated case

At 250 N·m and gear ratio 3, the kinematic engine speed is approximately 7457.55 RPM. Requested and applied wheel forces are both 8785.71 N, below the 12949.2 N cap. Requested and delivered shaft powers are about 195238.10 W. Wheel power is 175714.29 W and declared drivetrain loss is 19523.81 W. The budget residual is zero apart from floating-point roundoff.

Now select 320 N·m and ratio 4.2. The force request becomes 15744 N, while applied force remains 12949.2 N. Delivered engine torque falls to about 263.195 N·m. Requested power is 349866.67 W, delivered power is 287760 W, wheel power is 258984 W, and drivetrain loss is 28776 W. The remaining 62106.67 W is a curtailed request. Treating that entire difference as gearbox heat would misdescribe the executed model.

## Predict and sweep

1. Hold ratio 4.2 and vary requested torque from 80 to 320 N·m. The primary panel shows requested and applied force in N. Predict straight-line agreement below capacity and an applied-force plateau above it. The threshold is about 263.195 N·m, so the accessible 260 and 270 N·m settings bracket it. Use the selected metrics to check the delivered torque on either side.
2. Hold requested torque at 320 N·m and vary gear ratio from 0.8 to 4.2. The main response shows force versus ratio; the secondary panel shows engine RPM versus ratio. Predict that RPM keeps increasing after applied force reaches its cap. Explain why a force plateau does not imply a constant engine speed at fixed vehicle speed.

The sweep panels always use the nominal model with the other selected input fixed. The main response follows the selected fault mode. Its full gear-ratio curve helps locate the selected operating point; the metrics report the exact selected ratio. Read each panel’s axes before comparing numerical slopes.

## Named broken behavior and exact recovery

The fault omits the declared 10% loss in the torque-transmission calculation while retaining the traction cap. It therefore uses a lossless force map, even though the displayed accounting still requires 90% efficiency. The power-budget residual measures wheel power plus declared loss minus delivered shaft power. A nonzero residual exposes the inconsistency; reaching the traction cap alone cannot detect it.

Compare nominal and faulty applied-force curves at identical inputs. At saturated settings the applied forces can coincide, so inspect the delivered shaft power and budget residual as well. Disable the fault without moving either control. The nominal force and power balances should return. Only then use Reset parameters to reproduce the worked baseline; resetting inputs and repairing a model are separate actions.

## Limits and limiting cases

The default kinematic RPM already exceeds the separate redline used in P14. That is a reason to distinguish this mapping exercise from engine feasibility, not to treat its RPM as a validated operating point. No real torque curve, redline, gear-dependent efficiency, tire-slip dynamics, axle-specific grip, road load or measured vehicle behavior is included here. A positive force and closed power budget do not establish that a real car can maintain the selected state.

Explain why requested power, delivered power and wheel power differ in the saturated example. Identify the assumption that makes the undelivered portion curtailment rather than dissipation. Then name one additional model needed before choosing a real gear. The embedded checkpoint asks you to retain your own reasoning and evidence; this synthetic lesson does not establish measured-vehicle or learner acceptance.

## Common mistakes

A force cap is not an engine-speed limit. Curtailed requested power is not automatically gearbox heat. A saturated force comparison can hide the loss-omission fault, so check the separate delivered-power balance.

## Formative checks

Why does the saturated example reduce delivered torque while engine RPM still follows gearing? Check your reasoning: speed and ratio set the kinematics; the assumed torque curtailment supplies the force constraint. Explain which balance would fail if all requested power were counted as delivered.

## Teach-back checklist

Reproduce both power balances, locate the traction boundary, and distinguish the two sweep axes. Explain the fault without changing inputs, then name the missing axle-grip and engine-feasibility models. This is synthetic teaching evidence, not measured-vehicle validation.
