(vsc_l_)=
## VSC with coupling inductor

```{figure} ./vsc_l.svg
:height: 100px
:name: vsc_pq


```

$$
p_{out} = p_{in} + \Delta p_r
$$

$$
p_{out} \leq p_{in}
$$

$$
q_{out} = \Delta q_r
$$

$$
q_{out}^{\max} = \sqrt{S_n^2 - p_{out}^2}
$$

$$-q_{out}^{\max} \leq q_{out} \leq q_{out}^{\max}$$

### Example input

```{code} 
...
``"vscs":[{"type":"vsc_pq","bus":"1","p_in":0.5,"S_n":10e6,"K_delta":0.0}],
```


| Variable    | Code       | Description                          |  Units  |
| :---------- | :--------- | :----------------------------------- |:-------:|  
| $S_n$       | ``S_n``    | Nominal power                        | VA      |



### Inputs

| Variable       | Code         | Description              |  Units |
| :--------------| :----------  | :----------------------- | :-----:| 
| $p_s^\star$    | ``p_s_ref``  | Active power reference   |  pu-m  |    
| $p_s^\star$    | ``q_s_ref``  | Reactive power reference |  pu-m  |    

