(ntsst1)=
## ST1 equivalent

### Model

```{figure} ./ntsst1.svg
:height: 250px
:name: avr-ntsst1

ST1 equivalent AVR implemented in pydae 
```


```{warning} 

This is an equivalent model for the ST1 AVR. Some differences must be considered.
```

### Example input

```{code} 
...
``"avr":{"type":"ntsst1","K_a":200.0,"T_c":1.0,"T_b":10.0,"v_ref":1.0},``
...
```



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
