"""
1D Adjoint Method Diagram Generator
====================================

This script generates an educational diagram illustrating the 1D diffusion problem
used in the discrete adjoint method example.

Generated diagrams:
1. adjoint_1d_discretization.png
   - Shows the 1D domain discretized into 11 nodes
   - Displays boundary conditions (T0=0, T10=1)
   - Shows example interior node with stencil
   - Illustrates parameter α at each node

Usage:
    python3 create_adjoint_diagram.py

Requirements:
    - matplotlib
    - numpy
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, FancyArrowPatch
import numpy as np

# ============================================
# Diagram: 1D Finite-Difference Discretization
# ============================================
fig, ax = plt.subplots(1, 1, figsize=(14, 6))

# Domain parameters
nx = 11  # 11 nodes
L = 1.0
dx = L / (nx - 1)

# Node positions
node_positions = np.linspace(0, L, nx)
y_base = 0.5

# Draw domain as a thick line
ax.plot([0, L], [y_base, y_base], 'k-', linewidth=4)

# Draw all nodes
for i, x in enumerate(node_positions):
    ax.plot(x, y_base, 'bo', markersize=12)
    ax.text(x, y_base - 0.12, f'$x_{i}$', fontsize=13, ha='center', weight='bold')
    ax.text(x, y_base + 0.15, f'$T_{i}$', fontsize=12, ha='center', weight='bold', color='darkblue')

# Highlight boundary nodes
ax.plot(node_positions[0], y_base, 'go', markersize=16, markerfacecolor='lightgreen', markeredgewidth=2)
ax.text(node_positions[0], y_base - 0.28, 'BC: $T_0=0$', fontsize=11, ha='center', weight='bold', color='green')

ax.plot(node_positions[-1], y_base, 'go', markersize=16, markerfacecolor='lightgreen', markeredgewidth=2)
ax.text(node_positions[-1], y_base - 0.28, 'BC: $T_{10}=1$', fontsize=11, ha='center', weight='bold', color='green')

# Highlight one stencil (node i=5)
stencil_idx = 5
x_left = node_positions[stencil_idx - 1]
x_center = node_positions[stencil_idx]
x_right = node_positions[stencil_idx + 1]

# Draw arrows showing stencil
ax.annotate('', xy=(x_left, y_base - 0.4), xytext=(x_left, y_base - 0.32),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='red'))
ax.annotate('', xy=(x_center, y_base + 0.32), xytext=(x_center, y_base + 0.24),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='red'))
ax.annotate('', xy=(x_right, y_base - 0.4), xytext=(x_right, y_base - 0.32),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='red'))

# Label stencil
ax.text(x_left, y_base - 0.5, f'$T_{stencil_idx-1}$', fontsize=11, ha='center', weight='bold', color='red')
ax.text(x_center, y_base + 0.42, f'Center: $T_{stencil_idx}$', fontsize=11, ha='center', weight='bold', color='red')
ax.text(x_right, y_base - 0.5, f'$T_{stencil_idx+1}$', fontsize=11, ha='center', weight='bold', color='red')

# Draw stencil connection line
ax.plot([x_left, x_right], [y_base - 0.42, y_base - 0.42], 'r--', linewidth=2, alpha=0.5)
ax.text(x_center, y_base - 0.55, '3-point stencil', fontsize=11, ha='center', weight='bold', color='red',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

# Show spacing
spacing_y = 0.1
ax.annotate('', xy=(x_center + dx/2, spacing_y), xytext=(x_center - dx/2, spacing_y),
            arrowprops=dict(arrowstyle='<->', lw=2, color='purple'))
ax.text(x_center, spacing_y - 0.06, r'$\Delta x = 0.1$', fontsize=12, ha='center', weight='bold', color='purple')

# Add legend
ax.text(0.02, 0.65, '● = Node point where $T_i$ is defined', fontsize=11, ha='left', weight='bold')

ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.7, 0.8)
ax.set_aspect('equal')
ax.axis('off')

ax.set_title('1D Domain: 11 Nodes with Finite-Difference Discretization',
             fontsize=15, weight='bold', pad=20)

plt.tight_layout()
plt.savefig('adjoint_1d_discretization.png', dpi=300, bbox_inches='tight')
print("Saved: adjoint_1d_discretization.png")
plt.close()

# ============================================
# Diagram 2: Adjoint Method Workflow
# ============================================
fig, ax = plt.subplots(1, 1, figsize=(14, 10))

# Define box positions and sizes
box_width = 2.2
box_height = 0.8
y_start = 4.5
spacing = 1.0

# Step 1: Solve forward problem
y1 = y_start
box1 = FancyBboxPatch((0.5, y1), box_width, box_height, boxstyle="round,pad=0.1",
                       edgecolor='blue', facecolor='lightblue', linewidth=2)
ax.add_patch(box1)
ax.text(1.6, y1 + 0.4, '① Forward Solve', fontsize=14, ha='center', weight='bold')
ax.text(1.6, y1 + 0.05, r'Solve: $\mathbf{R}(\mathbf{T}, \boldsymbol{\alpha}) = 0$', fontsize=11, ha='center')

# Arrow down
ax.annotate('', xy=(1.6, y1 - 0.15), xytext=(1.6, y1 - 0.05),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))

# Step 2: Compute Jacobians
y2 = y1 - spacing - 0.3
box2 = FancyBboxPatch((0.5, y2), box_width, box_height, boxstyle="round,pad=0.1",
                       edgecolor='blue', facecolor='lightblue', linewidth=2)
ax.add_patch(box2)
ax.text(1.6, y2 + 0.4, '② Compute Jacobians', fontsize=14, ha='center', weight='bold')
ax.text(1.6, y2 + 0.05, r'Build: $\frac{\partial \mathbf{R}}{\partial \mathbf{T}}$, $\frac{\partial \mathbf{R}}{\partial \boldsymbol{\alpha}}$', fontsize=11, ha='center')

# Arrow down
ax.annotate('', xy=(1.6, y2 - 0.15), xytext=(1.6, y2 - 0.05),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))

# Step 3: Solve adjoint system
y3 = y2 - spacing - 0.3
box3 = FancyBboxPatch((0.5, y3), box_width, box_height, boxstyle="round,pad=0.1",
                       edgecolor='green', facecolor='lightgreen', linewidth=2)
ax.add_patch(box3)
ax.text(1.6, y3 + 0.4, '③ Adjoint Solve', fontsize=14, ha='center', weight='bold')
ax.text(1.6, y3 + 0.05, r'Solve: $\mathbf{J}^T \boldsymbol{\psi} = \frac{\partial F}{\partial \mathbf{T}}^T$', fontsize=11, ha='center')

# Arrow down
ax.annotate('', xy=(1.6, y3 - 0.15), xytext=(1.6, y3 - 0.05),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))

# Step 4: Compute sensitivities
y4 = y3 - spacing - 0.3
box4 = FancyBboxPatch((0.5, y4), box_width, box_height, boxstyle="round,pad=0.1",
                       edgecolor='green', facecolor='lightgreen', linewidth=2)
ax.add_patch(box4)
ax.text(1.6, y4 + 0.4, '④ Sensitivities', fontsize=14, ha='center', weight='bold')
ax.text(1.6, y4 + 0.05, r'Compute: $\frac{dF}{d\alpha_i} = T_i^2 \cdot \psi_i$', fontsize=11, ha='center')

# Arrow down
ax.annotate('', xy=(1.6, y4 - 0.15), xytext=(1.6, y4 - 0.05),
            arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))

# Step 5: Verification
y5 = y4 - spacing - 0.3
box5 = FancyBboxPatch((0.5, y5), box_width, box_height, boxstyle="round,pad=0.1",
                       edgecolor='red', facecolor='lightyellow', linewidth=2)
ax.add_patch(box5)
ax.text(1.6, y5 + 0.4, '⑤ Verify (Optional)', fontsize=14, ha='center', weight='bold')
ax.text(1.6, y5 + 0.05, r'Check: Finite-diff vs Adjoint', fontsize=11, ha='center')

# Add cost comparison on the right
cost_y = y1 - 0.5
ax.text(3.5, cost_y + 1.5, 'Computational Cost', fontsize=14, ha='center', weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

cost_info = (
    'Forward: Solves once\n'
    'Adjoint: Solves once\n'
    'Total: 2 solves (independent of #parameters)\n\n'
    'vs. Finite-Difference:\n'
    f'Cost: {nx-1} forward solves (one per interior node)\n'
    'Scales with # of design variables'
)
ax.text(3.5, cost_y - 1.0, cost_info, fontsize=11, ha='center', family='monospace',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

ax.set_xlim(0, 5)
ax.set_ylim(-1.5, 5.5)
ax.axis('off')

ax.set_title('Adjoint Method Workflow: Five Steps',
             fontsize=16, weight='bold', pad=20)

plt.tight_layout()
plt.savefig('adjoint_method_workflow.png', dpi=300, bbox_inches='tight')
print("Saved: adjoint_method_workflow.png")
plt.close()

print("\nAll adjoint diagrams generated successfully!")
