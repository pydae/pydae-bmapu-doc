#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import sympy as sym
import json
import sympy as sym
import pydae.build_cffi as db
from pydae.grid_bpu import bpu


# In[2]:


file_path = 'k12p6.json'
grid = bpu(file_path)


# In[3]:


g_list = grid.dae['g'] 
h_dict = grid.dae['h_dict']
f_list = grid.dae['f']
x_list = grid.dae['x']
params_dict = grid.dae['params_dict']

sys = {'name':'k12p6',
       'params_dict':params_dict,
       'f_list':f_list,
       'g_list':g_list,
       'x_list':x_list,
       'y_ini_list':grid.dae['y_ini'],
       'y_run_list':grid.dae['y_run'],
       'u_run_dict':grid.dae['u_run_dict'],
       'u_ini_dict':grid.dae['u_ini_dict'],
       'h_dict':h_dict}


bldr = db.builder(sys);
bldr.build()


# In[ ]:




