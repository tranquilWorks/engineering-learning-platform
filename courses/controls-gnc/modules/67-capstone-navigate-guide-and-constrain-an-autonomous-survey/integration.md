# Survey driven by a coupled navigation estimate

The original planar survey remains a transparent baseline. The new fused survey
executes the P59 strapdown and P61 loosely coupled GNSS/INS mechanisms inside the
guidance loop. Every guidance command uses estimated position and quaternion yaw.
Truth is used only by the plant/sensor simulation and by evaluation metrics.

## Stage trace

The pipeline is commanded turn/speed → accelerated plant → body IMU and six
pseudoranges → 3D mechanization → GNSS solve → 15-state correction/reset → LOS
lookahead → limited turn and freshness hold. The dynamics include a finite 0.35 s
velocity response with per-axis acceleration limited to 3 m/s²; holding commands
braking rather than teleporting velocity to zero.

The local corridor is (0,0) → (20,0) → (20,15) → (0,15) m. Lookahead is 4 m,
nominal desired speed 2 m/s, and the run lasts 30 s at 0.1 s steps. A fix is due
every second, except during [5, 5+dropout) seconds. A stale fix older than 3 s
commands hold. At the next valid fix the estimator corrects and guidance resumes.
This is a bounded mission segment, not evidence that the complete route finished.

## Actual requirements, including failures

The separate fused requirement table checks peak cross-track ≤12 m, turn-rate
excess ≤0, a braking command after the freshness threshold (one-step detection
allowance), and quaternion norm error ≤1e-12. These are computed from the fused
loop, not copied from the planar baseline. Tight 3 deg/s turns can legitimately
fail the cross-track requirement: the approximate minimum radius at 2 m/s is
$2/(3\pi/180)\approx38.2$ m, larger than this corridor. Passing unit tests does
not mean every control setting passes the mission requirements.

Fault mode disables turn limiting and freshness hold and withholds nominal
navigation corrections. The same IMU biases and GNSS observations remain;
formal covariance still updates and must not be mistaken for valid uncertainty.

## Cumulative evidence task

Predict the effect of a 20 s outage on progress versus path error. Run nominal,
zero outage, long outage, minimum turn limit, fault and recovery. Record the
pipeline's actual histories, GNSS update epochs, bias corrections, applied turns,
braking interval, peak cross-track and each requirement verdict. Explain a failed
requirement causally. Show that no measurement correction occurs inside the outage
and that it resumes afterward. Verify that recovery reproduces nominal output.

Compare this integrated path with the retained planar approximation. Name which
stages cause the differences. The estimator is loosely coupled, flat-Earth and
synthetic; it does not claim Earth-rate compensation, receiver multipath modeling,
measured IMU calibration, flight qualification or a completed full survey.

## Evidence boundary

These are bounded synthetic software experiments, not measured navigation or
statistical coverage certification. All state, measurement and covariance histories
are returned by the actual lesson runtime. The independent reference lives in
`recursive_navigation_references.py`; it does not import the lesson implementation.
Historical component plots and their numerical signatures remain intact so the
new integrated behavior can be compared with those limiting cases.

## Further reading

[Solà, Quaternion kinematics for the error-state Kalman filter, sections 5–6](https://arxiv.org/html/1711.02508v1).

The numerical evidence table shows selected epochs (including the first two and final sample); complete histories are retained by the runtime and independent verifier. Values in each column use the units in its label.
