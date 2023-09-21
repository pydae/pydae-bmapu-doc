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

VSC in PQ mode 


        K_b 
       


        I_ph = I_sc_t*irrad/I_rrad_sts
        
        eq_i_pv = -i_pv + I_ph - I_d - (v_pv+i_pv*R_pv_s)/R_pv_sh 

        I_d = I_0*(sym.exp((v_mpp+i_pv_mpp*R_pv_s)/(V_t*N_s))-1)
        I_ph = I_sc_t*q/I_rrad_sts
        eq_i_pv_mpp  = -i_pv_mpp + I_ph - I_d - (v_mpp+i_pv_mpp*R_pv_s)/R_pv_sh



The PV module datasheet gives the open circuit voltage $V_{oc}$ and the short circuit current $I_{sc}$.
Also the maximum power point voltage $V_{mp}$ and current $I_{mp}$. These values are defined for a given temperature (i.e. $T_{stc}$ =25.0ºC). For other temperatures manufacturers give the factors $K_{vt}$ and $K_{it}$. With this values and the total number of PV modules in series and parallel, $N_s$ and $N_p$, the following voltages and currents can be obtained:        


$$
V_{oc}^t = N_s V_{oc} \left(1 + \frac{K_{vt}}{100} \left( T - T_{stc} \right)\right)
$$
$$
V_{mp}^t = N_s V_{mp} \left(1 + \frac{K_{vt}}{100} \left( T - T_{stc} \right)\right)
$$

$$
I_{sc}^t = N_p I_{sc} \left(1 + \frac{K_{it}}{100} \left(T -T_k^{stc}\right)\right)
$$
$$
I_{mp}^t = N_p I_{mp} \left(1 + \frac{K_{it}}{100} \left(T -T_k^{stc}\right)\right)
$$

Considering the irradiance $E_e$ the following current is obtained, 
$$
    I_{mp}^i = I_{sc}^t \frac{E_e}{1000}
$$

$$
 i_{pv} = \frac{p_s S_n}{v_{dcv}}
$$

$$
0 = -v_{dcv} + V_{mp}^t - \frac{\left(I_{mp}^i - i_{pv}\right) \left(V_{mp}^t - V_{oc}^t\right)}{I_{mp}^i}
$$

$$
v_{dc} = \frac{v_{dcv}}{V_{dcb}}
$$

$$
  p_{mp} = \frac{V{_mp}^t I_{mp}^i}{S_n}
$$








$$
 V_t = \frac{K_d K_b T_k^{stc}}{E_c} 
$$




$$
I_0 =\left(I_{sc}^t - \frac{V_{oc}^t - I_{sc}^t  R_s}{R_{sh}} \right) e^{\left(\frac{-V_{oc}^t}{N_s V_t}\right)}
$$

$$
i_d = I_0 \left(e^{\left(\frac{v_{pv}+i_{pv} R_s}{V_t N_s}\right)}-1\right)
$$

$$
i_{ph} = I_{sc}^t \frac{i_r}{I_{r}^{stc}}
$$

$$
i_{sh} = \frac{v_{pv}+i_{pv} R_s}{R_{sh}} 
$$

$$
i_{pv} = i_{ph} - i_d - i_{sh}
$$

$$
p_{pv} = i_{pv} v_{pv}
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