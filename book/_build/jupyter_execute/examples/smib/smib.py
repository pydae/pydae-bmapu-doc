#!/usr/bin/env python
# coding: utf-8

# ## SMIB
# 
# Synchronous Machine Infinite Bus (SMIB) system
# 

# ### System building

# In[1]:


from pydae.bmapu import bmapu_builder


# #### System data

# In[2]:


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
         "avr":{'type':'sexs','K_a':200.0,'T_a':0.1,'T_b':1.0,'T_e':0.1,'E_min':-10.0,'E_max':10.0,"v_ref":1.0},
         "pss":{"type":"pss2","K_s3":1.0,"T_wo1":2.0,"T_wo2":2.0,"T_9":0.1,
                "K_s1":17.069,"T_1":0.28,"T_2":0.04,"T_3":0.28,"T_4":0.12,"T_wo3":2.0,"K_s2": 0.158,"T_7":2.0},       
         "gov":{"type":"tgov1","Droop":0.05,"T_1":1.0,"T_2":1.0,"T_3":1.0,"D_t":0.0,"K_sec":0.0,"p_c":0.8},
         "K_delta":0.0}],
"genapes":[{"bus":"2","S_n":1e9,"F_n":50.0,"X_v":0.001,"R_v":0.0,"K_delta":0.001,"K_alpha":1e-6}]
}


# #### System generation and compilation

# In[3]:


grid = bmapu_builder.bmapu(data)
grid.checker()
grid.build('smib')


# ### System analysis and simulation

# In[4]:


import numpy as np
import matplotlib.pyplot as plt
import pydae.grid_tools as gt
import pydae.ssa as ssa
from IPython.core.display import HTML,SVG


# In[5]:


get_ipython().run_line_magic('matplotlib', 'widget')


# #### Initialization

# In[6]:


import smib


# In[7]:


model = smib.model()
model.ini({'p_c_1':1.0},'xy_0.json')


# In[8]:


model.report_x()
model.report_y()


# #### Small signal analysis

# In[9]:


ssa.A_eval(model)
damp = ssa.damp_report(model)
damp.sort_values('Damp').round(2)


# #### Time domain simulation

# In[10]:


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

