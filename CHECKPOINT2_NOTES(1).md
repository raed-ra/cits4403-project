# Checkpoint 2 — what to show and say

## What I have working
A Python model of **complex contagion on Watts–Strogatz networks**, reproducing
the baseline result from Centola & Macy (2007).

- `complex_contagion.py` — the model + core experiment (runs in ~1 min)
- `contagion_result.png` — the result plot

Run it live if asked:  `python complex_contagion.py`

## What the model does (say this)
- Build a Watts–Strogatz graph `G(n, k, p)` — the small-world model from Lecture 3.
- Each node is adopted or not. Seed a small connected cluster as adopted.
- **Threshold rule:** a node adopts once the *fraction* of its neighbours that
  have adopted is ≥ θ. Small θ = simple contagion (1 neighbour enough);
  larger θ = complex contagion (needs several neighbours = social reinforcement).
- Update everyone repeatedly until nobody changes (steady state).
- Measure final cascade size = fraction of the network that adopted.

## The core experiment
Fix θ, sweep the rewiring probability p from 0.0001 (clustered ring) to 1 (random),
20 trials per point, plot mean cascade size with error bars.

## The result (the headline)
- **Complex contagion (θ=0.30):** spreads to the whole network while clustered,
  then COLLAPSES as p rises and shortcuts replace clustering.
- **Simple contagion (θ=0.10):** spreads fully at every p — shortcuts don't hurt it.
- This reproduces Centola & Macy: **long ties impede complex contagion.**
  Clustering provides the local reinforcement complex contagions need; random
  shortcuts destroy it.

## Why this fits the unit
Uses the Watts–Strogatz generator and small-world ideas straight from Lecture 3;
the collapse is a sharp transition (a complex-systems signature, like the
connectivity S-curve in the lectures).

## Where it's going (my extension — say this when asked "what next")
The baseline is deterministic and uses one threshold for everyone. My extension:
1. **Noisy thresholds** — nodes sometimes adopt below θ / resist above it.
   Recent work suggests noise can REVERSE the 2007 result — I'll test where.
2. **Heterogeneous thresholds** — different nodes have different θ.
Plan to map cascade size over a 2D phase diagram (p × noise) to locate where
clustering stops being an advantage. Stretch: repeat on a Barabási–Albert
(scale-free) network to test the role of hubs.

## Honest limitations (good to volunteer)
- Stylised threshold rule, synthetic networks.
- Only reproduced the baseline so far; extensions are next.
- Plan to validate on real network data (SNAP Facebook from Lecture 3).
