(pss_kundur_2)=
## PSS Kundur 2 equivalent

### Model

This is an equivalent model for the PSS defined in the book by Kundur at Figure E12.9. 

```{figure} ./pss_kundur_2.svg
:height: 250px
:name: pss_kundur_2

ST1 equivalent AVR implemented in pydae 
```


```{warning} 
Some differences must be considered.
```

### Example input

```{code} 
...
``"pss":{"type":"pss2","K_stab":1.0,"T_wo":10.0,"T_1":1,"T_2":1,"T_3":1,"T_4":1,"V_lim":0.2}, ``
...
```



### Inputs

| Variable   | Code        | pydae name       | Description        |  Units |
| :--------- | :---------- | :----------      | :----------------- | :-----:| 
| $\omega$   | ``omega``   | ``omega_<id>``   | Voltage reference  |  pu    |                  
        


### Parameters

| Constant     | Code        | Description                | pydae name          | Default |  Units  |
| :---------   |:----------  | :-------------             |:---------           |-------: | :------:| 
| $K_{stab}$   | ``K_stab``  | PSS Gain                   | ``K_stab_<id>``     | 1.0     |  pu-m   | 
| $T_{w}$      | ``T_wo``    | Washout time constant      | ``T_w_pss__<id>``   | 10.0    |  s      | 
| $T_{1}$      | ``T_1``     | Time Constant              | ``T_1_pss_<id>``    | 1.0     |  s      | 
| $T_{2}$      | ``T_2``     | Time Constant              | ``T_2_pss_<id>``    | 1.0     |  s      | 
| $T_{3}$      | ``T_3``     | Time Constant              | ``T_3_pss_<id>``    | 1.0     |  s      | 
| $T_{4}$      | ``T_4``     | Time Constant              | ``T_4_pss_<id>``    | 1.0     |  s      | 
| $V_{lim}$    | ``V_lim``   | PSS output limit           | ``V_lim_<id>``      | 0.2     |  pu     |      


### Outputs

| Variable   | Code        | Description           |  Units  |
| :--------- | :---------- | :-------------------- |:-------:|     
| $v_s$      | ``v_s``     |AVR PSS sognal         |  pu     | 
