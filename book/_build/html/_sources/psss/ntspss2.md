(ntspss2)=
## PSS2 equivalent

### Model

```{figure} ./ntspss2.png
:height: 250px
:name: pss-ntspss2

ST1 equivalent AVR implemented in pydae 
```


```{warning} 

This is an equivalent model for the PSS2 PSS. Some differences must be considered.
```

### Example input

```{code} 
...
``"pss":{"type":"pss2","K_s3":1.0,"T_wo1":2.0,"T_wo2":2.0,"T_9":0.1,       "K_s1":17.069,"T_1":0.28,"T_2":0.04,"T_3":0.28,"T_4":0.12,"T_wo3":2.0,"K_s2": 0.158,"T_7":2.0}, ``
...
```



### Inputs

| Variable   | Code        | Description        |  Units |
| :--------- | :---------- | :----------------- | :-----:| 
| $\omega$  | ``omega``   | Voltage reference  |  pu     |                  
| $p_g$      | ``p_g``     | Signal from PSS    |  pu-m    |              


### Parameters

| Variable   | Code        | Description    |  Units  |
| :--------- |:----------  | :------------- | :------:| 
| $K_{s1}$      | ``K_s1``     | PSS Gain       |  pu-m   | 
                


### Outputs

| Variable   | Code        | Description           |  Units  |
| :--------- | :---------- | :-------------------- |:-------:|     
| $v_s$      | ``v_s``     | Field winding voltage |  pu     | 
