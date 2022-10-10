(milano4)=
## Milano 4

Synchronous machine model of order 4 from Federico Milano book.


```{code} 
...
"syns":[
      {"bus":"1","S_n":1500e6,
       "X_d":2.135,"X1d":0.34, "T1d0":6.47,    
       "X_q":2.046,"X1q":0.573,"T1q0":0.61,  
       "R_a":0.0,"X_l": 0.234, 
       "H":6.3,"D":0.0,
       "Omega_b":314.1592653589793,"omega_s":1.0,"K_sec":0.0,
       "avr":{"type":"ntsst4","K_pr":3.15,"K_ir":3.15,"V_rmax":1.0,"V_rmin":-0.87,"T_a":0.02,"K_pm":1.0,"K_im":0.0,"K_p":6.5,"v_ref":1.0}, 
         "gov":{"type":"agov1","Droop":100.0,"T_1":1.0,"T_2":1.0,"T_3":1.0, "p_c":0.9,"omega_ref":1.0, "K_imw":0.0001},
       "pss":{"type":"pss2","K_s3":1.0,"T_wo1":2.0,"T_wo2":2.0,"T_9":0.1,
              "K_s1":17.069,"T_1":0.28,"T_2":0.04,"T_3":0.28,"T_4":0.12,"T_wo3":2.0,"K_s2": 0.158,"T_7":2.0}, 
         "K_delta":0.00}, 
...
```

 **Auxiliar equations**

$$
\begin{eqnarray}
    v_d &=& V \sin(\delta - \theta) \\
    v_q &=& V \cos(\delta - \theta) \\
    p_e &=& i_d \left(v_d + R_a i_d\right) + i_q \left(v_q + R_a i_q\right)  \\   
    \omega_s &=& \omega_{coi}
\end{eqnarray} 
$$

**Dynamic equations**

$$
\begin{eqnarray}
    \frac{ d\delta}{dt} &=& \Omega_b \left(\omega - \omega_s \right) - K_{\delta} \delta  \\
    \frac{ d\omega}{dt} &=& \frac{1}{2H} \left(p_m - p_e - D  \left(\omega - \omega_s \right) \right)  \\
    \frac{ de'_q}{dt} &=& \frac{1}{T'_{d0}} \left(-e'_q - \left(X_d - X'_d\right) i_d + v_f\right)  \\
    \frac{ de'_d}{dt} &=& \frac{1}{T'_{q0}} \left(-e'_d + \left(X_q - X'_q\right) i_q\right)
\end{eqnarray} 
$$


#### Algebraic equations
    

$$
\begin{eqnarray}
        0  &=& v_q + R_a i_q + X'_d i_d - e'_q \\
        0  &=& v_d + R_a i_d - X'_q i_q - e'_d \\
        0  &=& i_d v_d + i_q v_q - p_g  \\
        0  &=& i_d v_q - i_q v_d - q_g 
\end{eqnarray} 
$$

| Variable    | Code        | Description                                  |  Units  |
| :---------- | :---------- | :------------------------------------------- |:-------:|  
| $S_n$       | ``S_n``     | Nominal power                                | VA      |
| $H$         | ``H``       | Inertia constaant                            | s       |
| $S_n$       | ``S_n``     | Nominal power                                | VA      |
| $D$         | ``D``       | Damping coefficient                          | s       |
| $X_q$       | ``X_q``     | q-axis synchronous reactance                 | pu-m    |
| $X'_q$      | ``X1q``     | q-axis transient reactance                   | pu-m    |
| $T'_{q0}$   | ``T1q0``    | q-axis open circuit transient time constant  | s       |
| $X_d$       | ``X_d``     | d-axis synchronous reactance                 | pu-m    | 
| $X'_d$      | ``X1d``     | d-axis transient reactance                   | pu-m    |
| $T'_{d0}$   | ``T1d0``    | d-axis open circuit transient time constant  | s       |   
| $R_a$       | ``R_a``     | Armature resistance                          | pu-m    |    
| $K_{\delta}$| ``K_delta`` | Reference machine constant                   | -       | 
| $K_{sec}$   | ``K_sec``   | Secondary frequency control participation    | -       | 


| Variable    | Code        | Description                                  |  Units  |
| :---------- | :---------- | :------------------------------------------- |:-------:|        
| $\delta$    | ``delta``   | Rotor angle                                  | rad     |
| $\omega$    | ``omega``   | Rotor speed                                  | pu      |
| $e'_q  $    | ``e1q``     | q-axis transient voltage                     | pu      |
| $e'_d  $    | ``e1d``     | d-axis transient voltage                     | pu      |



| Variable    | Code        | Description                                  |  Units  |
| :---------- | :---------- | :------------------------------------------- |:-------:|  
| $i_d$       | ``i_d``     | d-axis current                               | pu-m    |
| $i_q$       | ``i_q``     | q-axis current                               | pu-m    |
| $p_g$       | ``p_g``     | Active power                                 | pu-m    |
| $q_g$       | ``q_g``     | Reactive power                               | pu-m    |
   

| Variable    | Code        | Description                                  |  Units  |
| :---------- | :---------- | :------------------------------------------- |:-------:| 
| $v_f$       |``v_f``      | Field voltage                                | pu-m    |
| $p_m$       |``p_m``      | Mechanical power                             | pu-m    |
        