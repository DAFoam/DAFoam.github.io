"""
Run the following command to install pyXDSM before running this script! pyXDSM requires Python 3+

pip install pyxdsm

Then, run this command to generate the design structure matrix

python dsm_simple.py


"""

from pyxdsm.XDSM import XDSM, FUNC

# Change `use_sfmath` to False to use computer modern
x = XDSM(use_sfmath=False)

# define the component, give it a tag call "Aero", and its component type is FUNC (function), and use "Aerodynamic Component" as its text
x.add_system("R", FUNC, ["\\textrm{Governing equation}", "\\vec{R}(\\vec{x}, \\vec{w})=0"])
x.add_system("f", FUNC, ["\\textrm{Objective function}", "f(\\vec{x}, \\vec{w})"])

# define the input and output for the "Aero" component
x.add_input("R", "\\vec{x}")
x.add_input("f", "\\vec{x}")
x.connect("R", "f", "\\vec{w}")
x.add_output("f", "f", side="right")

x.write("f_calculation")
