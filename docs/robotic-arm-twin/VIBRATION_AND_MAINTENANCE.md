# From joint vibration to maintenance decisions

The browser lessons now form a sequence: static two-joint exercise → actual ABB CAD → vibration simulation → maintenance timeline and qualitative fault trees. Restart the Python server after adding these routes. Its printed port applies to all pages.

## Model boundary

The vibration page represents one drive with two inertias: an output-referred motor rotor and a load, joined by a torsional spring/damper. The model is linearized about an equilibrium posture. Its example values are not taken from the ABB manual or CAD. It is not a measured ABB response or a recreation of its controller. Shaft flexibility, motor/load inertia, damping and periodic torque provide a useful system-identification starting point, rather than an arbitrary animated wobble.

The existing STEP-derived geometry remains on its separate CAD page. Vibration is plotted as angular deviations from equilibrium; it has not been applied as calibrated mesh movement.

## Derive the dynamics

Let G be motor revolutions per output revolution. A motor-side rotation is θr = G qm. Substitute into rotational kinetic energy:

`Er = ½ Jr (G q̇m)² = ½ (G² Jr) q̇m²`.

Thus the output-referred motor inertia is `Jm = G² Jr`. Work conservation gives ideal output-referred torque `τout = G τrotor`. The input field already uses output-equivalent torque; do not multiply it by G again. Losses require an identified efficiency/friction model.

The shaft twist is `qm − ql`. A linear torsional spring provides `ks(qm − ql)` torque and a relative damper adds `cs(q̇m − q̇l)`. Equal and opposite shaft torques act on motor and load. An effective holding stiffness `kp` anchors the motor-side deviation to its reference. Applying rotational Newton's law to each inertia gives:

```
Jm q̈m + bm q̇m + kp qm + ks(qm − ql) + cs(q̇m − q̇l) = τ(t)
Jl q̈l + bl q̇l + ks(ql − qm) + cs(q̇l − q̇m) = 0
```

All stiffnesses are N·m/rad; damping is N·m·s/rad; inertias are kg·m². This holding stiffness is a simplified support/feedback approximation, not an ABB control-system identification. Ring-down starts with a selected motor-side displacement and zero load displacement/velocities; periodic torque starts from rest.

In matrix form:

```
M = [[Jm, 0], [0, Jl]]
K = [[kp + ks, −ks], [−ks, ks]]
C = [[bm + cs, −cs], [−cs, bl + cs]]
M q̈ + C q̇ + K q = [τ(t), 0]ᵀ
```

Natural frequencies satisfy `det(K − ω²M) = 0`. Equivalently, take eigenvalues λ of the symmetric mass-normalized matrix `M^(-½) K M^(-½)` and compute `f = √λ / (2π)`. The implementation solves the symmetric 2×2 problem analytically and avoids a subtractive-cancellation expression for the smaller eigenvalue.

For harmonic input, substitute `q = Re(Q exp(iωt))`. Differentiation introduces iω and −ω², giving:

`(K − ω² M + iω C) Q = [A, 0]ᵀ`.

The code solves that complex 2×2 system. The sweep uses A = 1 N·m, so its vertical axis is degrees/N·m. These are steady-state response amplitudes, not an FFT of the finite simulation record. Damped peaks need not coincide with undamped natural frequencies. At an undamped pole, finite steady-state amplitude does not exist; the model rejects singular responses.

Time histories use fourth-order Runge–Kutta, with at least 100 integration steps per fastest natural/excitation cycle and a 1 ms upper step. A step-count ceiling prevents extreme parameters from locking the page. Plotted data is decimated after integration. RMS uses the complete integration samples, not just plotted points. Last-half RMS is not guaranteed settled response.

Energy for free-response checks is `E = ½ q̇ᵀM q̇ + ½ qᵀKq`. Without damping and external input, it should remain constant. With passive damping, `dE/dt = −q̇ᵀCq̇ ≤ 0`. These properties, static compliance, exact modal reference values, and numerical/analytic harmonic agreement are tested.

