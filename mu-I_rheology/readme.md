# The script for mu-I rheology model simulation.
*Backward compatible the clear water roll wave rheology*
mu-I rheology model proposed by Gray & Edwards (2014)

Modifications:
* Input entries for mu, mu1, mu2, L, beta
* mu bed-friction function implemented in `eval_nonhyperbolic_terms`--rheology type 11.
* Central difference for viscosity term's space discretization and RK2-TVD scheme for viscosity term's time integration.

**Possible problems**
```diff
-Error: Line truncation...
```
Solution: use `&` to truncation excessively long lines.
