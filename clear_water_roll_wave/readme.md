# The script for clear-water roll wave simulation.

Modifications:
* Time-dependent Dirichlet west BC.
* Due to simple topo, channel slope term is incorporated in the `semi-implicit term` (or in the `nonhyperbolic` term).
* Problem-specific parameters input: `distPeriod`, `distAmp`, `channelSlope`.
* New type of BC: 10 for TDBC, new type for rheology: 10 for clear-water roll waves.
