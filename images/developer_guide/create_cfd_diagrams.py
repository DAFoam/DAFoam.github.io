"""
CFD Diagram Generator for 2D Lid-Driven Cavity Example
======================================================

This script generates three educational diagrams illustrating fundamental CFD
concepts:

1. cfd_mesh_structure.png
   - Shows the structured quad mesh with cell centers and faces
   - Highlights boundary conditions on all domain edges
   - Red box highlights one example cell with labeled faces

2. cfd_single_cell_flux.png
   - Shows a single cell (P) and its four neighboring cells (E, W, N, S)
   - Displays face flux equations: phi_f = u_f * n_f * A_f
   - Illustrates conservation principle: sum of fluxes balances

3. cfd_velocity_field.png
   - Displays the converged velocity field solution
   - Shows velocity vectors and magnitude color map
   - Demonstrates counter-clockwise circulation pattern

Usage:
    python3 create_cfd_diagrams.py

Requirements:
    - matplotlib
    - numpy
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

# Set style for better looking diagrams
plt.style.use('seaborn-v0_8-darkgrid')

# ============================================
# Diagram 1: Mesh Structure with Cell Centers and Faces
# ============================================
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

nx, ny = 4, 4
dx = 1.0 / nx
dy = 1.0 / ny

# Draw grid cells
for i in range(nx):
    for j in range(ny):
        x = i * dx
        y = j * dy
        rect = Rectangle((x, y), dx, dy, linewidth=2, edgecolor='black', facecolor='lightblue', alpha=0.3)
        ax.add_patch(rect)
        
        # Draw cell center (●)
        cx = x + dx / 2
        cy = y + dy / 2
        ax.plot(cx, cy, 'ro', markersize=10, label='Cell center' if i == 0 and j == 0 else '')

# Highlight one cell and its faces
highlight_i, highlight_j = 1, 2
x = highlight_i * dx
y = highlight_j * dy
highlight_rect = Rectangle((x, y), dx, dy, linewidth=4, edgecolor='red', facecolor='none')
ax.add_patch(highlight_rect)

# Draw faces of highlighted cell with arrows
cx = x + dx / 2
cy = y + dy / 2

# Face arrows
arrow_props = dict(arrowstyle='->', lw=3, color='darkred')
# East face
ax.annotate('', xy=(x + dx, cy), xytext=(x + dx - 0.05, cy), arrowprops=arrow_props)
ax.text(x + dx + 0.03, cy, 'East\nface', fontsize=14, color='darkred', weight='bold')

# West face
ax.annotate('', xy=(x, cy), xytext=(x + 0.05, cy), arrowprops={**arrow_props, 'arrowstyle': '<-'})
ax.text(x - 0.08, cy, 'West\nface', fontsize=14, color='darkred', weight='bold', ha='right')

# North face
ax.annotate('', xy=(cx, y + dy), xytext=(cx, y + dy - 0.05), arrowprops=arrow_props)
ax.text(cx, y + dy + 0.03, 'North\nface', fontsize=14, color='darkred', weight='bold', ha='center')

# South face
ax.annotate('', xy=(cx, y), xytext=(cx, y + 0.05), arrowprops={**arrow_props, 'arrowstyle': '<-'})
ax.text(cx, y - 0.08, 'South\nface', fontsize=14, color='darkred', weight='bold', ha='center', va='top')

# Boundary condition annotations
ax.text(0.5, 1.05, 'Top: u=1, v=0 (moving lid)', fontsize=14, weight='bold', ha='center', 
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
ax.text(-0.12, 0.5, 'Left:\nu=0, v=0', fontsize=14, weight='bold', ha='right',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.7))
ax.text(1.12, 0.5, 'Right:\nu=0, v=0', fontsize=14, weight='bold', ha='left',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.7))
ax.text(0.5, -0.08, 'Bottom: u=0, v=0 (stationary)', fontsize=14, weight='bold', ha='center',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.7))

ax.set_xlim(-0.25, 1.25)
ax.set_ylim(-0.2, 1.2)
ax.set_aspect('equal')
ax.set_xlabel('x', fontsize=14, weight='bold')
ax.set_ylabel('y', fontsize=14, weight='bold')
ax.grid(False)

# Add legend
red_dot = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='r', markersize=10, label='Cell center (stores u, v, p)')
ax.legend(handles=[red_dot], loc='upper right', fontsize=14)

plt.tight_layout()
plt.savefig('cfd_mesh_structure.png', dpi=300, bbox_inches='tight')
print("Saved: cfd_mesh_structure.png")
plt.close()

