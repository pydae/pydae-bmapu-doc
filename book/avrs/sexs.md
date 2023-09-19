(sexs)=
## SEXS equivalent

### Model

```{figure} ./sexs.png
:height: 150px
:name: avr-sexs

SEXS AVR model diagram from  [Ippolito](https://www.mdpi.com/1996-1073/14/15/4391/htm)
```

```{figure} ./sexs.svg
:height: 150px
:name: avr-sexs-pydae

SEXS equivalent AVR implemented in pydae 
```

```{warning} 

This is an equivalent model for the SEXS AVR. Some differences must be considered.
```

### Example input

```{code} 
...
 {'type':'sexs','K_a':100.0,'T_a':0.1,'T_b':1.0,'T_e':0.1,'E_min':-10.0,'E_max':10.0}
...
```

The constant $K_{ai}$ (`K_ai`) can be left with its very small default value $K_{ai}$ = 1e-6.



### Inputs

| Variable   | Code        | Description        |  Units |
| :--------- | :---------- | :----------------- | :-----:| 
| $v^\star$  | ``v_ref``   | Voltage reference  |  u     |                  
| $v_s$      | ``v_pss``   | Signal from PSS    |  pu    |              


### Parameters

| Variable   | Code        | Default   | Description    |  Units  |
| :--------- |:----------  |:--------- | :------------- | :------:| 
| $K_a$      | ``K_a``     | 100    | AVR Gain       |  pu-m   | 
| $T_a$      | ``T_a``     | ``T_a``   | Time Constant  |  s      |              
| $T_b$      | ``T_b``     | ``T_b``   | Time Constant  |  s      |             
| $T_e$      | ``T_e``     | ``T_e``   | Time Constant  |  s      |             
| $E_{\max}$ | ``E_max``   | ``E_max`` | Limiter        |  pu-m   |                 
| $E_{\min}$ | ``E_min``   | ``E_min`` | Limiter        |  pu-m   |                  


### Outputs

| Variable   | Code        | Description           |  Units  |
| :--------- | :---------- | :-------------------- |:-------:|     
| $v_f$      | ``v_f``     | Field winding voltage |  pu     | 
