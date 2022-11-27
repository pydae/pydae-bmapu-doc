#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().run_line_magic('matplotlib', 'widget')


# In[2]:


import numpy as np
import scipy.optimize as sopt
import matplotlib.pyplot as plt
#import pydae.ssa as ssa
#import pydae.grid_tools as gt
import time
import json
#plt.style.use('easyres.mplstyle')


# In[3]:


from pv_plant import pv_plant_class,run,ini


# In[4]:


syst = pv_plant_class()


# In[5]:


t_0 = time.time()
ini(syst.struct,3)
print(time.time()-t_0)


# In[28]:


syst = pv_plant_class()
with open('xy_0_dict.json') as json_file:
    data = json.load(json_file)

for item in data:
    if item in syst.x_list:
        syst.struct[0].x[syst.x_list.index(item)] = data[item]
    if item in syst.y_ini_list:
        syst.struct[0].y_ini[syst.y_ini_list.index(item)] = data[item]     
        
xy_0 = np.vstack([syst.struct[0].x,syst.struct[0].y_ini])[:,0]
syst.xy_prev = xy_0
 


# In[9]:




for it in range(1,12):
    syst.set_value(f'I_max_INV_{it}',20)
    syst.set_value(f'K_p_v_INV_{it}',0.5)
    

syst.initialization_tol = 1e-12

syst.initialize([{}],xy0='prev')


# In[35]:


syst = pv_plant_class()
syst.Dt = 0.001
syst.decimation = 1
syst.update()
syst.xy_prev = xy_0

Dv_r = -0.045
Dq_r = 0.0

for it in range(1,12):
    syst.set_value(f'I_max_INV_{it}',20)
    syst.set_value(f'K_p_v_INV_{it}',0.5)
    

syst.initialization_tol = 1e-8

syst.initialize([{}],xy0='prev')

D_v_r_event_0 = {'t_end': 0.1}
for it in range(1,12):
    D_v_r_event_0.update({f'Dv_r_INV_{it}':-0.0})
    
D_v_r_event_1 = {'t_end':0.25}
for it in range(1,12):
    D_v_r_event_1.update({f'Dv_r_INV_{it}':-0.01})

    

events = [
     D_v_r_event_0,
     D_v_r_event_1
          ]
t_0 = time.time()

syst.run(events)
print(time.time()-t_0)
syst.post();


# In[36]:


plt.close('all')
fig, axes = plt.subplots(nrows=1,ncols=2, figsize=(8, 3), frameon=False, dpi=100, squeeze=False)

#v_POI_a = syst.get_values('v_POI_a_r') + 1j* syst.get_values('v_POI_a_i')
#v_POI_a_m = np.abs(v_POI_a)/38105

axes[0,0].plot(syst.T, syst.get_values('v_m_INV_1'), label="$V_{W1}$ (LV)")
fig.savefig('lctrl_lv.svg')


# In[20]:


#axes[0,0].plot(syst.T, syst.get_values('v_m_W2lv'), label=f"W2")
#axes[0,0].plot(syst.T, syst.get_values('v_m_W3lv'), label=f"W3")
axes[0,0].plot(syst.T, syst.get_values('v_m_W1mv'), label="$V_{W1}$ (MV)")
#axes[0,0].plot(syst.T, syst.get_values('v_m_W2mv'), label=f"W2mv")
#axes[0,0].plot(syst.T, syst.get_values('v_m_W3mv'), label=f"W3mv")
axes[0,0].plot(syst.T, v_POI_a_m, label="$V_{POI}$ (HV)")

axes[0,1].plot(syst.T, get_flow(syst,'POI','GRID').real/1e6, label="$P_{POI}$")  
axes[0,1].plot(syst.T, get_flow(syst,'POI','GRID').imag/1e6, label="$Q_{POI}$")  

y_labels = ['Voltages (pu)', 'Powers (MVA)']
for ax,ylabel in zip(axes.flatten(),y_labels):
    ax.set_ylabel(ylabel)
    ax.grid()
    ax.legend()
    ax.set_xlim([0,0.25])

    ax.set_xlabel('Time (s)')

fig.tight_layout()


# In[27]:


syst.struct[0].g


# In[21]:


syst.struct[0].g[173]


# In[ ]:




