#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pydae.bmapu import bmapu_builder


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
         "avr":{'type':'sexs','K_a':100.0,'T_a':0.1,'T_b':1.0,'T_e':0.1,'E_min':-10.0,'E_max':10.0,"v_ref":1.0},
         "pss":{"type":"pss2","K_s3":1.0,"T_wo1":2.0,"T_wo2":2.0,"T_9":0.1,
                "K_s1":17.069,"T_1":0.28,"T_2":0.04,"T_3":0.28,"T_4":0.12,"T_wo3":2.0,"K_s2": 0.158,"T_7":2.0},       
         "gov":{"type":"tgov1","Droop":0.05,"T_1":1.0,"T_2":1.0,"T_3":1.0,"D_t":0.0,"K_sec":0.0,"p_c":0.8},
         "K_delta":0.0}],
"genapes":[{"bus":"2","S_n":1e9,"F_n":50.0,"X_v":0.001,"R_v":0.0,"K_delta":0.001,"K_alpha":1e-6}]
}


# In[3]:


grid = bmapu_builder.bmapu(data)
grid.checker()
grid.build('smib')


# In[ ]:




