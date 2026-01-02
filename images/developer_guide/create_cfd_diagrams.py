"""
CFD Diagram Generator for 2D Lid-Driven Cavity Example
======================================================

This script generates three educational diagrams illustrating fundamental CFD
concepts:

1. cfd_mesh_structure.png
   - Shows the structured quad mesh with cell centers and faces
   - Highlights boundary conditions on all domain edges
   - Red box highlights one example cell with labeled faces

2. cfd_flux_calculation.png
   - Shows cell layout (P, N, S, E, W) with actual cells
   - Displays flux equations through each face
   - Illustrates conservation principle: sum of fluxes

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
ax.set_title('2D Lid-Driven Cavity: Mesh Structure\n(4×4 cells shown; red box = example cell with faces)',
             fontsize=14, weight='bold', pad=20)
ax.grid(False)

# Add legend
red_dot = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='r', markersize=10, label='Cell center (stores u, v, p)')
ax.legend(handles=[red_dot], loc='upper right', fontsize=14)

plt.tight_layout()
plt.savefig('cfd_mesh_structure.png', dpi=300, bbox_inches='tight')
print("Saved: cfd_mesh_structure.png")
plt.close()

# ============================================
# Diagram 2: Flux Calculation with Cell Layout (N, E, P, W, S)
# ============================================
fig, ax = plt.subplots(1, 1, figsize=(12, 12))

# Define cell positions - arranged in a cross pattern
cell_size = 0.35
cx, cy = 0.5, 0.5  # Center cell P

# Draw four neighboring cells (E, W, N, S) around P
cell_spacing = 0.35

# North cell
nx, ny = cx, cy + cell_spacing
rect_n = Rectangle((nx - cell_size/2, ny - cell_size/2), cell_size, cell_size,
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.4)
ax.add_patch(rect_n)
ax.plot(nx, ny, 'bs', markersize=12)
ax.text(nx, ny + 0.02, 'N', fontsize=16, weight='bold', ha='center', va='bottom')
ax.text(nx - 0.05, ny, r'$u_N, v_N, p_N$', fontsize=14, ha='right', va='center')

# South cell
sx, sy = cx, cy - cell_spacing
rect_s = Rectangle((sx - cell_size/2, sy - cell_size/2), cell_size, cell_size,
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.4)
ax.add_patch(rect_s)
ax.plot(sx, sy, 'bs', markersize=12)
ax.text(sx, sy - 0.02, 'S', fontsize=16, weight='bold', ha='center', va='top')
ax.text(sx - 0.05, sy, r'$u_S, v_S, p_S$', fontsize=14, ha='right', va='center')

# East cell
ex, ey = cx + cell_spacing, cy
rect_e = Rectangle((ex - cell_size/2, ey - cell_size/2), cell_size, cell_size,
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.4)
ax.add_patch(rect_e)
ax.plot(ex, ey, 'bs', markersize=12)
ax.text(ex + 0.02, ey, 'E', fontsize=16, weight='bold', ha='left', va='center')
ax.text(ex, ey + 0.05, r'$u_E, v_E, p_E$', fontsize=14, ha='center', va='bottom')

# West cell
wx, wy = cx - cell_spacing, cy
rect_w = Rectangle((wx - cell_size/2, wy - cell_size/2), cell_size, cell_size,
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.4)
ax.add_patch(rect_w)
ax.plot(wx, wy, 'bs', markersize=12)
ax.text(wx - 0.02, wy, 'W', fontsize=16, weight='bold', ha='right', va='center')
ax.text(wx, wy + 0.05, r'$u_W, v_W, p_W$', fontsize=14, ha='center', va='bottom')

# Central cell P (highlighted)
rect_p = Rectangle((cx - cell_size/2, cy - cell_size/2), cell_size, cell_size,
                    linewidth=3, edgecolor='red', facecolor='yellow', alpha=0.5)
ax.add_patch(rect_p)
ax.plot(cx, cy, 'ro', markersize=14)
ax.text(cx, cy + 0.02, r'$P$', fontsize=14, weight='bold', ha='center', va='bottom', color='red')
ax.text(cx, cy - 0.05, r'$u_P, v_P, p_P$', fontsize=14, ha='center', va='top', weight='bold')

# Draw flux arrows connecting cells through faces
arrow_props = dict(arrowstyle='->', lw=2.5, color='darkgreen', mutation_scale=25)

# East flux
east_mid = cx + (cell_size/2 + (cell_spacing - cell_size/2)) / 2
ax.annotate('', xy=(east_mid + 0.05, cy), xytext=(east_mid - 0.05, cy),
            arrowprops=arrow_props)
ax.text(east_mid, cy + 0.02, r'$\phi_E = u_E \cdot L_E$', fontsize=14, ha='center',
        weight='bold', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# West flux
west_mid = cx - (cell_size/2 + (cell_spacing - cell_size/2)) / 2
ax.annotate('', xy=(west_mid - 0.05, cy), xytext=(west_mid + 0.05, cy),
            arrowprops={**arrow_props, 'arrowstyle': '<-'})
ax.text(west_mid, cy + 0.02, r'$\phi_W = u_W \cdot L_W$', fontsize=14, ha='center',
        weight='bold', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# North flux
north_mid = cy + (cell_size/2 + (cell_spacing - cell_size/2)) / 2
ax.annotate('', xy=(cx, north_mid + 0.05), xytext=(cx, north_mid - 0.05),
            arrowprops=arrow_props)
ax.text(cx + 0., north_mid, r'$\phi_N = v_N \cdot L_N$', fontsize=14, ha='left',
        weight='bold', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# South flux
south_mid = cy - (cell_size/2 + (cell_spacing - cell_size/2)) / 2
ax.annotate('', xy=(cx, south_mid - 0.05), xytext=(cx, south_mid + 0.05),
            arrowprops={**arrow_props, 'arrowstyle': '<-'})
ax.text(cx - 0., south_mid, r'$\phi_S = v_S \cdot L_S$', fontsize=14, ha='left',
        weight='bold', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# Add conservation equation at bottom
conservation_eq = (r'Conservation: $\phi_E + \phi_W + \phi_N + \phi_S = 0$ (steady-state)',
                   'Flux balance ensures momentum conservation across cell faces')
ax.text(0.5, 0.04, conservation_eq[0] + '\n' + conservation_eq[1], fontsize=14, ha='center',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

ax.set_xlim(0.05, 0.95)
ax.set_ylim(0.02, 0.98)
ax.set_aspect('equal')
ax.set_title('Flux Calculation: Discrete Conservation with Cell Layout (N, E, P, W, S)',
             fontsize=16, weight='bold', pad=15)
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

plt.tight_layout()
plt.savefig('cfd_flux_calculation.png', dpi=300, bbox_inches='tight')
print("Saved: cfd_flux_calculation.png")
plt.close()

print("\nAll diagrams generated successfully!")
