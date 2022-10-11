#!/usr/bin/env python
# coding: utf-8

# # NTS base case

# In[1]:


from pydae.bmapu import bmapu_builder


# In[2]:


grid = bmapu_builder.bmapu('nts.json')
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


# ## Initialization

# In[29]:


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

# In[5]:


ssa.A_eval(model);
ssa.damp_report(model).round(2).sort_values('Damp')


# In[6]:


fig,axes = plt.subplots(nrows=1)

df = ssa.damp_report(model)
reals = df['Real'].values
imags = df['Imag'].values
axes.plot(reals,  imags,'o',color='b')
    
axes.set_xlim([-10,1.0])
axes.set_ylim([-6,6])

nts_data = np.genfromtxt('nts_points.csv', delimiter=',')
axes.plot(nts_data[:,0],  nts_data[:,1],'.',alpha=1,color='r')

axes.grid()


# In[7]:


ssa.participation(model)['Mode 27'].abs().round(2).sort_values(ascending=False)


# In[8]:


ssa.participation(model)['Mode 15'].abs().round(2).sort_values(ascending=False)


# In[9]:


ssa.shape2df(model)
SVG(ssa.plot_shapes(model,mode='Mode 15',    states=['omega_1', 'omega_4']))


# ## Time domain simulation

# In[42]:


model.Dt = 0.01
params.update({'T_b_4':10.0,'v_ref_1':1.0,'v_ref_4':1.0,'K_a_4':200,"Droop_1":1000.0})

model.ini(params,'xy_1.json')

model.run( 1.0,{'v_ref_4':1.0})
model.run( 40.0,{'v_ref_4':1.02})

model.post();


# In[46]:


fig,axes = plt.subplots(nrows=2, sharex=True)
axes[0].plot(model.Time,  model.get_values('p_g_1')*model.get_value('S_n_1')/1e6,label='p_g_1')
#axes[0].plot(model.Time,  model.get_values('p_m_1'),label='p_m_1')

axes[1].plot(model.Time,  model.get_values('V_1'),label='V_1')
axes[1].plot(model.Time,  model.get_values('V_4'),label='V_4')

for ax in axes:
    ax.grid()
    ax.legend()

