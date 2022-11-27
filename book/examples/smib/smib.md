---
jupytext:
  formats: ipynb,md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.14.1
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

## SMIB

Synchronous Machine Infinite Bus (SMIB) system

+++

### System building

```{code-cell} ipython3
from pydae.bmapu import bmapu_builder
```

#### System data

```{code-cell} ipython3
data = {
"sys":{"name":"smib","S_base":100e6, "K_p_agc":0.0,"K_i_agc":0.0,"K_xif":0.01},       
"buses":[{"name":"1", "P_W":0.0,"Q_var":0.0,"U_kV":20.0},
         {"name":"2", "P_W":0.0,"Q_var":0.0,"U_kV":20.0}
        ],
"lines":[{"bus_j":"1", "bus_k":"2", "X_pu":0.05,"R_pu":0.01,"Bs_pu":1e-6,"S_mva":100.0}],
"syns":[
      {"bus":"1","S_n":100e6,
         "X_d":1.8,"X1d":0.3, "T1d0":8.0,    
         "X_q":1.7,"X1q":0.55,"T1q0":0.4,  
         "R_a":0.01,"X_l": 0.2, 
         "H":5.0,"D":1.0,
         "Omega_b":314.1592653589793,"omega_s":1.0,"K_sec":0.0,
         "avr":{"type":"kundur_tgr","K_a":200,"T_r":0.01,"E_fmin":-5,"E_fmax":10.0,"T_a":1,"T_b":10,"v_ref":1.03},
         "gov":{"type":"agov1","Droop":0.05,"T_1":1.0,"T_2":2.0,"T_3":10.0, "p_c":0.8,"omega_ref":1.0, "K_imw":0.0},
         "pss":{"type":"pss_kundur_2","K_stab":20, "T_1":0.05, "T_2":0.02, "T_3":3.0, "T_4":5.4, "T_w":10.0},      
         "gov":{"type":"tgov1","Droop":0.05,"T_1":1.0,"T_2":1.0,"T_3":1.0,"D_t":0.0,"K_sec":0.0,"p_c":0.8},
         "K_delta":0.0}],
"genapes":[{"bus":"2","S_n":1e9,"F_n":50.0,"X_v":0.001,"R_v":0.0,"K_delta":0.001,"K_alpha":1e-6}]
}
```

#### System generation and compilation

```{code-cell} ipython3
grid = bmapu_builder.bmapu(data)
grid.checker()
grid.build('smib')
del grid # just to don't have a large ipynb file
```

### System analysis and simulation

```{code-cell} ipython3
import numpy as np
import matplotlib.pyplot as plt
import pydae.grid_tools as gt
import pydae.ssa as ssa
from IPython.core.display import HTML,SVG
%matplotlib inline
import matplotlib_inline
matplotlib_inline.backend_inline.set_matplotlib_formats('svg')
```

#### Initialization

```{code-cell} ipython3
import smib
```

```{code-cell} ipython3
model = smib.model()
model.ini({'p_c_1':1.0,'T_b_1':1.0},'xy_0.json')
```

```{code-cell} ipython3
model.report_x()
model.report_y()
```

#### Small signal analysis

```{code-cell} ipython3
ssa.A_eval(model)
damp = ssa.damp_report(model)
damp.sort_values('Damp').round(2)
```

#### Time domain simulation

```{code-cell} ipython3
model = smib.model()
model.Dt = 0.01
model.decimation = 1
model.ini({'v_ref_1':1.0, 'K_a_1':200.0},'xy_0.json')
model.run( 1.0,{})
model.run(30.0,{'v_ref_1':1.05})
model.post();

fig,axes = plt.subplots(nrows=3)

axes[0].plot(model.Time,  model.get_values('V_1'),label='V_1')

axes[1].plot(model.Time,  model.get_values('p_g_1'),label='p_g_1')
axes[1].plot(model.Time,  model.get_values('q_g_1'),label='q_g_1')

axes[2].plot(model.Time,  model.get_values('omega_1'),label='omega_1')

for ax in axes:
    ax.legend()
    ax.grid()
    ax.set_xlim([0,20])
ax.set_xlabel('Time (s)')
fig.tight_layout()
```

```{code-cell} ipython3
del model
```

```{code-cell} ipython3

```

```{code-cell} ipython3

```

```{code-cell} ipython3

```
