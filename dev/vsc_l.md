(vscpq)=
## VSC in PQ mode

```{figure} ./vsc_pq.svg
:height: 100px
:name: vsc_pq

VSC in PQ mode with saturation 
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
