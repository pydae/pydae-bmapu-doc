# Initialization

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

```{code-cell} python3
model.ini({},'xy_0.json')
```

```{code-cell} python3
model.report_x()  # obtained dynamic states
model.report_y()  # obtained algebraic states
model.report_z()  # obtained outputs
model.report_u()  # obtained algebraic states (theta is both state and output; f_x is both input and output)
model.report_params()  # considered parameters
```


