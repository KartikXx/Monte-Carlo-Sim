import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

#Core Simulation
# ─────────────────────────────────────────────
# This is the heart of the project.
# We generate N random (x, y) points in the range [-1, 1].
# A point is "inside" the unit circle if x² + y² <= 1.
# π ≈ 4 * (inside / total)

def estimate_pi(n_samples):
    """
    Run one Monte Carlo simulation with n_samples points.
    Returns: pi_estimate, x coords, y coords, inside mask
    """
    x = np.random.uniform(-1, 1, n_samples)  # random x in [-1, 1]
    y = np.random.uniform(-1, 1, n_samples)  # random y in [-1, 1]

    inside = (x**2 + y**2) <= 1.0

    pi_estimate = 4 * np.sum(inside) / n_samples
    return pi_estimate, x, y, inside


# Convergence Analysis
# ─────────────────────────────────────────────
# We run the simulation at increasing sample sizes: 10³ to 10⁶
# At each size we record the π estimate.
# This shows HOW FAST the estimate converges to true π.
# This is the "statistical relationship between sample size
# and approximation accuracy" from your resume bullet.

sample_sizes = np.logspace(3, 6, 50).astype(int)  # 50 points from 1000 to 1,000,000
pi_estimates = []
errors = []

print("Running convergence analysis...")
for n in sample_sizes:
    est, _, _, _ = estimate_pi(n)
    pi_estimates.append(est)
    errors.append(abs(est - np.pi))  # absolute error vs true π
    print(f"  n={n:>8,}  →  π ≈ {est:.6f}  |  error = {abs(est - np.pi):.6f}")

print(f"\nTrue π = {np.pi:.6f}")
print(f"Best estimate (n=1,000,000): {pi_estimates[-1]:.6f}")
print(f"Final error: {errors[-1]:.6f}")


# Visualizations
# ─────────────────────────────────────────────
# We build 3 plots:
#   Plot 1 — The sampling scatter (the classic visual)
#   Plot 2 — Convergence of π estimate as n increases
#   Plot 3 — Estimation error vs sample size (log scale)

fig = plt.figure(figsize=(16, 5))
fig.suptitle("Monte Carlo Estimation of π", fontsize=15, fontweight='bold', y=1.01)
gs = gridspec.GridSpec(1, 3, figure=fig, wspace=0.35)


# ── Plot 1: Sampling Scatter ──────────────────
# Show 5000 random points — green inside the circle, red outside.
# The ratio of green to total visually demonstrates WHY this works.

ax1 = fig.add_subplot(gs[0])

n_visual = 5000
est_visual, x_vis, y_vis, inside_vis = estimate_pi(n_visual)

ax1.scatter(x_vis[inside_vis],  y_vis[inside_vis],  color='#2ecc71', s=0.8, alpha=0.6, label='Inside')
ax1.scatter(x_vis[~inside_vis], y_vis[~inside_vis], color='#e74c3c', s=0.8, alpha=0.6, label='Outside')

# Draw the unit circle on top
theta = np.linspace(0, 2 * np.pi, 300)
ax1.plot(np.cos(theta), np.sin(theta), 'black', linewidth=1.2)
ax1.set_aspect('equal')
ax1.set_title(f"Random Sampling (n=5,000)\nπ ≈ {est_visual:.4f}", fontsize=10)
ax1.set_xlabel("x")
ax1.set_ylabel("y")
ax1.legend(loc='upper right', markerscale=6, fontsize=8)
ax1.set_xlim(-1.1, 1.1)
ax1.set_ylim(-1.1, 1.1)


# ── Plot 2: Convergence of π Estimate ────────
# As n grows, the estimate gets closer to true π.
# The red dashed line is true π — we're watching our estimate home in on it.

ax2 = fig.add_subplot(gs[1])

ax2.semilogx(sample_sizes, pi_estimates, color='#3498db', linewidth=1.5, label='π estimate')
ax2.axhline(y=np.pi, color='#e74c3c', linestyle='--', linewidth=1.2, label=f'True π = {np.pi:.4f}')
ax2.fill_between(sample_sizes,
                 [np.pi - 0.05] * len(sample_sizes),
                 [np.pi + 0.05] * len(sample_sizes),
                 alpha=0.1, color='red', label='±0.05 band')

ax2.set_title("Convergence of π Estimate", fontsize=10)
ax2.set_xlabel("Sample Size (log scale)")
ax2.set_ylabel("Estimated π")
ax2.legend(fontsize=8)
ax2.grid(True, alpha=0.3)


# ── Plot 3: Estimation Error (Log-Log) ───────
# This is the most technically interesting plot.
# On a log-log scale, Monte Carlo error follows a straight line
# with slope -0.5 — meaning error ∝ 1/√n

ax3 = fig.add_subplot(gs[2])

ax3.loglog(sample_sizes, errors, color='#9b59b6', linewidth=1.5, label='Absolute Error')

# Overlay the theoretical O(1/√n) line for comparison
theoretical = 1 / np.sqrt(sample_sizes)
ax3.loglog(sample_sizes, theoretical, 'k--', linewidth=1, alpha=0.6, label='O(1/√n) theoretical')

ax3.set_title("Estimation Error vs Sample Size\n(Log-Log Scale)", fontsize=10)
ax3.set_xlabel("Sample Size (log scale)")
ax3.set_ylabel("Absolute Error |π_est − π|")
ax3.legend(fontsize=8)
ax3.grid(True, alpha=0.3, which='both')


plt.tight_layout()
plt.savefig("monte_carlo_results.png", dpi=150, bbox_inches='tight')
plt.show()
print("\nPlot saved as monte_carlo_results.png")