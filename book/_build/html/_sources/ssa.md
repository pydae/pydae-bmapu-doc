# SSA

Small signal analysis (SSA)


For the given nonlinear DAE system:

$$
\begin{split}  
\mathbf {\dot x}  &   =  \mathbf{f (x,y,u) } \\
\mathbf 0 &   =  \mathbf{g (x,y,u) }  \\
\mathbf z &   =  \mathbf{h (x,y,u) } 
\end{split}
$$

with:

- $ \mathbf x$: dynamic states
- $ \mathbf y$: algebraic states
- $ \mathbf u$: known inputs		
- $ \mathbf f$: differential equations
- $ \mathbf g$: algebraic equations	
- $ \mathbf z$: outputs
- $ \mathbf h$: outputs functions


The steady state can be obtained by solving the following algebraic system for $ \mathbf x$ and $ \mathbf y$ for given inputs $ \mathbf u$:

$$
\begin{split}   
\mathbf 0 & =  \mathbf{f (x,y,u) } \\
\mathbf 0 & =  \mathbf{g (x,y,u) }   
\end{split}
$$
The solution for the previous system can be renamed as $\mathbf x_0$, $\mathbf y_0$. And the vector $\mathbf z_0$ can be also computed for the given input $\mathbf u_0$.

A linear system with the following form can be obtained: 
$$
\begin{split}
\Delta \mathbf{\dot {x}} &= \mathbf{A}\Delta \mathbf{x} + \mathbf{B}\Delta \mathbf{u}\\  
\Delta \mathbf{ {z}}     &= \mathbf{C}\Delta \mathbf{x} + \mathbf{D}\Delta \mathbf{u}
\end{split}
$$
where $\Delta \mathbf x = \mathbf x - \mathbf {x_0}$, $\Delta \mathbf y = \mathbf y - \mathbf {y_0}$, $\Delta \mathbf u = \mathbf u - \mathbf {u_0}$ and $\Delta \mathbf z = \mathbf z - \mathbf {z_0}$. 

To perform the small-signal analysis, the equivalent of the $ \bf A$ matrix must be found. To do this, the equilibrium point have to be determined and then linelize the system. Using the Taylor series:

$$
\begin{equation} 
 \mathbf {f (x,y) }  \approx \mathbf {f (x_0,y_0) + F_x\left|_{x_0,y_0}\right.}  \Delta \mathbf { x  + F_y\left|_{x_0,y_0}\right.}  \Delta   \mathbf y
\end{equation}
$$

$$
\begin{equation}
 \mathbf {g (x,y) }  \approx \mathbf {g (x_0,y_0) + G_x\left|_{x_0,y_0}\right.}  \Delta  \mathbf {x  + G_y\left|_{x_0,y_0}\right.}  \Delta   \mathbf y
\end{equation}
$$

Making:
$$
	\begin{equation} 
	 \Delta \mathbf { \dot  x   = f (x,y) - f (x_0,y_0)}
	\end{equation}
$$

It is obtained:
$$
	\begin{equation} 
	\begin{split}
	 \Delta \mathbf { \dot  x } &= \mathbf {F_x^0}  \Delta \mathbf { x  + F_y^0}  \Delta \mathbf {y} \\
	 \mathbf {0} &= \mathbf {G_x^0}  \Delta  \mathbf {x  + G_y^0}  \Delta   \mathbf y
	\end{split}
	\end{equation}\\
$$

Where:
$$
\begin{equation} 
\begin{split}
\mathbf {F_x^0} = \mathbf {F_x\left|_{x_0y_0}\right.}  & \;\;\;\; \mathbf {F_y^0  = F_y \left|_{x_0,y_0}\right.}  \\
\mathbf {G_x^0} = \mathbf {G_x\left|_{x_0y_0}\right.}  & \;\;\;\; \mathbf {G_y^0  = G_y \left|_{x_0,y_0}\right.} 
\end{split}
\end{equation}
$$


Assuming $\det(\mathbf{G_y^0})\neq \mathbf{0}$ e can obtain $\Delta \mathbf y$ being expressed as follows:
$$
\begin{equation}
 \Delta \mathbf{y} =  - \left( \mathbf{G_y^0} \right)^{-1} \mathbf{G_x^0} \Delta \mathbf{x}  	
\end{equation}
$$
leaving the algebraic states as functions of the dynamic states, the inputs and the parameters.


In pydae once the initial state is obtained it is possible to use ssa module to compute the  $\mathbf{A}$ matrix as follows:


```{code-cell} python3
ssa.A_eval(model)
```

The matrix A can be accessed by doing:

```{code-cell} python3
model.A
```

The `ssa` module also have a function to compute the eigenvalues of $\mathbf{A}$ and to create a pandas dataframe. This dataframe is displayed automatically in a jupyter notebook:
```{code-cell} python3
ssa.damp_report(model).round(2).sort_values('Damp')
```



$$
\begin{equation}
\Delta \mathbf{\dot {x}} = \underbrace {\left( {\mathbf{F_x^0}  - \mathbf{F_y^0} \left( \mathbf{G_y^0} \right)^{-1} \mathbf{G_x^0} } \right)}_\mathbf{A}\Delta \mathbf{x}  
\end{equation}
$$

### Full linear state space model system


$$
\begin{align}
\Delta \mathbf{\dot {x}} &= \underbrace {\left( {\mathbf{F_x^0}  - \mathbf{F_y^0} \left( \mathbf{G_y^0} \right)^{-1} \mathbf{G_x^0} } \right)}_\mathbf{A}\Delta \mathbf{x} + \underbrace {\left( {\mathbf{F_u^0}  - \mathbf{F_y^0} \left( \mathbf{G_y^0} \right)^{-1} \mathbf{G_u^0} } \right)}_\mathbf{B}\Delta \mathbf{u}\\  
\Delta \mathbf{ {z}} &= \underbrace {\left( {\mathbf{H_x^0}  - \mathbf{H_y^0} \left( \mathbf{G_y^0} \right)^{-1} \mathbf{G_x^0} } \right)}_\mathbf{C}\Delta \mathbf{x} + \underbrace {\left( {\mathbf{H_u^0}  - \mathbf{H_y^0} \left( \mathbf{G_y^0} \right)^{-1} \mathbf{G_u^0} } \right)}_\mathbf{D}\Delta \mathbf{u}
\end{align}
$$

$$
\begin{align}
\Delta \mathbf{\dot {x}} &= \mathbf{A}\Delta \mathbf{x} + \mathbf{B}\Delta \mathbf{u}\\  
\Delta \mathbf{ {z}}     &= \mathbf{C}\Delta \mathbf{x} + \mathbf{D}\Delta \mathbf{u}
\end{align}
$$


```{code-cell} python3
ssa.ss_eval(model)
```


