(milano4)=
# Milano 4

Synchronous machine model of order 4 from Federico Milano book.

```{figure} ./sm_grid.svg
:height: 500px
:name: sm_grid

Synchronous Machine (SM)
```

```{code} 
...
"syns":[
      {"bus":"1","S_n":1500e6,
       "X_d":2.135,"X1d":0.34, "T1d0":6.47,    
       "X_q":2.046,"X1q":0.573,"T1q0":0.61,  
       "R_a":0.01,"X_l": 0.234, 
       "H":6.3,"D":0.0,
       "Omega_b":314.159,"omega_s":1.0,
       "K_sec":0.0,"K_delta":0.0}, 
       ]
...
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
    v_d &=  V \sin(\delta - \theta) \\
    v_q &=  V \cos(\delta - \theta) \\
    p_e &=  i_d \left(v_d + R_a i_d\right) + i_q \left(v_q + R_a i_q\right)  \\   
    \omega_s &=  \omega_{coi}
\end{align} 
$$

### Diferential equations


$$
\begin{align}
    \frac{ d\delta}{dt} &= \Omega_b \left(\omega - \omega_s \right) - K_{\delta} \delta  \\
    \frac{ d\omega}{dt} &= \frac{1}{2H} \left(p_m - p_e - D  \left(\omega - \omega_s \right) \right)  \\
    \frac{ de'_q}{dt} &= \frac{1}{T'_{d0}} \left(-e'_q - \left(X_d - X'_d\right) i_d + v_f\right)  \\
    \frac{ de'_d}{dt} &= \frac{1}{T'_{q0}} \left(-e'_d + \left(X_q - X'_q\right) i_q\right)
\end{align} 
$$


### Algebraic equations
    

$$
\begin{align}
        0  &= v_q + R_a i_q + X'_d i_d - e'_q \\
        0  &= v_d + R_a i_d - X'_q i_q - e'_d \\
        0  &= i_d v_d + i_q v_q - p_g  \\
        0  &= i_d v_q - i_q v_d - q_g 
\end{align} 
$$

### Dynamic and algebraic states


$$ 
\mathbf x = \left[
\begin{array}{c} 
\delta \\ 
\omega \\ 
e'_q \\ 
e'_d
\end{array} \right] \;\;\;\;\;\;
\mathbf y = \left[
\begin{array}{c} 
 i_d \\ 
 i_q \\ 
 p_g \\ 
 q_g
\end{array} \right]
$$

### Inputs and outputs

$$ 
\mathbf u = \left[
\begin{array}{c} 
 v_f \\ 
 p_m 
\end{array} \right] \;\;\;\;\;\;
\mathbf z = \left[
\begin{array}{c} 
 p_e \\ 
 v_f \\
 p_m 
\end{array} \right] 
$$


### Parameters


| Constant    | Data       | pydae            | Default   | Description                                  |  Units  |
| :---------- | :----------| :----------      |       ---:| :------------------------------------------- |:-------:|  
| $S_n$       | ``S_n``    | ``S_n_<id>``     | 20e6      | Nominal power                                | VA      |
| $H$         | ``H``      | ``H_<id>``       | 5.0       | Inertia constaant                            | s       |
| $D$         | ``D``      | ``D_<id>``       | 1.0       | Damping coefficient                          | s       |
| $X_q$       | ``X_q``    | ``X_q_<id>``     | 1.70      | q-axis synchronous reactance                 | pu-m    |
| $X'_q$      | ``X1q``    | ``X1q_<id>``     | 0.55      | q-axis transient reactance                   | pu-m    |
| $T'_{q0}$   | ``T1q0``   | ``T1q0_<id>``    | 0.40      | q-axis open circuit transient time constant  | s       |
| $X_d$       | ``X_d``    | ``X_d_<id>``     | 1.8       | d-axis synchronous reactance                 | pu-m    | 
| $X'_d$      | ``X1d``    | ``X1d_<id>``     | 0.3       | d-axis transient reactance                   | pu-m    |
| $T'_{d0}$   | ``T1d0``   | ``T1d0_<id>``    | 8.0       | d-axis open circuit transient time constant  | s       |   
| $R_a$       | ``R_a``    | ``R_a_<id>``     | 0.01      | Armature resistance                          | pu-m    |    
| $K_{\delta}$| ``K_delta``| ``K_delta_<id>`` | 0.0       | Reference machine constant                   | -       | 
| $K_{sec}$   | ``K_sec``  | ``K_sec_<id>``   | 1.0       | Secondary frequency control participation    | -       | 



### Dynamic states

| Variable    | pydae            | Description                                  |  Units  |
| :---------- | :----------      | :------------------------------------------- |:-------:|        
| $\delta$    | ``delta_<id>``   | Rotor angle                                  | rad     |
| $\omega$    | ``omega_<id>``   | Rotor speed                                  | pu      |
| $e'_q  $    | ``e1q_<id>``     | q-axis transient voltage                     | pu      |
| $e'_d  $    | ``e1d_<id>``     | d-axis transient voltage                     | pu      |


### Algebraic states


| Variable    | pydae            | Description                                  |  Units  |
| :---------- | :----------      | :------------------------------------------- |:-------:|  
| $i_d$       | ``i_d_<id>``     | d-axis current                               | pu-m    |
| $i_q$       | ``i_q_<id>``     | q-axis current                               | pu-m    |
| $p_g$       | ``p_g_<id>``     | Active power                                 | pu-m    |
| $q_g$       | ``q_g_<id>``     | Reactive power                               | pu-m    |

   
### Inputs

| Variable    | pydae        | Default   | Description                                  |  Units  |
| :---------- | :----------  |   -------:| :------------------------------------------- |:-------:| 
| $v_f$       |``v_f_<id>``  |      1.5  | Field voltage                                | pu-m    |
| $p_m$       |``p_m_<id>``  |      0.5  | Mechanical power                             | pu-m    |
        