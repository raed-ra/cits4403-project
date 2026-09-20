"""
CITS4403 Computational Modelling Project
Complex Contagion on Watts-Strogatz Small-World Networks

Author: Raed
Baseline: Centola & Macy (2007), "Complex Contagions and the Weakness of Long Ties"

This reproduces the core result: as the rewiring probability p increases
(clustered ring lattice -> random graph), a COMPLEX contagion (threshold > 1
neighbour needed) spreads LESS well, because long-range shortcuts destroy the
local reinforcement that complex contagions rely on. A SIMPLE contagion
(threshold = 1) behaves the opposite way.
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt


# ----------------------------------------------------------------------
# 1. THE CONTAGION MODEL
# ----------------------------------------------------------------------

def run_contagion(G, theta, seed_nodes, max_steps=1000):
    """
    Run a threshold contagion to steady state on graph G.

    G          : the network (nodes are people, edges are social ties)
    theta      : threshold — a node adopts once the FRACTION of its
                 neighbours who have adopted is >= theta
    seed_nodes : the initially-adopted nodes (a starting cluster)
    returns    : the fraction of the whole network that ends up adopted
    """
    # state[node] = True if adopted, False otherwise
    adopted = {node: False for node in G.nodes()}
    for s in seed_nodes:
        adopted[s] = True

    # Keep updating everyone until a full pass changes nobody (steady state)
    for step in range(max_steps):
        newly_adopted = []
        for node in G.nodes():
            if adopted[node]:
                continue  # already adopted, skip
            neighbours = list(G.neighbors(node))
            if len(neighbours) == 0:
                continue
            # fraction of this node's neighbours who have adopted
            frac_active = sum(adopted[n] for n in neighbours) / len(neighbours)
            if frac_active >= theta:
                newly_adopted.append(node)

        if not newly_adopted:
            break  # nothing changed this pass -> steady state reached
        for node in newly_adopted:
            adopted[node] = True

    # final cascade size = fraction of network that adopted
    return sum(adopted.values()) / G.number_of_nodes()


def seed_cluster(G, size):
    """Pick a small CONNECTED starting cluster: a node and its neighbours.
    Complex contagions need a local cluster to get going, not scattered seeds."""
    start = list(G.nodes())[0]
    cluster = {start}
    for n in G.neighbors(start):
        cluster.add(n)
        if len(cluster) >= size:
            break
    return list(cluster)


# ----------------------------------------------------------------------
# 2. THE CORE EXPERIMENT: sweep p, fix theta
# ----------------------------------------------------------------------

def sweep_rewiring(n, k, theta, p_values, n_trials, seed_size):
    """
    For each rewiring probability p, build several WS graphs and run the
    contagion on each, then average the final cascade size.

    Returns two arrays: mean cascade size, and standard deviation (error bars).
    """
    means = []
    stds = []
    for p in p_values:
        results = []
        for trial in range(n_trials):
            G = nx.watts_strogatz_graph(n, k, p)
            seeds = seed_cluster(G, seed_size)
            final = run_contagion(G, theta, seeds)
            results.append(final)
        means.append(np.mean(results))
        stds.append(np.std(results))
        print(f"  p={p:.4f}  ->  mean cascade size = {np.mean(results):.3f}")
    return np.array(means), np.array(stds)


# ----------------------------------------------------------------------
# 3. RUN IT
# ----------------------------------------------------------------------

if __name__ == "__main__":
    # --- parameters (stated assumptions) ---
    n = 500          # number of nodes (people)
    k = 10           # each node connected to k nearest neighbours
    seed_size = 12   # size of the initial adopted cluster
    n_trials = 20    # repeats per p value (for averaging + error bars)

    # rewiring probabilities, log-spaced from very clustered to random
    p_values = np.logspace(-4, 0, 12)   # 0.0001 ... 1.0

    print("=" * 55)
    print("COMPLEX contagion (theta = 0.30, needs ~3 of 10 neighbours)")
    print("=" * 55)
    complex_means, complex_stds = sweep_rewiring(
        n, k, theta=0.30, p_values=p_values,
        n_trials=n_trials, seed_size=seed_size)

    print()
    print("=" * 55)
    print("SIMPLE contagion (theta = 0.10, needs just 1 of 10 neighbours)")
    print("=" * 55)
    simple_means, simple_stds = sweep_rewiring(
        n, k, theta=0.10, p_values=p_values,
        n_trials=n_trials, seed_size=seed_size)

    # --- plot ---
    fig, ax = plt.subplots(figsize=(8, 5.5))

    ax.errorbar(p_values, complex_means, yerr=complex_stds,
                marker='o', capsize=3, label='Complex contagion (θ=0.30)',
                color='#c1272d')
    ax.errorbar(p_values, simple_means, yerr=simple_stds,
                marker='s', capsize=3, label='Simple contagion (θ=0.10)',
                color='#0072b2')

    ax.set_xscale('log')
    ax.set_xlabel('Rewiring probability  p   (clustered ring  →  random)')
    ax.set_ylabel('Final cascade size (fraction adopted)')
    ax.set_title('Complex vs Simple Contagion on Watts–Strogatz Networks\n'
                 'Baseline: Centola & Macy (2007)')
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig('/home/claude/contagion_result.png', dpi=130)
    print("\nSaved plot to contagion_result.png")
