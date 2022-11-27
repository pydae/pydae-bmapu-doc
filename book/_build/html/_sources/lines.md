# Lines 

Lines can be inserted in three type of parameters

* Serie `R` and `X` in $\Omega$ and shunt `B_s` in in $1/\Omega$
* Serie `R_pu`, `X_pu` and shunt `Bs_pu` in pu on a `S_mva` base.
* Serie `R_km` and `X_km` in $\Omega$/km and shunt `Bs_km` in km$/\Omega$, for a line with a `km` lenght.

## Examples

### Values in $\Omega$ and $1/\Omega$

```
"lines":[{"bus_j":"1", "bus_k":"2", "X":0.05,"R":0.01,"Bs":1e-6}],
```

### Values in pu

```
"lines":[{"bus_j":"1", "bus_k":"2", "X_pu":0.05,"R_pu":0.01,"Bs_pu":1e-6,"S_mva":100.0}],
```

### Values in $\Omega/\text{km}$ and $1/\left(\Omega \text{km}\right)$

```
"lines":[{"bus_j":"2", "bus_k":"3", "X_km":0.4100 ,"R_km":0.0718,"Bs_km":0.271e-6,"km":50}],
```

## Typical values

| :--- | ---: |

| Voltage level (kV)  | R (Ω/km) | X (Ω/km) | B (Ω-1/Km)| Power (MVA)| Lenght (km)|
| :---                | :---     | :---     | :---      | :---       | :---       |
| 400 V               | 0.400    | 0.09     | -         | 0.1        | 1          |
| 20 kV (underground) | 0.270    | 0.12     | -         | 4          | 10         |
| 20 kV               | 0.426    | 0.0      | -         |            |            | 
| 66 kV               | 0.1194   | 0.3856   | 3.386e-6  | 50         | 50         | 
| 132 kV              | 0.0718   | 0.4100   | 2.710e-7  |            |            |
| 220 kV              | 0.0463   | 0.3155   | 3.676e-6  |            |            | 
| 400 kV              | 0.0268   | 0.2766   | 4.59e-6   |            |            | 

