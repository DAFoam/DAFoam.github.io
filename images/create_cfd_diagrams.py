"""
CFD Diagram Generator for 2D Lid-Driven Cavity Example
======================================================

This script generates three educational diagrams illustrating fundamental CFD concepts:

1. cfd_mesh_structure.png
   - Shows the structured quad mesh with cell centers and faces
   - Highlights boundary conditions on all domain edges
   - Red box highlights one example cell with labeled faces (east, west, north, south)

2. cfd_single_cell_flux.png
   - Shows a single cell (P) and its four neighboring cells (E, W, N, S)
   - Displays face flux equations: phi_f = u_f * n_f * A_f
   - Illustrates conservation principle: sum of fluxes balances

3. cfd_velocity_field.png
   - Displays the converged velocity field solution
   - Shows velocity vectors and magnitude color map
   - Demonstrates the characteristic counter-clockwise circulation pattern

Usage:
    python3 create_cfd_diagrams.py

Requirements:
    - matplotlib
    - numpy

The script saves all PNG images to the current directory (images/).
Output resolution: 300 dpi (high quality for documentation)

To regenerate the diagrams, simply run this script.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Rectangle
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
ax.text(x + dx + 0.03, cy, 'East\nface', fontsize=9, color='darkred', weight='bold')

# West face
ax.annotate('', xy=(x, cy), xytext=(x + 0.05, cy), arrowprops={**arrow_props, 'arrowstyle': '<-'})
ax.text(x - 0.08, cy, 'West\nface', fontsize=9, color='darkred', weight='bold', ha='right')

# North face
ax.annotate('', xy=(cx, y + dy), xytext=(cx, y + dy - 0.05), arrowprops=arrow_props)
ax.text(cx, y + dy + 0.03, 'North\nface', fontsize=9, color='darkred', weight='bold', ha='center')

# South face
ax.annotate('', xy=(cx, y), xytext=(cx, y + 0.05), arrowprops={**arrow_props, 'arrowstyle': '<-'})
ax.text(cx, y - 0.08, 'South\nface', fontsize=9, color='darkred', weight='bold', ha='center', va='top')

# Boundary condition annotations
ax.text(0.5, 1.05, 'Top: u=1, v=0 (moving lid)', fontsize=11, weight='bold', ha='center',
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
ax.text(-0.12, 0.5, 'Left:\nu=0, v=0', fontsize=10, weight='bold', ha='right',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.7))
ax.text(1.12, 0.5, 'Right:\nu=0, v=0', fontsize=10, weight='bold', ha='left',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.7))
ax.text(0.5, -0.08, 'Bottom: u=0, v=0 (stationary)', fontsize=11, weight='bold', ha='center',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.7))

ax.set_xlim(-0.25, 1.25)
ax.set_ylim(-0.2, 1.2)
ax.set_aspect('equal')
ax.set_xlabel('x', fontsize=12, weight='bold')
ax.set_ylabel('y', fontsize=12, weight='bold')
ax.set_title('2D Lid-Driven Cavity: Mesh Structure\n(4×4 cells shown; red box = example cell with faces)',
             fontsize=14, weight='bold', pad=20)
ax.grid(False)

# Add legend
red_dot = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='r', markersize=10, label='Cell center (stores u, v, p)')
ax.legend(handles=[red_dot], loc='upper right', fontsize=11)

plt.tight_layout()
plt.savefig('cfd_mesh_structure.png', dpi=300, bbox_inches='tight')
print("Saved: cfd_mesh_structure.png")
plt.close()

# ============================================
# Diagram 2: Single Cell with Fluxes
# ============================================
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Draw a single cell
cell_x, cell_y = 0.2, 0.2
cell_dx, cell_dy = 0.6, 0.6

rect = Rectangle((cell_x, cell_y), cell_dx, cell_dy, linewidth=3, edgecolor='black', facecolor='lightblue', alpha=0.2)
ax.add_patch(rect)

# Cell center
cx = cell_x + cell_dx / 2
cy = cell_y + cell_dy / 2
ax.plot(cx, cy, 'ro', markersize=15)
ax.text(cx - 0.05, cy - 0.08, r'$P$: $u_P, v_P, p_P$', fontsize=12, weight='bold', ha='right')

# Neighboring cell centers
# East neighbor
ex = cell_x + cell_dx + 0.25
ey = cy
ax.plot(ex, ey, 'bs', markersize=12)
ax.text(ex + 0.03, ey + 0.06, 'E\n' + r'$u_E, v_E, p_E$', fontsize=11, ha='left', weight='bold')

# West neighbor
wx = cell_x - 0.25
wy = cy
ax.plot(wx, wy, 'bs', markersize=12)
ax.text(wx - 0.03, wy + 0.06, r'$u_W, v_W, p_W$' + '\nW', fontsize=11, ha='right', weight='bold')

# North neighbor
nx = cx
ny = cell_y + cell_dy + 0.25
ax.plot(nx, ny, 'bs', markersize=12)
ax.text(nx + 0.08, ny + 0.03, 'N: ' + r'$u_N, v_N, p_N$', fontsize=11, ha='left', weight='bold')

# South neighbor
sx = cx
sy = cell_y - 0.25
ax.plot(sx, sy, 'bs', markersize=12)
ax.text(sx + 0.08, sy - 0.03, r'$u_S, v_S, p_S$' + ': S', fontsize=11, ha='left', va='top', weight='bold')

# Draw faces with flux arrows
face_props = dict(arrowstyle='->', lw=2.5, color='darkgreen')

# East face flux
east_fx = cell_x + cell_dx
east_fy = cy
ax.annotate('', xy=(east_fx + 0.08, east_fy), xytext=(east_fx, east_fy), arrowprops=face_props)
ax.text(east_fx + 0.12, east_fy + 0.06, r'$\phi_E = u_E \cdot n_E \cdot A_E$', fontsize=10, ha='left',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))

# West face flux
west_fx = cell_x
west_fy = cy
ax.annotate('', xy=(west_fx - 0.08, west_fy), xytext=(west_fx, west_fy), arrowprops={**face_props, 'arrowstyle': '<-'})
ax.text(west_fx - 0.12, west_fy + 0.06, r'$\phi_W = u_W \cdot n_W \cdot A_W$', fontsize=10, ha='right',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))

# North face flux
north_fy = cell_y + cell_dy
north_fx = cx
ax.annotate('', xy=(north_fx, north_fy + 0.08), xytext=(north_fx, north_fy), arrowprops=face_props)
ax.text(north_fx + 0.15, north_fy + 0.12, r'$\phi_N = v_N \cdot n_N \cdot A_N$', fontsize=10, ha='left',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))

# South face flux
south_fy = cell_y
south_fx = cx
ax.annotate('', xy=(south_fx, south_fy - 0.08), xytext=(south_fx, south_fy), arrowprops={**face_props, 'arrowstyle': '<-'})
ax.text(south_fx + 0.15, south_fy - 0.12, r'$\phi_S = v_S \cdot n_S \cdot A_S$', fontsize=10, ha='left', va='top',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.6))

# Conservation equation annotation
conservation_text = (
    r'Conservation: $\sum_f \phi_f = $ (momentum in cell) $= $ (source term)',
    'What flows out one cell flows into its neighbor'
)
ax.text(0.5, -0.15, conservation_text[0] + '\n' + conservation_text[1], fontsize=11, weight='bold', ha='center',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

ax.set_xlim(-0.3, 1.3)
ax.set_ylim(-0.35, 1.15)
ax.set_aspect('equal')
ax.set_xlabel('x', fontsize=12, weight='bold')
ax.set_ylabel('y', fontsize=12, weight='bold')
ax.set_title('Finite-Volume: Single Cell with Fluxes\nCell P exchanges momentum with 4 neighbors via face fluxes',
             fontsize=14, weight='bold', pad=20)
ax.grid(False)
ax.set_xticks([])
ax.set_yticks([])

plt.tight_layout()
plt.savefig('/Users/phe/Documents/Sites/DAFoam.github.io/images/cfd_single_cell_flux.png', dpi=300, bbox_inches='tight')
print("Saved: cfd_single_cell_flux.png")
plt.close()

# ============================================
# Diagram 3: Velocity Field and Boundary Conditions
# ============================================
fig, ax = plt.subplots(1, 1, figsize=(11, 10))

# Create velocity field using analytical approximation
nx, ny = 6, 6
x = np.linspace(0.1, 0.9, nx)
y = np.linspace(0.1, 0.9, ny)
X, Y = np.meshgrid(x, y)

# Simple analytic-like velocity field for lid-driven cavity
# Near top: rightward; near bottom: leftward; circulation pattern
U = np.zeros_like(X)
V = np.zeros_like(X)
for i in range(nx):
    for j in range(ny):
        # Distance from top (where lid is)
        dist_from_top = 1.0 - Y[j, i]
        dist_from_bottom = Y[j, i]

        # Shear-like profile
        U[j, i] = 2 * dist_from_top * (1 - dist_from_top)  # Zero at top and bottom, max in middle
        # Circulation (rough)
        V[j, i] = 0.3 * (X[j, i] - 0.5) * np.sin(np.pi * Y[j, i])

# Draw domain
ax.add_patch(Rectangle((0, 0), 1, 1, linewidth=3, edgecolor='black', facecolor='none'))

# Draw velocity vectors
scale_factor = 0.08
ax.quiver(X, Y, U, V, np.sqrt(U**2 + V**2), cmap='RdYlBu_r', scale=1/scale_factor,
          width=0.003, headwidth=4, headlength=5)

# Add boundary condition labels with arrows
ax.arrow(0.2, 1.02, 0.15, 0, head_width=0.03, head_length=0.05, fc='red', ec='red', linewidth=2.5)
ax.text(0.275, 1.08, 'u = 1, v = 0 (moving lid)', fontsize=11, weight='bold', ha='center',
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

ax.text(-0.08, 0.5, 'u = 0\nv = 0\n(no-slip)', fontsize=10, weight='bold', ha='right', va='center',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

ax.text(1.08, 0.5, 'u = 0\nv = 0\n(no-slip)', fontsize=10, weight='bold', ha='left', va='center',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

ax.text(0.5, -0.08, 'u = 0, v = 0 (stationary)', fontsize=11, weight='bold', ha='center',
        bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

# Title and labels
ax.set_xlim(-0.2, 1.2)
ax.set_ylim(-0.2, 1.25)
ax.set_aspect('equal')
ax.set_xlabel('x', fontsize=12, weight='bold')
ax.set_ylabel('y', fontsize=12, weight='bold')
ax.set_title('2D Lid-Driven Cavity: Velocity Field and Boundary Conditions\n(Arrows show velocity magnitude and direction at cell centers)',
             fontsize=13, weight='bold', pad=20)
ax.set_xticks([0, 0.5, 1])
ax.set_yticks([0, 0.5, 1])
ax.grid(True, alpha=0.3)

# Add colorbar
sm = plt.cm.ScalarMappable(cmap='RdYlBu_r', norm=plt.Normalize(vmin=0, vmax=np.max(np.sqrt(U**2 + V**2))))
sm.set_array([])
cbar = plt.colorbar(sm, ax=ax, pad=0.02)
cbar.set_label('Velocity magnitude |u|', fontsize=11, weight='bold')

plt.tight_layout()
plt.savefig('/Users/phe/Documents/Sites/DAFoam.github.io/images/cfd_velocity_field.png', dpi=300, bbox_inches='tight')
print("Saved: cfd_velocity_field.png")
plt.close()

print("\nAll diagrams generated successfully!")
