(vsc_l_)=
## VSC with coupling inductor

```{figure} ./vsc_comentado.svg
:height: 300px
:name: vsc_pq


```
 
```{figure} ./ac_3ph_3w_l.svg
:height: 400px
:name: vsc_pq


```

```{figure} ./ac_1ph_1w_l.svg
:height: 200px
:name: vsc_pq


```

$$  Z_s = R_{s} + j X_{s} $$
$$  \vec v_t = v_{tm} \angle \theta_t = v_{tr} + j v_{ti} $$
$$  \vec v_s = v_{sm} \angle \theta_s = v_{sr} + j v_{si} $$
$$  \vec i_s = i_{sr} + j i_{si} $$
$$  s_s = p_s + j q_s = \vec v_s \vec i_s^*$$

$$ 0 = \vec v_t - \vec i_s Z_s - \vec v_s $$

 


### Example input

```{code} 
...
"vscs": [{"bus":"MPE","type":"vsc_l","S_n":100e6,"F_n":50.0,"X_s":0.1,"R_s":0.01}],
```







 

 

## Differential algebraic equations model  

$$
\begin{split}   \nonumber
\mathbf {\dot x}  &   =  \mathbf{f (x,y,u,p) } \\
\mathbf 0 &   =  \mathbf{g (x,y,u,p) }  \\
\mathbf z &   =  \mathbf{h (x,y,u,p) } 
\end{split}
$$

with:

- $ \mathbf x$: dynamic states
- $ \mathbf y$: algebraic states
- $ \mathbf u$: known inputs	
- $ \mathbf p$: parameters		
- $ \mathbf f$: differential equations
- $ \mathbf g$: algebraic equations	
- $ \mathbf z$: outputs
- $ \mathbf h$: outputs functions


### Auxiliar equations

$$
\begin{align}
    v_{sr} &=  V_s\cos(\theta_s) \\
    v_{si} &=  V_s\sin(\theta_s) \\
    \Omega_b &= 2\pi F_n \\
    v_{tm} &= m \cdot v_{dc} \\
    v_{tr} &=  v_{tm} \cos(\theta_t) \\
    v_{ti} &=  v_{tm} \sin(\theta_t) \\
    i_m &= \sqrt{i_{sr}^2 + i_{si}^2} \\
    p_{loss} &= A_l + B_l i_m + C_l i_m^2 \\
    p_{ac} &= p_s + R_s i_m^2 \\
    i_d &= p_{dc}/v_{dc}
\end{align} 
$$

### Diferential equations

Only algebraic.



### Algebraic equations
    

$$
\begin{align}
    0 &= v_{ti} - R_s i_{si} - X_s i_{sr} - v_{si}  \\
    0 &= v_{tr} - R_s i_{sr} + X_s i_{si} - v_{sr} \\
    0 &=  i_{sr} v_{sr} + i_{si} v_{si} - p_s  \\
    0 &=  i_{sr} v_{si} - i_{si} v_{sr} - q_s \\
    0 &= -p_{dc} + p_{ac} + p_{loss} 
\end{align} 
$$

### Dynamic and algebraic states

$$ 
\mathbf x = \left[
\begin{array}{c} 
\;\end{array} \right] \;\;\;\;\;\;
\mathbf y = \left[
\begin{array}{c} 
 i_{sr} \\ 
 i_{si} \\ 
 p_s \\ 
 q_s \\
 p_{dc}
\end{array} \right]
$$

### Inputs and outputs

$$ 
\mathbf u = \left[
\begin{array}{c} 
 m \\ 
 \theta_t 
\end{array} \right] \;\;\;\;\;\;
\mathbf z = \left[
\begin{array}{c} 
 p_{ac} \\ 
 i_d 
\end{array} \right] 
$$


| Variable    | Data       | pydae      | Default    | Description               |  Units  |
| :---------- | :--------- | :--------- | :--------- | :------------------------ |:-------:|  
| $S_n$       | ``S_n``    | ``S_n``    | 1e6        | Nominal power             | VA      |
| $F_n$       | ``F_n``    | ``F_n``    |  50.0      | Nominal frequency         | Hz      |
| $X_s$       | ``X_s``    | ``X_s``    |  0.10      | Coupling filter reactance | pu-m    |
| $R_s$       | ``R_s``    | ``R_s``    |  0.01      | Coupling filter resistance| pu-m    |



### Inputs

| Variable       | Data         | Description              |  Units |
| :--------------| :----------  | :----------------------- | :-----:|
| $m$            | ``m``        | Modulation factor        |  pu-m  |
| $\theta_t$     | ``theta_t``  | Internal phase angle     |  rad   |


### Algebraic states


| Variable    | pydae            | Description                                  |  Units  |
| :---------- | :----------      | :------------------------------------------- |:-------:|  
| $i_{sr}$    | ``i_sr_<id>``    | Injected current real part                   | pu-m    |
| $i_{si}$    | ``i_si_<id>``    | Injected current imaginary part              | pu-m    |
| $p_s$       | ``p_s_<id>``     | Injected active power                        | pu-m    |
| $q_s$       | ``q_s_<id>``     | Injected aeactive power                      | pu-m    |
| $p_{dc}$    | ``p_dc_<id>``    | DC side power                                | pu-m    |

