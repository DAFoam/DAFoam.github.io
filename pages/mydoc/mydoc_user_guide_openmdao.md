---
title: OpenMDAO Basics
keywords: user guide
summary: 
sidebar: mydoc_sidebar
permalink: mydoc_user_guide_openmdao.html
folder: mydoc
---

{% include note.html content="This webpage is under construction." %}

OpenMDAO is an open-source optimization framework and a platform for building new analysis tools with analytic derivatives. DAFoam is coupled with OpenMDAO to perform MDO. To understand the basic of OpenMDAO, the following tutorial is presented. 

<img src="{{ site.url }}{{ site.baseurl }}/images/user_guide/example_xdsm.png" width="500" />

Fig. 1. Example eXtended Design Structure Matrix (XDSM). The red component is implicit
and the green one is explicit. The blue component is an independent variable that is not necessary for this optimization, but it shows how an independent variable component can be added to the system. The design variable is *x* and the objective function is *f*. *y* is the solution from the implicit component and is passed to the explicit component as
the input to compute *f*.

Below is an N2, or N-squared, diagram that OpenMDAO can output when you run a problem. The N2 diagram will output as .html, which can be opened within a web browser. This is an interactive diagram can help you visualize your connections within your optimization framework. 

<img src="{{ site.url }}{{ site.baseurl }}/images/user_guide/example_n2.png" width="500" />

Fig. 2. The N2 diagram for the two-component optimization. 

Below are the pieces of the runScript. 

```python
class ImplicitEqn(om.ImplicitComponent):
    def setup(self):
        # define input
        self.add_input("x", val=1.0)
        # define output
        self.add_output("y", val=1.0)

    def setup_partials(self):
        # Finite difference all partials.
        self.declare_partials("*", "*", method="fd")

    def apply_nonlinear(self, inputs, outputs, residuals):
        # get the input and output and compute the residual
        # R = e^(-x * y) - y
        # NOTE: we use [0] here because OpenMDAO assumes all inputs
        # and outputs are arrays. If the input is a scalar, OpenMDAO
        # will create an array that has size 1, so to get its value
        # we have to use [0]
        x = inputs["x"][0]
        y = outputs["y"][0]
        residuals["y"] = np.exp(-x * y) - y
```

This snippet above defines an implicit component (`om.ImplicitComponent`). In this case, first design the `setup` function. This function is where you can add inputs and outputs. This is where you also can define your partials, if necessary. Below that is where you define the `setup_partials` function. In this case, the line `self.declare_partials("\*", "\*", method="fd")` declares the partials of every input w.r.t. every output using the `"\*"` and the partial is calculated using `"fd"` (finite difference). Other methods are `"cs"` (complex step) or, by not calling a method, OpenMDAO assumes it will be calculated analytically. For an implicit component, we create the apply_nonlinear function to define and calculate the residuals. See [Implicit Component Documentation](https://openmdao.org/newdocs/versions/latest/features/core_features/working_with_components/implicit_component.html) for more information. 

```python
class Objective(om.ExplicitComponent):
    def setup(self):

        # define input
        self.add_input("y", val=1.0)

        # define output
        self.add_output("f", val=1.0)

    def setup_partials(self):
        # Finite difference all partials.
        self.declare_partials("*", "*", method="fd")

    def compute(self, inputs, outputs):
        # compute the output based on the input
        y = inputs["y"][0]

        outputs["f"] = 2 * y * y - y + 1
```

The snippet above defines an explicit component (`om.ExplicitComponent`). Similar to the implicit component, the first steps are defining the `setup` and `setup_partials` functions. Now, we define the `compute` function, where we call the inputs from the setup and calculate the outputs from setup. The syntax, as shown in the snippet, must be followed in order for OpenMDAO to recognize the inputs and outputs. If you were to calculate partial derivatives analytically, you will also define a `compute_partials` function and then run the calculations. See [Explicit Component Documentation](https://openmdao.org/newdocs/versions/latest/features/core_features/working_with_components/explicit_component.html) for more information. 

```python
# create an OpenMDAO problem object
prob = om.Problem()
# now add the implicit component defined above to prob
prob.model.add_subsystem("ImplicitEqn", ImplicitEqn(), promotes=["*"])
# add the objective explicit component defined above to prob
prob.model.add_subsystem("Objective", Objective(), promotes=["*"],)
# set the linear/nonlinear equation solution for the implicit component
prob.model.nonlinear_solver = om.NewtonSolver(solve_subsystems=False)
prob.model.linear_solver = om.ScipyKrylov()
# set the design variable and objective function
prob.model.add_design_var("x", lower=-10, upper=10)
prob.model.add_objective("f", scaler=1)
# setup the optimizer
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options["optimizer"] = "SLSQP"
# setup the problem
prob.setup()
# write the n2 diagram
om.n2(prob, show_browser=False, outfile="n2.html")
# run the optimization
prob.run_driver()
```

The snippet above defines the OpenMDAO problem and sets the necessary parameters to run the problem. First, you simply make an OpenMDAO problem (`om.Problem()`). Next, you add all the subsystems you created. In this case, the ImplicitEqn (implicit component) and Objective (explicit component) are the subsystems. In the line `prob.model.add_subsystem("ImplicitEqn", ImplicitEqn(), promotes=["\*"])` we add the subsystem to the model (`prob.model.add_subsystem`), name the subsystem (`"ImplicitEqn"` -- many times the name can be the same as the name you used to define it), call the OpenMDAO class that corresponds to the subsystem (`ImplicitEqn()`), and then promote the variables you want to include (`promotes=["\*"]`), which means call all inputs and outputs -- separate flags exist for the inputs and outputs: `promotes_inputs=...` and `promotes_outputs=...` if you want to call them separately or only promote certain outputs). Next, we add the nonlinear and linear solvers (see [Solvers](https://openmdao.org/newdocs/versions/latest/theory_manual/solver_api.html?highlight=list%20linear%20nonlinear%20solvers) for a list of OpenMDAO solvers). After that, we set the design variable(s) and objective function. Under the add_design_var, first name the variable, then, as in this case, you can add an upper and lower bound for the design variable. Under the add_objective, first name the objective function, then, as in this case, you can add a scaler flag to multiply the model value to get a scaled value. Under each of these, a `units=...` flag can also be added if they need to be specified. Next, we set the driver to actually run the optimization. Under the options (`prob.driver.option["optimizer"]`), set the optimizer you choose to use (as a string). Refer to [Drivers](https://openmdao.org/newdocs/versions/latest/features/building_blocks/drivers/index.html) for a list of drivers and optimizers that OpenMDAO supports. Finally, we can setup the problem (prob.setup()). As an option, you can generate the n2 diagram. Lastly, to run the problem, we add the final line `prob.run_driver()` which will run the entire optimization. 


{% include links.html %}
