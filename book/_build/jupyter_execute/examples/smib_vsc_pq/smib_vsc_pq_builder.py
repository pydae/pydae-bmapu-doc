#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pydae.build_cffi as db
from pydae.bmapu import bmapu_builder


# In[13]:


import pydae.grid_tools as gt


# In[14]:


grid = bmapu_builder.bmapu('smib_vsc_pq.json')
grid.checker()
grid.build('smib_vsc_pq')


# In[ ]:




