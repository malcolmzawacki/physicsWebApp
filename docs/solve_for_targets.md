# Available solve-for targets

Reference for the checked-in catalog. Target IDs are scoped to generator and problem type.

## ConstantMotionGenerator

### Constant Speed

| Target | ID | Levels |
|---|---|---|
| Distance | `inst-speed-question.distance` | Easy, Medium, Hard |
| Speed | `inst-speed-question.speed` | Easy, Medium, Hard |
| Time | `inst-speed-question.time` | Easy, Medium, Hard |

## MomentumGenerator

### Momentum

| Target | ID | Levels |
|---|---|---|
| Momentum | `momentum-q.momentum` | Easy, Medium, Hard |
| Mass | `momentum-q.mass` | Easy, Medium, Hard |
| Velocity | `momentum-q.velocity` | Easy, Medium, Hard |

## LinearMotionGenerator

### No Time

| Target | ID | Levels |
|---|---|---|
| Acceleration | `no-time-question.acceleration` | Easy, Medium, Hard |
| Final velocity | `no-time-question.final-velocity` | Easy, Medium, Hard |
| Initial velocity | `no-time-question.initial-velocity` | Easy, Medium, Hard |
| Displacement | `no-time-question.displacement` | Easy, Medium, Hard |

### No Distance

| Target | ID | Levels |
|---|---|---|
| Acceleration | `no-dist-question.acceleration` | Easy, Medium, Hard |
| Final velocity | `no-dist-question.final-velocity` | Easy, Medium, Hard |
| Initial velocity | `no-dist-question.initial-velocity` | Easy, Medium, Hard |
| Time | `no-dist-question.time` | Easy, Medium, Hard |

### No Acceleration

| Target | ID | Levels |
|---|---|---|
| Time | `no-acc-question.time` | Easy, Medium, Hard |
| Displacement | `no-acc-question.displacement` | Easy, Medium, Hard |
| Final velocity | `no-acc-question.final-velocity` | Easy, Medium, Hard |
| Initial velocity | `no-acc-question.initial-velocity` | Easy, Medium, Hard |

### No Final Velocity

| Target | ID | Levels |
|---|---|---|
| Displacement | `no-vf-question.displacement` | Easy, Medium, Hard |
| Time | `no-vf-question.time` | Easy, Medium, Hard |
| Initial velocity | `no-vf-question.initial-velocity` | Easy, Medium, Hard |
| Acceleration | `no-vf-question.acceleration` | Easy, Medium, Hard |

## RotationalMotionGenerator

### No Time

| Target | ID | Levels |
|---|---|---|
| Angular acceleration | `no-time-question.angular-acceleration` | Easy, Medium, Hard |
| Final angular velocity | `no-time-question.final-angular-velocity` | Easy, Medium, Hard |
| Initial angular velocity | `no-time-question.initial-angular-velocity` | Easy, Medium, Hard |
| Angular displacement | `no-time-question.angular-displacement` | Easy, Medium, Hard |

### No Distance

| Target | ID | Levels |
|---|---|---|
| Angular acceleration | `no-dist-question.angular-acceleration` | Easy, Medium, Hard |
| Final angular velocity | `no-dist-question.final-angular-velocity` | Easy, Medium, Hard |
| Initial angular velocity | `no-dist-question.initial-angular-velocity` | Easy, Medium, Hard |
| Time | `no-dist-question.time` | Easy, Medium, Hard |

### No Acceleration

| Target | ID | Levels |
|---|---|---|
| Time | `no-acc-question.time` | Easy, Medium, Hard |
| Angular displacement | `no-acc-question.angular-displacement` | Easy, Medium, Hard |
| Final angular velocity | `no-acc-question.final-angular-velocity` | Easy, Medium, Hard |
| Initial angular velocity | `no-acc-question.initial-angular-velocity` | Easy, Medium, Hard |

### No Final Velocity

| Target | ID | Levels |
|---|---|---|
| Angular displacement | `no-vf-question.angular-displacement` | Easy, Medium, Hard |
| Time | `no-vf-question.time` | Easy, Medium, Hard |
| Initial angular velocity | `no-vf-question.initial-angular-velocity` | Easy, Medium, Hard |
| Angular acceleration | `no-vf-question.angular-acceleration` | Easy, Medium, Hard |

## AtwoodGenerator

### Static Friction Half Atwood

| Target | ID | Levels |
|---|---|---|
| Tension | `static-half-atwood.tension` | Easy, Medium, Hard |
| Mass 1 | `static-half-atwood.mass-1` | Easy, Medium, Hard |
| Mass 2 | `static-half-atwood.mass-2` | Easy, Medium, Hard |
| Coefficient of friction | `static-half-atwood.coefficient-of-friction` | Easy, Medium, Hard |

### Frictionless Half Atwood

| Target | ID | Levels |
|---|---|---|
| Tension | `frictionless-half-atwood.tension` | Easy, Medium, Hard |
| Mass 1 | `frictionless-half-atwood.mass-1` | Easy, Medium, Hard |
| Mass 2 | `frictionless-half-atwood.mass-2` | Easy, Medium, Hard |
| Acceleration | `frictionless-half-atwood.acceleration` | Easy, Medium, Hard |

### Kinetic Friction Half Atwood

| Target | ID | Levels |
|---|---|---|
| Acceleration and tension | `kinetic-half-atwood.acceleration-and-tension` | Easy, Medium, Hard |
| Acceleration and coefficient | `kinetic-half-atwood.acceleration-and-coefficient` | Easy, Medium, Hard |
| Coefficient and tension | `kinetic-half-atwood.coefficient-and-tension` | Easy, Medium, Hard |
| Mass 2 and acceleration | `kinetic-half-atwood.mass-2-and-acceleration` | Easy, Medium, Hard |
| Mass 2 and tension | `kinetic-half-atwood.mass-2-and-tension` | Easy, Medium, Hard |
| Mass 2 and coefficient | `kinetic-half-atwood.mass-2-and-coefficient` | Easy, Medium, Hard |
| Mass 1 and acceleration | `kinetic-half-atwood.mass-1-and-acceleration` | Easy, Medium, Hard |
| Mass 1 and tension | `kinetic-half-atwood.mass-1-and-tension` | Easy, Medium, Hard |
| Mass 1 and coefficient | `kinetic-half-atwood.mass-1-and-coefficient` | Easy, Medium, Hard |
| Mass 1 and mass 2 | `kinetic-half-atwood.mass-1-and-mass-2` | Easy, Medium, Hard |

## InclineGenerator

### Static Incline

| Target | ID | Levels |
|---|---|---|
| Maximum angle | `static-incline.maximum-angle` | Easy, Medium, Hard |
| Minimum static friction coefficient | `static-incline.minimum-static-friction-coefficient` | Easy, Medium, Hard |

### Frictionless Incline

| Target | ID | Levels |
|---|---|---|
| Angle | `frictionless-incline.angle` | Easy, Medium, Hard |
| Acceleration | `frictionless-incline.acceleration` | Easy, Medium, Hard |

### Kinetic Friction Incline

| Target | ID | Levels |
|---|---|---|
| Acceleration | `kinetic-friction-incline.acceleration` | Easy, Medium, Hard |
| Kinetic friction coefficient | `kinetic-friction-incline.kinetic-friction-coefficient` | Easy, Medium, Hard |

## ImpulseGenerator

### Impulse

| Target | ID | Levels |
|---|---|---|
| Change in momentum | `impulse-q.change-in-momentum` | Easy |
| Force | `impulse-q.force` | Easy, Medium, Hard |
| Time | `impulse-q.time` | Easy, Medium, Hard |
| Mass | `impulse-q.mass` | Medium, Hard |
| Change in velocity | `impulse-q.change-in-velocity` | Medium |
| Initial velocity | `impulse-q.initial-velocity` | Hard |
| Final velocity | `impulse-q.final-velocity` | Hard |

### Change in Momentum

| Target | ID | Levels |
|---|---|---|
| Change in momentum | `change-in-momentum.change-in-momentum` | Easy, Medium, Hard |
| Initial momentum | `change-in-momentum.initial-momentum` | Easy |
| Final momentum | `change-in-momentum.final-momentum` | Easy |
| Mass | `change-in-momentum.mass` | Medium, Hard |
| Change in velocity | `change-in-momentum.change-in-velocity` | Medium |
| Initial velocity | `change-in-momentum.initial-velocity` | Hard |
| Final velocity | `change-in-momentum.final-velocity` | Hard |

## ProjectileGenerator

### Type 1

| Target | ID | Levels |
|---|---|---|
| Horizontal distance | `generate-type1-question.horizontal-distance` | Easy |
| Cliff height | `generate-type1-question.cliff-height` | Easy |
| Initial speed | `generate-type1-question.initial-speed` | Easy |
| Final speed and horizontal distance | `generate-type1-question.final-speed-and-horizontal-distance` | Medium, Hard |
| Initial speed and cliff height | `generate-type1-question.initial-speed-and-cliff-height` | Medium, Hard |
| Final speed and landing angle | `generate-type1-question.final-speed-and-landing-angle` | Medium, Hard |

### Type 2

| Target | ID | Levels |
|---|---|---|
| Initial speed and launch angle | `generate-type2-question.initial-speed-and-launch-angle` | Medium, Hard |
| Initial speed and horizontal distance | `generate-type2-question.initial-speed-and-horizontal-distance` | Medium, Hard |
| Launch angle and horizontal distance | `generate-type2-question.launch-angle-and-horizontal-distance` | Medium, Hard |

### Type 3

| Target | ID | Levels |
|---|---|---|
| Horizontal distance and final speed (off cliff) | `range-speed` | Easy |
| Horizontal distance and landing angle (onto cliff) | `range-angle` | Easy |
| Cliff height and landing speed (onto cliff) | `height-speed` | Easy |
| Launch setback and return-to-height time (off cliff) | `setback-time` | Medium, Hard |
| Launch angle and distance to cliff (onto cliff) | `angle-range` | Medium, Hard |

## EnergyBasicsGenerator

### Elastic Potential Energy

| Target | ID | Levels |
|---|---|---|
| Elastic Potential Energy | `elastic-problem.elastic-potential-energy` | Easy, Medium, Hard |
| Compression Distance | `elastic-problem.compression-distance` | Medium, Hard |
| Spring Strength | `elastic-problem.spring-strength` | Medium, Hard |

### Kinetic Energy

| Target | ID | Levels |
|---|---|---|
| Kinetic Energy | `kinetic-problem.kinetic-energy` | Easy, Medium, Hard |
| Velocity | `kinetic-problem.velocity` | Medium, Hard |
| Mass | `kinetic-problem.mass` | Medium, Hard |

### Gravitational Potential Energy

| Target | ID | Levels |
|---|---|---|
| Gravitational Potential Energy | `gravitational-problem.gravitational-potential-energy` | Easy, Medium, Hard |
| Height | `gravitational-problem.height` | Medium, Hard |
| Mass | `gravitational-problem.mass` | Medium, Hard |

### Work

| Target | ID | Levels |
|---|---|---|
| Work | `work-problem.work` | Easy, Medium, Hard |
| Distance | `work-problem.distance` | Medium, Hard |
| Force | `work-problem.force` | Medium, Hard |

## EnergyConservationGenerator

### Gravitational <--> Kinetic

| Target | ID | Levels |
|---|---|---|
| Velocity | `kinetic-gravitational-problem.velocity` | Easy, Medium, Hard |
| Height | `kinetic-gravitational-problem.height` | Easy, Medium, Hard |

### Gravitational <--> Elastic

| Target | ID | Levels |
|---|---|---|
| Spring Strength | `elastic-gravitational-problem.spring-strength` | Easy, Medium, Hard |
| Height | `elastic-gravitational-problem.height` | Easy, Medium, Hard |
| Compression Distance | `elastic-gravitational-problem.compression-distance` | Easy, Medium, Hard |
| Mass | `elastic-gravitational-problem.mass` | Easy, Medium, Hard |

### Elastic <--> Kinetic

| Target | ID | Levels |
|---|---|---|
| Spring Strength | `elastic-kinetic-problem.spring-strength` | Easy, Medium, Hard |
| Velocity | `elastic-kinetic-problem.velocity` | Easy, Medium, Hard |
| Compression Distance | `elastic-kinetic-problem.compression-distance` | Easy, Medium, Hard |
| Mass | `elastic-kinetic-problem.mass` | Easy, Medium, Hard |

## ThermalLossGenerator

### Gravitational <--> Kinetic

| Target | ID | Levels |
|---|---|---|
| Work done by Friction (gravitational to kinetic) | `grav-to-kin-thermal-q.work-done-by-friction-grav-to-kin` | Easy, Medium, Hard |
| Velocity (gravitational to kinetic) | `grav-to-kin-thermal-q.velocity-grav-to-kin` | Medium, Hard |
| Height (gravitational to kinetic) | `grav-to-kin-thermal-q.height-grav-to-kin` | Medium, Hard |
| Work done by Friction (kinetic to gravitational) | `kin-to-grav-thermal-q.work-done-by-friction-kin-to-grav` | Easy, Medium, Hard |
| Velocity (kinetic to gravitational) | `kin-to-grav-thermal-q.velocity-kin-to-grav` | Medium, Hard |
| Height (kinetic to gravitational) | `kin-to-grav-thermal-q.height-kin-to-grav` | Medium, Hard |

### Gravitational <--> Elastic

| Target | ID | Levels |
|---|---|---|
| Work done by Friction (gravitational to elastic) | `grav-to-elastic-thermal-q.work-done-by-friction-grav-to-elastic` | Easy, Medium, Hard |
| Spring Strength (gravitational to elastic) | `grav-to-elastic-thermal-q.spring-strength-grav-to-elastic` | Medium, Hard |
| Compression Distance (gravitational to elastic) | `grav-to-elastic-thermal-q.compression-distance-grav-to-elastic` | Medium, Hard |
| Mass (gravitational to elastic) | `grav-to-elastic-thermal-q.mass-grav-to-elastic` | Medium, Hard |
| Ramp Height (gravitational to elastic) | `grav-to-elastic-thermal-q.ramp-height-grav-to-elastic` | Medium, Hard |
| Work done by Friction (elastic to gravitational) | `elastic-to-grav-thermal-q.work-done-by-friction-elastic-to-grav` | Easy, Medium, Hard |
| Spring Strength (elastic to gravitational) | `elastic-to-grav-thermal-q.spring-strength-elastic-to-grav` | Medium, Hard |
| Compression Distance (elastic to gravitational) | `elastic-to-grav-thermal-q.compression-distance-elastic-to-grav` | Medium, Hard |
| Mass (elastic to gravitational) | `elastic-to-grav-thermal-q.mass-elastic-to-grav` | Medium, Hard |
| Ramp Height (elastic to gravitational) | `elastic-to-grav-thermal-q.ramp-height-elastic-to-grav` | Medium, Hard |

### Elastic <--> Kinetic

| Target | ID | Levels |
|---|---|---|
| Work done by Friction (kinetic to elastic) | `kinetic-to-elastic-thermal-q.work-done-by-friction-kinetic-to-elastic` | Easy, Medium, Hard |
| Spring Strength (kinetic to elastic) | `kinetic-to-elastic-thermal-q.spring-strength-kinetic-to-elastic` | Medium, Hard |
| Compression Distance (kinetic to elastic) | `kinetic-to-elastic-thermal-q.compression-distance-kinetic-to-elastic` | Medium, Hard |
| Mass (kinetic to elastic) | `kinetic-to-elastic-thermal-q.mass-kinetic-to-elastic` | Medium, Hard |
| Velocity (kinetic to elastic) | `kinetic-to-elastic-thermal-q.velocity-kinetic-to-elastic` | Medium, Hard |
| Work done by Friction (elastic to kinetic) | `elastic-to-kinetic-thermal-q.work-done-by-friction-elastic-to-kinetic` | Easy, Medium, Hard |
| Spring Strength (elastic to kinetic) | `elastic-to-kinetic-thermal-q.spring-strength-elastic-to-kinetic` | Medium, Hard |
| Compression Distance (elastic to kinetic) | `elastic-to-kinetic-thermal-q.compression-distance-elastic-to-kinetic` | Medium, Hard |
| Mass (elastic to kinetic) | `elastic-to-kinetic-thermal-q.mass-elastic-to-kinetic` | Medium, Hard |
| Velocity (elastic to kinetic) | `elastic-to-kinetic-thermal-q.velocity-elastic-to-kinetic` | Medium, Hard |

## ThermalWithFrictionGenerator

### Gravitational <--> Kinetic

| Target | ID | Levels |
|---|---|---|
| Thermal Energy and Final Velocity (grav to kinetic) | `grav-to-kinetic-friction-distance-q.thermal-energy-and-final-velocity-grav-to-kinetic` | Easy |
| Thermal Energy and Ramp Height (grav to kinetic) | `grav-to-kinetic-friction-distance-q.thermal-energy-and-ramp-height-grav-to-kinetic` | Easy |
| Thermal Energy and Mass (grav to kinetic) | `grav-to-kinetic-friction-distance-q.thermal-energy-and-mass-grav-to-kinetic` | Easy |
| Final Velocity (grav to kinetic) | `grav-to-kinetic-friction-distance-q.final-velocity-grav-to-kinetic` | Medium, Hard |
| Ramp Height (grav to kinetic) | `grav-to-kinetic-friction-distance-q.ramp-height-grav-to-kinetic` | Medium, Hard |
| Mass (grav to kinetic) | `grav-to-kinetic-friction-distance-q.mass-grav-to-kinetic` | Medium, Hard |
| Ramp Length (grav to kinetic) | `grav-to-kinetic-friction-distance-q.ramp-length-grav-to-kinetic` | Medium, Hard |
| Force of Friction (grav to kinetic) | `grav-to-kinetic-friction-distance-q.force-of-friction-grav-to-kinetic` | Medium, Hard |
| Thermal Energy and Initial Velocity (kinetic to grav) | `kinetic-to-grav-friction-distance-q.thermal-energy-and-final-velocity-kinetic-to-grav` | Easy |
| Thermal Energy and Ramp Height (kinetic to grav) | `kinetic-to-grav-friction-distance-q.thermal-energy-and-ramp-height-kinetic-to-grav` | Easy |
| Thermal Energy and Mass (kinetic to grav) | `kinetic-to-grav-friction-distance-q.thermal-energy-and-mass-kinetic-to-grav` | Easy |
| Initial Velocity (kinetic to grav) | `kinetic-to-grav-friction-distance-q.final-velocity-kinetic-to-grav` | Medium, Hard |
| Ramp Height (kinetic to grav) | `kinetic-to-grav-friction-distance-q.ramp-height-kinetic-to-grav` | Medium, Hard |
| Mass (kinetic to grav) | `kinetic-to-grav-friction-distance-q.mass-kinetic-to-grav` | Medium, Hard |
| Ramp Length (kinetic to grav) | `kinetic-to-grav-friction-distance-q.ramp-length-kinetic-to-grav` | Medium, Hard |
| Force of Friction (kinetic to grav) | `kinetic-to-grav-friction-distance-q.force-of-friction-kinetic-to-grav` | Medium, Hard |

### Gravitational <--> Elastic

| Target | ID | Levels |
|---|---|---|
| Thermal Energy and Spring Compression (gravitational to elastic) | `grav-to-elastic-friction-distance-q.thermal-energy-and-spring-compression-grav-to-elastic` | Easy |
| Thermal Energy and Spring Constant (gravitational to elastic) | `grav-to-elastic-friction-distance-q.thermal-energy-and-spring-constant-grav-to-elastic` | Easy |
| Thermal Energy and Ramp Height (gravitational to elastic) | `grav-to-elastic-friction-distance-q.thermal-energy-and-ramp-height-grav-to-elastic` | Easy |
| Thermal Energy and Mass (gravitational to elastic) | `grav-to-elastic-friction-distance-q.thermal-energy-and-mass-grav-to-elastic` | Easy |
| Spring Compression (gravitational to elastic) | `grav-to-elastic-friction-distance-q.spring-compression-grav-to-elastic` | Medium, Hard |
| Spring Constant (gravitational to elastic) | `grav-to-elastic-friction-distance-q.spring-constant-grav-to-elastic` | Medium, Hard |
| Mass (gravitational to elastic) | `grav-to-elastic-friction-distance-q.mass-grav-to-elastic` | Medium, Hard |
| Ramp Length (gravitational to elastic) | `grav-to-elastic-friction-distance-q.ramp-length-grav-to-elastic` | Medium, Hard |
| Ramp Height (gravitational to elastic) | `grav-to-elastic-friction-distance-q.ramp-height-grav-to-elastic` | Medium, Hard |
| Force of Friction (gravitational to elastic) | `grav-to-elastic-friction-distance-q.force-of-friction-grav-to-elastic` | Medium, Hard |
| Thermal Energy and Height (elastic to gravitational) | `elastic-to-grav-friction-distance-q.thermal-energy-and-height-elastic-to-grav` | Easy |
| Thermal Energy and Spring Compression (elastic to gravitational) | `elastic-to-grav-friction-distance-q.thermal-energy-and-spring-compression-elastic-to-grav` | Easy |
| Thermal Energy and Spring Constant (elastic to gravitational) | `elastic-to-grav-friction-distance-q.thermal-energy-and-spring-constant-elastic-to-grav` | Easy |
| Thermal Energy and Mass (elastic to gravitational) | `elastic-to-grav-friction-distance-q.thermal-energy-and-mass-elastic-to-grav` | Easy |
| Height (elastic to gravitational) | `elastic-to-grav-friction-distance-q.height-elastic-to-grav` | Medium, Hard |
| Spring Compression (elastic to gravitational) | `elastic-to-grav-friction-distance-q.spring-compression-elastic-to-grav` | Medium, Hard |
| Mass (elastic to gravitational) | `elastic-to-grav-friction-distance-q.mass-elastic-to-grav` | Medium, Hard |
| Ramp Length (elastic to gravitational) | `elastic-to-grav-friction-distance-q.ramp-length-elastic-to-grav` | Medium, Hard |
| Spring Constant (elastic to gravitational) | `elastic-to-grav-friction-distance-q.spring-constant-elastic-to-grav` | Medium, Hard |
| Force of Friction (elastic to gravitational) | `elastic-to-grav-friction-distance-q.force-of-friction-elastic-to-grav` | Medium, Hard |

### Elastic <--> Kinetic

| Target | ID | Levels |
|---|---|---|
| Thermal Energy and Spring Compression (kinetic to elastic) | `kinetic-to-elastic-friction-distance-q.thermal-energy-and-spring-compression-kinetic-to-elastic` | Easy |
| Thermal Energy and Spring Constant (kinetic to elastic) | `kinetic-to-elastic-friction-distance-q.thermal-energy-and-spring-constant-kinetic-to-elastic` | Easy |
| Thermal Energy and Initial Velocity (kinetic to elastic) | `kinetic-to-elastic-friction-distance-q.thermal-energy-and-initial-velocity-kinetic-to-elastic` | Easy |
| Thermal Energy and Mass (kinetic to elastic) | `kinetic-to-elastic-friction-distance-q.thermal-energy-and-mass-kinetic-to-elastic` | Easy |
| Spring Compression (kinetic to elastic) | `kinetic-to-elastic-friction-distance-q.spring-compression-kinetic-to-elastic` | Medium, Hard |
| Spring Constant (kinetic to elastic) | `kinetic-to-elastic-friction-distance-q.spring-constant-kinetic-to-elastic` | Medium, Hard |
| Mass (kinetic to elastic) | `kinetic-to-elastic-friction-distance-q.mass-kinetic-to-elastic` | Medium, Hard |
| Distance (kinetic to elastic) | `kinetic-to-elastic-friction-distance-q.distance-kinetic-to-elastic` | Medium, Hard |
| Initial Velocity (kinetic to elastic) | `kinetic-to-elastic-friction-distance-q.initial-velocity-kinetic-to-elastic` | Medium, Hard |
| Force of Friction (kinetic to elastic) | `kinetic-to-elastic-friction-distance-q.force-of-friction-kinetic-to-elastic` | Medium, Hard |
| Thermal Energy and Velocity (elastic to kinetic) | `elastic-to-kinetic-friction-distance-q.thermal-energy-and-velocity-elastic-to-kinetic` | Easy |
| Thermal Energy and Spring Compression (elastic to kinetic) | `elastic-to-kinetic-friction-distance-q.thermal-energy-and-spring-compression-elastic-to-kinetic` | Easy |
| Thermal Energy and Spring Constant (elastic to kinetic) | `elastic-to-kinetic-friction-distance-q.thermal-energy-and-spring-constant-elastic-to-kinetic` | Easy |
| Thermal Energy and Mass (elastic to kinetic) | `elastic-to-kinetic-friction-distance-q.thermal-energy-and-mass-elastic-to-kinetic` | Easy |
| Velocity (elastic to kinetic) | `elastic-to-kinetic-friction-distance-q.velocity-elastic-to-kinetic` | Medium, Hard |
| Spring Compression (elastic to kinetic) | `elastic-to-kinetic-friction-distance-q.spring-compression-elastic-to-kinetic` | Medium, Hard |
| Mass (elastic to kinetic) | `elastic-to-kinetic-friction-distance-q.mass-elastic-to-kinetic` | Medium, Hard |
| Distance (elastic to kinetic) | `elastic-to-kinetic-friction-distance-q.distance-elastic-to-kinetic` | Medium, Hard |
| Spring Constant (elastic to kinetic) | `elastic-to-kinetic-friction-distance-q.spring-constant-elastic-to-kinetic` | Medium, Hard |
| Force of Friction (elastic to kinetic) | `elastic-to-kinetic-friction-distance-q.force-of-friction-elastic-to-kinetic` | Medium, Hard |

## WaveGenerator

### Wave Properties

| Target | ID | Levels |
|---|---|---|
| Wave Speed | `properties-of-waves.wave-speed` | Easy, Medium, Hard |
| Wavelength | `properties-of-waves.wavelength` | Easy, Medium, Hard |
| Frequency | `properties-of-waves.frequency` | Easy, Medium, Hard |

### String Harmonics

| Target | ID | Levels |
|---|---|---|
| Wavelength | `string-harmonics.wavelength` | Easy |
| Fundamental Frequency | `string-harmonics.fundamental-frequency` | Easy |
| String Length | `string-harmonics.string-length` | Easy |
| First Harmonic Wavelength and Second Harmonic Wavelength and Third Harmonic Wavelength | `string-harmonics.first-harmonic-wavelength-and-second-harmonic-wavelength-and-third-harmonic-wavelength` | Medium |
| Fundamental Frequency and Second Harmonic Frequency and Third Harmonic Frequency | `string-harmonics.fundamental-frequency-and-second-harmonic-frequency-and-third-harmonic-frequency` | Medium |
| Wavelength and String Length | `string-harmonics.wavelength-and-string-length` | Hard |
| Fundamental Frequency and String Length | `string-harmonics.fundamental-frequency-and-string-length` | Hard |

### Open Ended Column Harmonics

| Target | ID | Levels |
|---|---|---|
| Wavelength | `open-column-harmonics.wavelength` | Easy |
| Fundamental Frequency | `open-column-harmonics.fundamental-frequency` | Easy |
| Column Length | `open-column-harmonics.column-length` | Easy |
| First Harmonic Wavelength and Second Harmonic Wavelength and Third Harmonic Wavelength | `open-column-harmonics.first-harmonic-wavelength-and-second-harmonic-wavelength-and-third-harmonic-wavelength` | Medium |
| Fundamental Frequency and Second Harmonic Frequency and Third Harmonic Frequency | `open-column-harmonics.fundamental-frequency-and-second-harmonic-frequency-and-third-harmonic-frequency` | Medium |
| Wavelength and Column Length | `open-column-harmonics.wavelength-and-column-length` | Hard |
| Fundamental Frequency and Column Length | `open-column-harmonics.fundamental-frequency-and-column-length` | Hard |

### Closed End Column Harmonics

| Target | ID | Levels |
|---|---|---|
| Wavelength | `closed-column-harmonics.wavelength` | Easy |
| Fundamental Frequency | `closed-column-harmonics.fundamental-frequency` | Easy |
| Column Length | `closed-column-harmonics.column-length` | Easy |
| First Harmonic Wavelength and Third Harmonic Wavelength and Fifth Harmonic Wavelength | `closed-column-harmonics.first-harmonic-wavelength-and-third-harmonic-wavelength-and-fifth-harmonic-wavelength` | Medium |
| Fundamental Frequency and Third Harmonic Frequency and Fifth Harmonic Frequency | `closed-column-harmonics.fundamental-frequency-and-third-harmonic-frequency-and-fifth-harmonic-frequency` | Medium |
| Wavelength and Column Length | `closed-column-harmonics.wavelength-and-column-length` | Hard |
| Fundamental Frequency and Column Length | `closed-column-harmonics.fundamental-frequency-and-column-length` | Hard |

## ForceGenerator

### Newton's Second Law

| Target | ID | Levels |
|---|---|---|
| Object acceleration | `generate-force-question.object-acceleration` | Easy |
| Net Force on Object | `generate-force-question.net-force-on-object` | Easy |
| Object mass | `generate-force-question.object-mass` | Easy |
| Net Force and coefficient of friction | `generate-force-question.net-force-and-coefficient-of-friction` | Medium, Hard |
| Net Force and acceleration | `generate-force-question.net-force-and-acceleration` | Medium, Hard |
| Net Force and Applied Force | `generate-force-question.net-force-and-applied-force` | Medium, Hard |

## RelativeMotionGenerator

### Independent motion

| Target | ID | Levels |
|---|---|---|
| Relative velocity | `selected-question.relative-velocity` | Easy |
| Object A velocity relative to ground | `selected-question.object-a-velocity-relative-to-ground` | Easy, Medium, Hard |
| Object B velocity relative to ground | `selected-question.object-b-velocity-relative-to-ground` | Easy, Medium, Hard |
| Separation after stated time | `selected-question.separation-after-stated-time` | Medium |
| Meeting time | `selected-question.meeting-time` | Hard |

### Nested reference frames

| Target | ID | Levels |
|---|---|---|
| Person velocity relative to shore | `selected-question.person-velocity-relative-to-shore` | Easy, Medium, Hard |
| Person velocity relative to boat | `selected-question.person-velocity-relative-to-boat` | Easy, Medium |
| boat velocity relative to shore | `selected-question.boat-velocity-relative-to-shore` | Easy |
| boat velocity relative to water | `selected-question.boat-velocity-relative-to-water` | Medium, Hard |
| water velocity relative to shore | `selected-question.water-velocity-relative-to-shore` | Medium, Hard |
| Person velocity relative to moving walkway | `selected-question.person-velocity-relative-to-moving-walkway` | Hard |
| moving walkway velocity relative to boat | `selected-question.moving-walkway-velocity-relative-to-boat` | Hard |

### Combined

| Target | ID | Levels |
|---|---|---|
| Person A velocity relative to Person B | `selected-question.person-a-velocity-relative-to-person-b` | Easy, Medium, Hard |
| Person A velocity relative to boat A | `selected-question.person-a-velocity-relative-to-boat-a` | Easy, Medium |
| boat A velocity relative to shore | `selected-question.boat-a-velocity-relative-to-shore` | Easy |
| Person B velocity relative to boat B | `selected-question.person-b-velocity-relative-to-boat-b` | Easy, Medium |
| boat B velocity relative to shore | `selected-question.boat-b-velocity-relative-to-shore` | Easy |
| boat A velocity relative to water | `selected-question.boat-a-velocity-relative-to-water` | Medium, Hard |
| boat B velocity relative to water | `selected-question.boat-b-velocity-relative-to-water` | Medium, Hard |
| Person A velocity relative to walkway A | `selected-question.person-a-velocity-relative-to-walkway-a` | Hard |
| walkway A velocity relative to boat A | `selected-question.walkway-a-velocity-relative-to-boat-a` | Hard |
| Person B velocity relative to walkway B | `selected-question.person-b-velocity-relative-to-walkway-b` | Hard |
| walkway B velocity relative to boat B | `selected-question.walkway-b-velocity-relative-to-boat-b` | Hard |

## OhmsLawTargets

### Single Resistor

| Target | ID | Levels |
|---|---|---|
| Voltage | `voltage` | Easy, Medium, Hard |
| Current | `current` | Easy, Medium, Hard |
| Resistance | `resistance` | Easy, Medium, Hard |

## StoichiometryTargets

### Product amount

| Target | ID | Levels |
|---|---|---|
| Product moles (given reactant mass) | `gram-to-mole` | Medium |
| Product mass (given reactant moles) | `mole-to-gram` | Medium |

