(tgov1)=
## TGOV1 equivalent

### Model

```{figure} ./tgov1.svg
:height: 250px
:name: gov-tgov1

TGOV1 equivalent GOV implemented in pydae 
```


```{warning} 

This is an equivalent model for the TGOV1 governor. Some differences must be considered.
```

### Example input

```{code} 
...
``"avr":{"type":"ntsst1","K_a":200.0,"T_c":1.0,"T_b":10.0,"v_ref":1.0},``
...
```



### Inputs

| Variable       | Code         | Description              |  Units |
| :--------------| :----------  | :----------------------- | :-----:| 
| $p_c$          | ``p_c``      | Local reference power    |  pu-m  |    
| $\omega$       | ``omega``    | Machine speed            |  pu    |              
| $\omega_{coi}$ | ``omega_coi``| Machine speed            |  pu    |              
| $p_{agc}$      | ``p_agc``    | AGC power reference      |  pu-s  |  

### Parameters

| Variable   | Code       | Description                               |  Units  |
| :--------- |:---------  | :---------------------------------------- | :------:| 
| $K_{sec}$  | ``K_sec``  | Secondary frequency enable=1, disable = 0 |  bool   | 
                


### Outputs

| Variable   | Code        | Description           |  Units  |
| :--------- | :---------- | :-------------------- |:-------:|     
| $p_m$      | ``p_m``     | Mechanical power      |  pu-m   | 
