(pv_vsc)=
# PV model considering inverter

```{figure} ./pv_vsc_ctrl.svg
:height: 300px
:name: vsc_pq

VSC in PQ mode with saturation 
```

```{figure} ./pv_module_data.svg
:height: 300px
:name: pv_module

VSC in PQ mode with saturation 
```

```{figure} ./pv_module.svg
:height: 300px
:name: pv_module

VSC in PQ mode with saturation 
```

## PV panel model

The PV module datasheet gives the open circuit voltage $V_{oc}$ and the short circuit current $I_{sc}$.
Also the maximum power point voltage $V_{mp}$ and current $I_{mp}$. These values are defined for a given temperature (i.e. $T_{stc}$ =25.0ºC). For other temperatures manufacturers give the factors $K_{vt}$ and $K_{it}$. With this values and the total number of PV modules in series and parallel, $N_s$ and $N_p$, the following voltages and currents can be obtained:        


$$
V_{oc}^t = N_s V_{oc} \left(1 + \frac{K_{vt}}{100} \left( T - T_{stc} \right)\right)
$$
$$
V_{mp}^t = N_s V_{mp} \left(1 + \frac{K_{vt}}{100} \left( T - T_{stc} \right)\right)
$$

$$
I_{sc}^t = N_p I_{sc} \left(1 + \frac{K_{it}}{100} \left(T -T_{stc}\right)\right)
$$

$$
I_{mp}^t = N_p I_{mp} \left(1 + \frac{K_{it}}{100} \left(T -T_{stc}\right)\right)
$$

Considering the irradiance $E_e$ the following current is obtained, 

$$
    I_{mp}^i = I_{sc}^t \frac{E_e}{1000}
$$

$$
 i_{pv} = \frac{p_s S_n}{v_{dcv}}
$$

$$
\begin{equation}
0 =  V_{mp}^t - \frac{\left(I_{mp}^i - i_{pv}\right) \left(V_{mp}^t - V_{oc}^t\right)}{I_{mp}^i} - v_{dc}  V_{dcb} 
\end{equation}
$$


$$
  p_{mp} = \frac{V_{mp}^t I_{mp}^i}{S_n}
$$


## VSC model
       

### Auxiliar equations

$$
v_{sm} = \sqrt{v_{sd}^2 + v_{sq}^2}
$$

$$
\begin{align}
    i_{sdar}^\star &= \frac{i_{sa}^\star v_{sd} + i_{sr}^\star v_{sq}}{v_{sm}} \\
    i_{sqar}^\star &= \frac{i_{sa}^\star v_{sq} - i_{sr}^\star v_{sd}}{v_{sm}} 
\end{align}
$$

$$
\begin{align}
    i_{sdpq}^\star &= \frac{p_s^\star v_{sd} + q_s^\star v_{sq}}{v_{sd}^2 + v_{sq}^2} \\
    i_{sqpq}^\star &= \frac{p_s^\star v_{sq} - q_s^\star v_{sd}}{v_{sd}^2 + v_{sq}^2}
\end{align}
$$

