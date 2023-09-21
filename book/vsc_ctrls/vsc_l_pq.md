(vsc_l_ctrl_pq)=
## VSC Control in PQ mode

```{figure} ./vsc_pq.svg
:height: 100px
:name: vsc_pq

VSC in PQ mode with saturation 
```

### Auxiliar equations 
$$
\begin{align}
\delta &= \theta_s \\
v_{sD} &= V_s \sin(\theta_s) \\
v_{sQ} &= V_s \cos(\theta_s)  \\
v_{sd} &= v_{sD} \cos(\delta) - v_{sQ} \sin(\delta) \\ 
v_{sq} &= v_{sD} \sin(\delta) + v_{sQ} \cos(\delta) \\
\Omega_b &= 2 \pi F_n \\
\omega_s &= \omega_{coi} \\
v_{tD}^\star &= v_{td}^\star \cos(\delta) + v_{tq}^\star \sin(\delta)\\ 
v_{tQ}^\star &=-v_{td}^\star \sin(\delta) + v_{tq}^\star \cos(\delta)\\  
v_{ti}^\star &=  v_{tD}^\star \\
v_{tr}^\star &=  v_{tQ}^\star \\  
m^\star &= \frac{\sqrt{ \left( v_{tr}^\star \right)^2 + \left(v_{ti}^\star \right)^2}}{v_{dc}} \\
\theta_t^\star &= atan(v_{ti}^\star,v_{tr}^\star)  
\end{align}
$$

### Diferential equations

Only algebraic.



### Algebraic equations


$$
\begin{align}
    0  &= i_{sd}^\star v_{sd} + i_{sq}^\star v_{sq} - p_s^\star \\  
    0  &= i_{sq}^\star v_{sd} - i_{sd}^\star v_{sq} - q_s^\star \\  
    0  &= v_{td}^\star - R_s i_{sd}^\star - X_s i_{sq}^\star - v_{sd}  \\  
    0  &= v_{tq}^\star - R_s i_{sq}^\star + X_s i_{sd}^\star - v_{sq}  \\  
    0  &= m-m^\star\\
    0  &= \theta_t-\theta_t^\star\\
\end{align}
$$

### Dynamic and algebraic states

$$ 
\mathbf x = \left[
\begin{array}{c} 
\;\end{array} \right] \;\;\;\;\;\;
\mathbf y = \left[
\begin{array}{c} 
 i_{sd}^\star \\ 
 i_{sq}^\star \\ 
 v_{td}^\star \\ 
 v_{tq}^\star \\
 m \\
\theta_t
\end{array} \right]
$$

### Inputs and outputs

$$ 
\mathbf u = \left[
\begin{array}{c} 
p_s^\star \\ 
q_s^\star
\end{array} \right] \;\;\;\;\;\;
\mathbf z = \left[
\begin{array}{c} 
\;
\end{array} \right] 
$$


### Example input

```{code} 
"vscs": [{"bus":"MPE","type":"vsc_l","S_n":100e6,"F_n":50.0,"X_s":0.1,"R_s":0.01,
         "ctrl":{"type":"pq","p_s_ref":0.2,"q_s_ref":0.1}}],
```

### Parameters


| Variable    | Data       | pydae           | Default    | Description               |  Units  |
| :---------- | :--------- | :---------      | :--------- | :------------------------ |:-------:|  
| $S_n$       | ``S_n``    | ``S_n_<id>``    | 1e6        | Nominal power             | VA      |
| $F_n$       | ``F_n``    | ``F_n_<id>``    |  50.0      | Nominal frequency         | Hz      |
| $X_s$       | ``X_s``    | ``X_s_<id>``    |  0.10      | Coupling filter reactance | pu-m    |
| $R_s$       | ``R_s``    | ``R_s_<id>``    |  0.01      | Coupling filter resistance| pu-m    |


### Inputs

| Variable       | Data          | pydae             | Description              |  Units |
| :--------------|:----------    |:----------        | :----------------------- | :-----:|
| $p_s^\star$    | ``p_s_ref``   | ``p_s_ref_<id>``  | Active power reference   |  pu-m  |
| $q_s^\star$    | ``q_s_ref``   | ``q_s_ref_<id>``  | Reactive power reference |  pu-m  |


### Algebraic states


| Variable       | pydae            | Description                                  |  Units  |
| :----------    | :----------      | :------------------------------------------- |:-------:|  
| $i_{sr}$       | ``i_sr_<id>``    | Injected current reference d                 | pu-m    |
| $i_{si}$       | ``i_si_<id>``    | Injected current reference q                 | pu-m    |
| $v_{td}^\star$ | ``p_s_<id>``     | Injected active power                        | pu-m    |
| $v_{tq}^\star$ | ``v_tq_ref_<id>``| Injected aeactive power                      | pu-m    |
| $m$            | ``m_<id>``       | Modulation factor                            | pu-m    |
| $\theta_t$     | ``theta_t_<id>`` | Internal angle                               | rad     |


 
