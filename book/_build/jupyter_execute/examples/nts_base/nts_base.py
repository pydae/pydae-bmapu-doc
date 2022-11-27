#!/usr/bin/env python
# coding: utf-8

# ## NTS base case
# 
# <img src="nts.png" width="600">
# 

# In[1]:


from pydae.bmapu import bmapu_builder


# In[2]:


grid = bmapu_builder.bmapu('nts_base.json')
grid.checker()
grid.build('nts')


# In[ ]:





# In[3]:


import numpy as np
import matplotlib.pyplot as plt
import pydae.grid_tools as gt
import pydae.ssa as ssa
from IPython.core.display import HTML,SVG
import nts


# ### Initialization

# In[14]:


lf = 1.0
params = {'p_c_1':0.935*lf, # generator at bus 1 power reference
          'P_2':-1250e6*lf,'P_3':-4000e6*lf, # loads
          }


model = nts.model()

gt.change_line(model,'2','3',R_pu=0.0,X_pu=0.6,S_mva=100)
model.ini(params,'xy_0.json')
model.save_xy_0('xy_1.json')

S_n_1,S_n_4,p_g_1,p_g_4 = model.get_mvalue(['S_n_1','S_n_4','p_g_1','p_g_4'])
print(f'P_g1 = {p_g_1*S_n_1/1e6:0.0f} MW, P_g4 = {p_g_4*S_n_4/1e6:0.0f} MW')
model.report_y()


# ## Small signal analysis

# In[15]:


ssa.A_eval(model);
ssa.damp_report(model).round(2).sort_values('Damp')


# In[23]:


ssa.plot_eig(model, x_min=-4,x_max=0.1,y_min=0,y_max=1);


# ### Participation factors

# In[24]:


ssa.participation(model)['Mode 27'].abs().round(2).sort_values(ascending=False)


# In[10]:


ssa.participation(model)['Mode 15'].abs().round(2).sort_values(ascending=False)


# ### Mode shapes

# In[25]:


ssa.shape2df(model)
SVG(ssa.plot_shapes(model,mode='Mode 15',    states=['omega_1', 'omega_4']))


# ## Time domain simulation

# In[26]:


model.Dt = 0.01
params.update({'T_b_4':10.0,'v_ref_1':1.0,'v_ref_4':1.0,'K_a_4':200,"Droop_1":1000.0})

model.ini(params,'xy_1.json')

model.run( 1.0,{'v_ref_4':1.0})
model.run( 40.0,{'v_ref_4':1.02})

model.post();


# In[27]:


fig,axes = plt.subplots(nrows=2, sharex=True)
axes[0].plot(model.Time,  model.get_values('p_g_1')*model.get_value('S_n_1')/1e6,label='p_g_1')
#axes[0].plot(model.Time,  model.get_values('p_m_1'),label='p_m_1')

axes[1].plot(model.Time,  model.get_values('V_1'),label='V_1')
axes[1].plot(model.Time,  model.get_values('V_4'),label='V_4')

for ax in axes:
    ax.grid()
    ax.legend()


# In[30]:


fig,axes = plt.subplots(nrows=1, sharex=True)

axes.plot(model.Time,  model.get_values('omega_1'),label='omega_1')
axes.plot(model.Time,  model.get_values('omega_4'),label='omega_4')
axes.grid()
axes.legend()


# In[ ]:




