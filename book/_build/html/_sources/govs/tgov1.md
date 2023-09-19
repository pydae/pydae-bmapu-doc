(tgov1)=
## TGOV1 equivalent

### Model

```{figure} ./tgov1_pydae.svg
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
    "gov":{"type":"tgov1","Droop":0.05,"T_1":1.0,"T_2":1.0,"T_3":1.0,"D_t":0.0,"p_c":0.0,"K_sec":1.0},
...
```


### Inputs

| Variable       | Code         | Description              |  Units |
| :--------------| :----------  | :----------------------- | :-----:| 
| $p_c$          | ``p_c``      | Local reference power    |  pu-m  |    
| $\omega$       | ``omega``    | Machine speed            |  pu    |              
| $p_{agc}$      | ``p_agc``    | AGC power reference      |  pu-s  |  


### Parameters

| Constant   | Code       | pydae name        | Default| Description                               |  Units  |
| :--------- |:---------  |:---------         |-------:| :---------------------------------------- | :------:| 
| $Droop$    | ``Droop``  | ``Droop``         | 0.05   | Permanent droop                           |  pu     | 
| $T_1$      | ``T_1``    | ``T_gov_1_<id>``  | 1      | Steam bowl time constant                  |  s      | 
| $T_2$      | ``T_2``    | ``T_gov_2_<id>``  | 1      | Numerator time constant of T2, T3 block   |  s      | 
| $T_3$      | ``T_3``    | ``T_gov_3_<id>``  | 1      | Reheater time constant                    |  s      | 
 



### Outputs

| Variable   | Code        | Description           |  Units  |
| :--------- | :---------- | :-------------------- |:-------:|     
| $p_m$      | ``p_m``     | Mechanical power      |  pu-m   | 
