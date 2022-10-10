(ntsst4)=
## ST4 equivalent

### Model

```{figure} ./ntsst4.png
:height: 250px
:name: avr-ntsst4

ST4 equivalent AVR implemented in pydae 
```


```{warning} 

This is an equivalent model for the ST4 AVR. Some differences must be considered.
```

### Example input

```{code} 
...
 "avr":{"type":"ntsst4","K_pr":3.15,"K_ir":3.15,"V_rmax":1.0,"V_rmin":-0.87,"T_a":0.02,"K_pm":1.0,"K_im":0.0,"K_p": 6.5,"v_ref":1.0}
...
```

The constant $K_{ai}$ (`K_ai`) can be left with its very small default value $K_{ai}$ = 1e-6.



### Inputs

| Variable   | Code        | Description        |  Units |
| :--------- | :---------- | :----------------- | :-----:| 
| $v^\star$  | ``v_ref``   | Voltage reference  |  u     |                  
| $v_s$      | ``v_pss``   | Signal from PSS    |  pu    |              


### Parameters

| Variable   | Code        | Description    |  Units  |
| :--------- |:----------  | :------------- | :------:| 
| $K_a$      | ``K_a``     | AVR Gain       |  pu-m   | 
                


### Outputs

| Variable   | Code        | Description           |  Units  |
| :--------- | :---------- | :-------------------- |:-------:|     
| $v_f$      | ``v_f``     | Field winding voltage |  pu     | 
