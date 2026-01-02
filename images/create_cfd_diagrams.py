"""
CFD Diagram Generator for 2D Lid-Driven Cavity Example
======================================================

This script generates two educational diagrams illustrating fundamental CFD concepts:

1. cfd_mesh_structure.png
   - Shows the structured quad mesh with cell centers and faces
   - Highlights boundary conditions on all domain edges
   - Red box highlights one example cell with labeled faces (east, west, north, south)

2. cfd_flux_calculation.png
   - Shows a central cell (P) and its four neighboring cells (E, W, N, S)
   - Cells are drawn as rectangles to show they are adjacent (connected)
   - Displays face flux equations through each shared face
   - Illustrates conservation principle: sum of fluxes balances

Usage:
    python3 create_cfd_diagrams.py

Requirements:
    - matplotlib
    - numpy

The script saves all PNG images to the current directory.
Output resolution: 300 dpi (high quality for documentation)

To regenerate the diagrams, simply run this script.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Rectangle

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
# Diagram 2: Flux Calculation with Connected Cells
# ============================================
fig, ax = plt.subplots(1, 1, figsize=(10, 10))

# Cell size - make it larger so cells touch
cell_size = 0.25

# Center positions (cells are adjacent, touching)
cx, cy = 0.5, 0.5      # P cell center
ex, ey = cx + cell_size, cy         # E cell center (right neighbor)
wx, wy = cx - cell_size, cy         # W cell center (left neighbor)
nx, ny = cx, cy + cell_size         # N cell center (top neighbor)
sx, sy = cx, cy - cell_size         # S cell center (bottom neighbor)

# Draw all five cells as rectangles (adjacent/touching)
# East cell
rect_e = Rectangle((ex - cell_size/2, ey - cell_size/2), cell_size, cell_size,
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.3)
ax.add_patch(rect_e)
ax.plot(ex, ey, 'bs', markersize=11)
ax.text(ex + 0.15, ey, 'E', fontsize=12, weight='bold', ha='left', color='blue')
ax.text(ex + 0.13, ey - 0.08, r'$u_E, v_E, p_E$', fontsize=8, ha='left')

# West cell
rect_w = Rectangle((wx - cell_size/2, wy - cell_size/2), cell_size, cell_size,
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.3)
ax.add_patch(rect_w)
ax.plot(wx, wy, 'bs', markersize=11)
ax.text(wx - 0.15, wy, 'W', fontsize=12, weight='bold', ha='right', color='blue')
ax.text(wx - 0.13, wy - 0.08, r'$u_W, v_W, p_W$', fontsize=8, ha='right')

# North cell
rect_n = Rectangle((nx - cell_size/2, ny - cell_size/2), cell_size, cell_size,
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.3)
ax.add_patch(rect_n)
ax.plot(nx, ny, 'bs', markersize=11)
ax.text(nx, ny + 0.15, 'N', fontsize=12, weight='bold', ha='center', color='blue')
ax.text(nx + 0.08, ny + 0.13, r'$u_N, v_N, p_N$', fontsize=8, ha='left')

# South cell
rect_s = Rectangle((sx - cell_size/2, sy - cell_size/2), cell_size, cell_size,
                    linewidth=2, edgecolor='blue', facecolor='lightblue', alpha=0.3)
ax.add_patch(rect_s)
ax.plot(sx, sy, 'bs', markersize=11)
ax.text(sx, sy - 0.15, 'S', fontsize=12, weight='bold', ha='center', color='blue', va='top')
ax.text(sx + 0.08, sy - 0.13, r'$u_S, v_S, p_S$', fontsize=8, ha='left', va='top')

# Central cell P (highlighted)
rect_p = Rectangle((cx - cell_size/2, cy - cell_size/2), cell_size, cell_size,
                    linewidth=3, edgecolor='red', facecolor='yellow', alpha=0.5)
ax.add_patch(rect_p)
ax.plot(cx, cy, 'ro', markersize=13)
ax.text(cx, cy + 0.08, r'$P$', fontsize=13, weight='bold', ha='center', color='red')
ax.text(cx, cy - 0.08, r'$u_P, v_P, p_P$', fontsize=8, ha='center', weight='bold')

# Draw flux arrows at shared faces (right next to the cells)
arrow_props = dict(arrowstyle='->', lw=3, color='darkgreen', mutation_scale=25)

# East flux (between P and E)
east_face_x = cx + cell_size/2
ax.annotate('', xy=(east_face_x + 0.04, cy), xytext=(east_face_x - 0.04, cy),
            arrowprops=arrow_props)
ax.text(east_face_x + 0.08, cy + 0.08, r'$\phi_E$', fontsize=10, ha='left', weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# West flux (between W and P)
west_face_x = cx - cell_size/2
ax.annotate('', xy=(west_face_x - 0.04, cy), xytext=(west_face_x + 0.04, cy),
            arrowprops={**arrow_props, 'arrowstyle': '<-'})
ax.text(west_face_x - 0.08, cy + 0.08, r'$\phi_W$', fontsize=10, ha='right', weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# North flux (between P and N)
north_face_y = cy + cell_size/2
ax.annotate('', xy=(cx, north_face_y + 0.04), xytext=(cx, north_face_y - 0.04),
            arrowprops=arrow_props)
ax.text(cx + 0.10, north_face_y + 0.08, r'$\phi_N$', fontsize=10, ha='left', weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# South flux (between S and P)
south_face_y = cy - cell_size/2
ax.annotate('', xy=(cx, south_face_y - 0.04), xytext=(cx, south_face_y + 0.04),
            arrowprops={**arrow_props, 'arrowstyle': '<-'})
ax.text(cx - 0.10, south_face_y - 0.08, r'$\phi_S$', fontsize=10, ha='right', weight='bold',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))

# Conservation equation annotation
conservation_eq = r'Conservation: $\phi_E + \phi_W + \phi_N + \phi_S = 0$ (steady-state)'
ax.text(0.5, 0.02, conservation_eq, fontsize=10, weight='bold', ha='center',
        bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

ax.set_xlim(-0.05, 1.05)
ax.set_ylim(-0.05, 1.05)
ax.set_aspect('equal')
ax.set_title('Flux Calculation: Cell P Exchanges Momentum with 4 Adjacent Neighbors',
             fontsize=12, weight='bold', pad=15)
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
