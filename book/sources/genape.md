(genape)=
## Controllable voltage source behind impedance

### Model

```{figure} ./genape.png
:height: 250px
:name: fig-genape

Voltage source behind impedance
```


### Example input

```{code} 
...
``"sources":[{"type":"genape","bus":"1","S_n":100e6,"F_n":50,"X_v":0.01,"R_v":0.0,"K_delta":0.01,"K_alpha":0.01}]
``
...
```



### Inputs

| Variable       | Code         | Description                       |  Units |
| :--------------| :----------  | :-------------------------------- | :-----:| 
| $\omega^\star$ | ``omega_ref``| Local reference power             |  pu-m  |    
| $\alpha$       | ``alpha``    | RoCoF in pu if K_alpha = 1.0      |  pu/s  |              
| $v^\star$      | ``v_ref``    | internal voltage reference        |  pu-s  |  
| $\nu$          | ``rocov``    | RoCoV, Rate of Change of Voltage  |  pu-s  |  




### Parameters

| Variable   | Code       | Description                                                         |  Units  |
| :--------- |:---------  | :------------------------------------------------------------------ | :------:| 
| $S_n$      | ``S_n``    | coupling reactance in pu (base machine S_n)                         |  VA     | 
| $X_v$      | ``X_v``    | coupling reactance in pu (base machine S_n)                         |  pu-m   | 
| $R_v$      | ``R_v``    | coupling resistance in pu (base machine S_n)                        |  pu-m   | 
| $K_{\delta}$| ``K_delta``| if K_delta>0.0 current generator is converted to reference machine  |  -      | 



### Outputs

| Variable   | Code        | Description           |  Units  |
| :--------- | :---------- | :-------------------- |:-------:|     
| $\alpha$   | ``alpha``   | RoCoF in pu           |  pu/s   | 
| $\Delta v$ | ``Dv``      | Voltage incerement    |  pu     | 
| $\theta_v$ | ``theta_v`` | Voltage phase         |  rad    | 
