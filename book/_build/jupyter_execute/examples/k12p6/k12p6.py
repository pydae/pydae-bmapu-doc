#!/usr/bin/env python
# coding: utf-8

# ## Kundur example 12.6

# In[1]:


from pydae.bmapu import bmapu_builder


# In[2]:


grid = bmapu_builder.bmapu('k12p6.json')
grid.checker()
grid.build('k12p6')


# In[5]:


import numpy as np
import matplotlib.pyplot as plt
import pydae.grid_tools as gt
import pydae.ssa as ssa
from IPython.core.display import HTML,SVG
from pydae.svg_tools import svg
import scipy.optimize as sopt
get_ipython().run_line_magic('config', "InlineBackend.figure_formats = ['svg']")


# In[7]:


SVG('sp_k12p6.svg')


# In[8]:


import k12p6 


# ### Initialization

# In[12]:


model = k12p6.model()

K_delta = 0.001
K_sec = 0.1
K_a = 200.0
T_r = 0.02
D = 0.5

params = {'P_7':-967e6,'P_9':-1_767e6,'Q_7':100e6,'Q_9':250e6,
                  'K_delta_1':K_delta,'K_delta_2':0,
                  'K_delta_3':0,'K_delta_4':0,
                  'K_a_1':K_a,'K_a_2':K_a,'K_a_3':K_a,'K_a_4':K_a,
                  #'T_r_1':T_r,'T_r_2':T_r,'T_r_3':T_r,'T_r_4':T_r,
                  'p_c_1':701.4/900,'p_c_2':701.4/900,'p_c_4':701.4/900,
                  #'v_ref_1':1.03,'v_ref_2':1.01,'v_ref_3':1.03,'v_ref_4':1.01,
                     'K_sec_1':0,'K_sec_2':0,'K_sec_3':K_sec,'K_sec_4':0,
                  'K_imw_1':0.01, 'K_imw_2':0.01,'K_imw_3':0.0, 'K_imw_4':0.01,
                  'D_1':D,'D_2':D,'D_3':D,'D_4':D
                    }

model.ini(params,'xy_0.json')


# ### Small signal analysis

# #### Eigenvalues

# In[27]:


ssa.A_eval(model)
damp = ssa.damp_report(model)
damp.sort_values('Damp').round(2)


# In[28]:


ssa.plot_eig(model,x_min=-1,x_max=0.01,y_min=0,y_max=1.5);


# #### Participation factors

# In[29]:


ssa.participation(model)['Mode 13'].abs().round(2).sort_values(ascending=False)


# ### Mode shapes

# In[32]:


ssa.shape2df(model).loc['Mode 14'][[f'omega_{it+1}' for it in range(4)]]


# In[35]:


svg_string = ssa.plot_shapes(model,mode='Mode 13',states=[f'omega_{it+1}' for it in range(4)])
SVG(svg_string)


# ### Time domain simulation

# In[40]:


model = k12p6.model()

model.ini(params,'xy_0.json')
model.run(1.0,{'v_ref_1': 1.03})
model.run(10.0,{'v_ref_1': 1.03*1.05});
model.post();
fig,axes = plt.subplots()
axes.plot(model.Time,model.get_values('omega_1'),label='omega_1')
axes.plot(model.Time,model.get_values('omega_2'),label='omega_2')
axes.plot(model.Time,model.get_values('omega_3'),label='omega_3')
axes.plot(model.Time,model.get_values('omega_4'),label='omega_4')
axes.legend()


# In[ ]:




