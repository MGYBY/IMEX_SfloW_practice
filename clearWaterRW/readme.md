# The script for clear-water roll wave simulation.

Modifications:
* Time-dependent Dirichlet west BC.
* Due to simple topo, channel slope term is incorporated in the `semi-implicit term` (or in the `nonhyperbolic` term).
* Problem-specific parameters input: `distPeriod`, `distAmp`, `channelSlope`.
* New type of BC: 10 for TDBC, new type for rheology: 10 for clear-water roll waves.

Note that the orginal notation is kept for type-10 rheology.

**Compilation problem**
```diff
-: variable `t` is needed before the compilation of `IMEX_Sflow_2d.f90`
```
*Solution: move variable `t` to `parameters_2d.f90`*