$$
\begin{align}
    i_{sd}^{'\star} = \left(1-k_{lv} \right) i_{sdpq}^\star + k_{lv} i_{sdar}^\star  \\
    i_{sq}^{'\star} = \left(1-k_{lv} \right) i_{sqpq}^\star + k_{lv} i_{sqar}^\star 
\end{align}
$$

$$
\begin{equation}
 i_{sd}^{\star} =
    \begin{cases}
        -I_{\max} & \text{if } i_{sd}^{'\star} < -I_{\max} \\
        i_{sd}^{'\star} & \text{if }   -I_{\max}\le i_{sd}^{'\star}\le I_{\max} \\
       I_{\max} & \text{if } i_{sd}^{'\star} > I_{\max}
    \end{cases}
\end{equation}
$$

$$
\begin{equation}
 i_{sq}^{\star} =
    \begin{cases}
        -I_{\max} & \text{if } i_{sq}^{'\star} < -I_{\max} \\
        i_{sq}^{'\star} & \text{if }   -I_{\max}\le i_{sq}^{'\star}\le I_{\max} \\
       I_{\max} & \text{if } i_{sq}^{'\star} > I_{\max}
    \end{cases}
\end{equation}
$$

$$
\begin{align}
    v_{td}^\star &=  R_s i_{sd}^\star - X_s i_{sq}^\star + v_{sd}  \\
    v_{tq}^\star &=  R_s i_{sq}^\star + X_s i_{sd}^\star + v_{sq} 
\end{align}
$$

$$
\begin{align}
    v_{tD}^\star &= v_{td}^\star \cos(\delta) + v_{tq}^\star \sin(\delta) \\  
    v_{tQ}^\star &=-v_{td}^\star \sin(\delta) + v_{tq}^\star \cos(\delta)    
\end{align}
$$


$$
\begin{align}
    v_{ti}^\star &= v_{tD}^\star \\
    v_{tr}^\star &= v_{tQ}^\star   
\end{align}
$$

$$
    m^\star = \frac{\sqrt{v_{tr}^{\star 2} + v_{ti}^{\star 2}}}{v_{dc}}
$$

$$
\theta_t^\star = \arctan\left(v_{ti}^\star,v_{tr}^\star\right) 
$$

$$
\begin{align}
    v_{si} = V_s \sin(\theta_s)\\
    v_{sr} = V_s \cos(\theta_s) 
\end{align}
$$

$$
    \Omega_b = 2 \pi F_n
$$ 

$$
\begin{align}
m &= m^\star \\
\theta_t &= \theta_t^\star
\end{align}
$$

$$
\begin{align}
    v_{tm} &= m v_{dc} \\
    v_{tr} &= v_{tm}\cos(\theta_t) \\
    v_{ti} &= v_{tm}\sin(\theta_t)
\end{align}
$$

$$
\begin{align}
  v_{ti} &= v_{ti}^\star \\
  v_{tr} &= v_{tr}^\star \\
  i_{sr} &= \frac{R_s\left(v_{tr} - v_{sr} \right)+ X_s \left( v_{si} - v_{ti}\right)}{R_s^2 + X_s^2} \\
  i_{si} &= \frac{R_s \left(v_{ti} - v_{si}  \right) + X_s \left(v_{tr} -  v_{sr} \right) }{R_s^2 + X_s^2}  
\end{align}
$$


$$
\begin{equation}
 k_{lv} =
    \begin{cases}
        0 & \text{if } v_{sm} > V_{lv} \\
        1 & \text{if } v_{sm} \le V_{lv}  
    \end{cases}
\end{equation}
$$


$$
\begin{equation}
 p_s^\star =
    \begin{cases}
        p_s^{ppc} & \text{if } p_s^{ppc} < p_{mp} \\
        p_{mp}    & \text{if } p_s^{ppc} \ge p_{mp} \\
    \end{cases}
\end{equation}
$$

$$
p_s^\star = q_s^{ppc}
$$


### Algebraic equations   
  
$$
\begin{align}
    0  &= i_{si} v_{si} + i_{sr} v_{sr} - p_s  \\
    0  &= i_{si} v_{sr} - i_{sr} v_{si} - q_s 
\end{align}
$$

### Example input

```{code} 
...
``"vscs":[{"type":"vsc_pq","bus":"1","p_in":0.5,"S_n":10e6,"K_delta":0.0}],
```


| Variable    | Code            | Description                          |  Units  |
| :---------- | :-------------- | :----------------------------------- |:-------:|  
| $K_b$       | ``Boltzman``    | Boltzmann constant                     | J/K      |



| Variable    | Description                          |  Units  |
| :---------- | :----------------------------------- |:-------:|  
| $i_r$       | Irradiancia                          |  $W/m^2$     |
| $T_k$       | Temperatura del módulo               | K     |
| $v_{pv}$    | Tensión del módulo                   |  V     |
| $i_{pv}$    | Corriente del módulo                         |  A    |
| $I_{st}$    | Corriente de corto circuito          | A       |
| $V_{oc}$    | Tensión en circuito abierto          | V       |
| $I_{mpp}$   | Corriente  en MPP                    | A       |
| $V_{mpp}$   | Tensión en MPP                       | V       |
| $K_{vt}$    | Coeficiente de cambio de $V_{oc}$ con la temperatura | %/ºC |
| $K_{it}$    | Coeficiente de cambio de $I_{st}$ con la temperatura | %/ºC |
| $I_{st}^t$  | $I_{st}$ modificada por la temperatura | A       |
| $V_{oc}^t$  | $V_{oc}$ modificada por la temperatura | V       |
| $K_b$       | Boltzmann constant                   | J/K     |
| $K_{d}$     | Factor de calidad (idealidad) del diodo | - |
| $R_{s}$     | Resistencia serie | $\Omega$ |
| $R_{sh}$    | Resistencia paralelo | $\Omega$ |
| $T_{k}^{stc}$    | Temperatura en condiciones estándares de medida (25ºC)  | $K$ |
| $I_{r}^{stc}$    | Irradiancia en condiciones estándares de medida (1000)  | $W/m^2$ |