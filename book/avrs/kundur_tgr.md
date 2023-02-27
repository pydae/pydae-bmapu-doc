(kundur_tgr)=
## Kundur TGR AVR equivalent

### Model

```{figure} ./kundur_tgr_book.png
:height: 120px
:name: avr-tgr

AVR-TGR model diagram from  Kundur's Book

```{figure} ./kundur_tgr.svg
:height: 150px
:name: avr-tgr-pydae

Kundur TGR equivalent AVR implemented in pydae 
```

```{warning} 

This is an equivalent model for the Kundur's Book AVR-TGR. Some differences must be considered.
```

### Example input

```{code} 
...
 {'type':'kundur_tgr','K_a':100.0,'T_a':0.1,'T_b':1.0,'T_r':0.1}
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
| $T_r$      | ``T_r``     | Time Constant  |  s      |             
| $K_a$      | ``K_a``     | AVR Gain       |  pu-m   | 
| $T_a$      | ``T_a``     | Time Constant  |  s      |              
| $T_b$      | ``T_b``     | Time Constant  |  s      |                         


### Outputs

| Variable   | Code        | Description           |  Units  |
| :--------- | :---------- | :-------------------- |:-------:|     
| $v_f$      | ``v_f``     | Field winding voltage |  pu     | 