## What the simulation can teach

Change one parameter at a time. Compare damping at fixed inertias/stiffnesses; change load inertia; compare periodic torque near each natural frequency; compare a free release with a forced response. A small-angle warning appears for large calculated deviations.

A link from the maintenance page loads an **assumed** reduced-stiffness/increased-viscous-friction scenario. That parameter change has no calibrated relationship to overdue hours, wear depth, probability of failure or remaining useful life. Real gearbox wear may involve backlash, impacts, changing friction and multiple modes that this linear model does not represent. Motor-current ripple, electrical harmonics and bearing-defect signatures require additional model inputs and measurements.

## Maintenance schedule provenance and calculation

The detailed source is the independently retrieved [ABB product manual](https://search.abb.com/library/Download.aspx?DocumentID=3HAC085697-001&LanguageCode=en&DocumentPartId=&Action=Launch), document **3HAC085697-001, Revision N**. Its schedule and interval definitions were reviewed on printed/PDF pages **120–122**, including visual confirmation of the table columns and footnotes. A hash/retrieval receipt is stored in `evidence/product_manual_provenance.json`. This is distinct from the supplied product specification **3HAC085704-001, Revision M**.

The app transcribes the schedule into task records with source page numbers. Calendar deadlines add months to each recorded service date, clamping month ends correctly. Hour-based deadlines add the relevant interval to each task's recorded last-service DTC. The initial-hours task requires an explicit completion record and total hours from commissioning. Unknown service history produces unknown due status; it does not silently assume service at commissioning.

Forecast calendar dates for hourly items use the user's assumed future DTC accrual/day. That is a planning projection, not a new OEM deadline. Event-triggered work and actual service procedures can supersede a simple repeating schedule. This starter is not an exhaustive operational maintenance program. Confirm applicability to installed options, duties, records, and site requirements with the applicable manual. Do not infer routine motor servicing merely because the page models a motor: the supplied product specification describes maintenance-free AC motors.

## Fault-tree scope

A fault tree starts at an unwanted outcome and works backward through logical conditions. AND requires all inputs; OR requires one. The implementation has three states: assumed present, assumed absent, and unknown. For example, an AND gate with a known-absent input is false even if another input is unknown; an OR gate with a known-present input is true even if others are unknown.

Each maintenance item selects an illustrative pathway. The top event is scoped to impairment associated with neglected maintenance, rather than all possible causes of robot failure. Inspections are detection barriers: missing an inspection does not necessarily create the underlying defect. An overdue task alone cannot satisfy the tree. A simulated pathway also requires specified adverse conditions and consequences.

The scenarios cover lubrication, seals, balancing components, harnesses, battery/data retention, dampers, stops, labels, and contamination. These are qualitative hypotheses for engineering review; they are not manufacturer failure-probability models. No numerical risk, likelihood, failure date or RUL is generated. A tree whose conditions are satisfied is an internally satisfied scenario, not a diagnosis of the physical robot.

## Turn it into a twin model

1. Verify asset identity, controller version/options, source geometry and actual posture.
2. Establish joint frames and motor/load measurement reference sides.
3. Obtain documented or experimentally identified inertias, stiffness and damping for the relevant posture/load.
4. Record synchronized excitation, motor/load positions, currents and suitable accelerometer signals where available.
5. Fit on one dataset, validate on a separate run, and quantify residual/parameter uncertainty.
6. Link genuine per-component service records and DTC values, rather than the fictional training history.
7. Have the fault-tree structure and causal assumptions reviewed against actual failure evidence and maintenance procedures.
8. Version the model, source evidence, calibration, maintenance records and analytics. Only then use the validated scope to inform operational decisions.

No software here sends robot commands or records fictitious work as completed maintenance. JSON exports explicitly identify hypothetical parameters or unverified/training history.
