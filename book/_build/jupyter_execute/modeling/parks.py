#!/usr/bin/env python
# coding: utf-8

# ### Park transform

# In[1]:


import sympy as sym
import numpy as np


# #### Phasor definition

# In[2]:


X_m =  1.0  # phasor module
X_a =  0.2  # phasor angle 

X = X_m*np.exp(1j*X_a)

print(f'X_m = {X_m:0.3f}, X_a = {X_a:0.3f}')


# #### Phasor to generic DQ

# In[3]:


r = X.real   # X_m*cos(X_a)
i = X.imag   # X_m*sin(X_a)

D = i
Q = r

print(f'D = {D:0.3f}, Q = {Q:0.3f}')


# ### Park transform DQ to dq with angle $\delta$

# In[4]:


delta = 0.1

d = D * np.cos(delta) - Q * np.sin(delta)   
q = D * np.sin(delta) + Q * np.cos(delta)

print(f'd = {d:0.3f}, q = {q:0.3f}')


# #### Inverse Park transform dq to DQ with angle $\delta$

# In[5]:


D =  d * np.cos(delta) + q * np.sin(delta)   
Q = -d * np.sin(delta) + q * np.cos(delta) 

print(f'D = {D:0.3f}, Q = {Q:0.3f}')


# #### From DQ to phasor

# In[6]:


i = D
r = Q
print(f'r = {r:0.3f}, i = {i:0.3f}')

P_m = np.sqrt(r**2 + i**2)
P_a = np.arctan2(i,r)
print(f'P_m = {P_m:0.3f}, P_a = {P_a:0.3f}')


# In[ ]:





# In[7]:


re,im = sym.symbols('d,q', real = True)
D,Q = sym.symbols('D,Q', real = True)
delta = sym.Symbol('delta', real = True)


# In[ ]:





# In[ ]:





# ### Park from milano
# 
# $$
# d = X_m \sin\left(\delta - X_a\right)  \\
# q = X_m \cos\left(\delta - X_a\right)
# $$

# In[8]:


d = X_m*np.sin(delta - X_a) 
q = X_m*np.cos(delta - X_a) 

print(f'd = {d:0.3f}, q = {q:0.3f}')


# In[ ]:


r = X.real   # X_m*cos(X_a)
i = X.imag   # X_m*sin(X_a)

print(f'r = {r:0.3f}, i = {i:0.3f}')

D = i
Q = r

print(f'D = {D:0.3f}, Q = {Q:0.3f}')

# Park DQ to dq
d = -D * np.cos(delta) + Q * np.sin(delta)   
q =  D * np.sin(delta) + Q * np.cos(delta)

print(f'd = {d:0.3f}, q = {q:0.3f}')

# Inverse Park dq to DQ, P = inv(P)
D = -d * np.cos(delta) + q * np.sin(delta)   
Q =  d * np.sin(delta) + q * np.cos(delta) 


print(f'D = {D:0.3f}, Q = {Q:0.3f}')

i = D
r = Q

print(f'r = {r:0.3f}, i = {i:0.3f}')


# ### Parks symbolic

# In[ ]:


delta = sym.Symbol('delta', real = True)

P = sym.Matrix([[-sym.cos(delta), sym.sin(delta)],
                [ sym.sin(delta), sym.cos(delta)]])
P


# In[ ]:


sym.simplify(P.inv())


# In[ ]:





# In[ ]:


### RL circuit


# In[ ]:


v_1_r,v_1_i = sym.symbols('v_1_r,v_1_i', real = True)
v_2_r,v_2_i = sym.symbols('v_2_r,v_2_i', real = True)
i_1_r,i_1_i = sym.symbols('i_1_r,i_1_i', real = True)
R,X = sym.symbols('R,X', real = True)

v_1 = v_1_r + 1j*v_1_i
v_2 = v_2_r + 1j*v_2_i
i_1 = i_1_r + 1j*i_1_i
Z = R + 1j*X

eq = v_1 - Z*i_1 - v_2 

ri = sym.Matrix([[ sym.re(eq)],
                 [ sym.im(eq)]])

ri


# In[ ]:


v_1_D,v_1_Q = sym.symbols('v_1_D,v_1_Q', real = True)
v_2_D,v_2_Q = sym.symbols('v_2_D,v_2_Q', real = True)
i_1_D,i_1_Q = sym.symbols('i_1_D,i_1_Q', real = True)
R,X = sym.symbols('R,X', real = True)

v_1 = v_1_Q + 1j*v_1_D
v_2 = v_2_Q + 1j*v_2_D
i_1 = i_1_Q + 1j*i_1_D
Z = R + 1j*X

eq = v_1 - Z*i_1 - v_2 

DQ = sym.Matrix([[ sym.re(eq)],
                 [ sym.im(eq)]])

DQ


# In[ ]:


eq = v_1 - Z*i_1 - v_2 


# In[ ]:


# eq = v_1DQ - Z*i_1DQ - v_2DQ
# eq = Pinv*v_1dq - Z*Pinv*i_1dq - Pinv*v_2dq
# eq = P*(Pinv*v_1dq - Z*Pinv*i_1dq - Pinv*v_2dq)
# eq = P*Pinv*v_1dq - P*Z*Pinv*i_1dq - P*Pinv*v_2dq)
# eq = v_1dq - P*Z*Pinv*i_1dq - v_2dq)

v_1_d,v_1_q = sym.symbols('v_1_d,v_1_q', real = True)
v_2_d,v_2_q = sym.symbols('v_2_d,v_2_q', real = True)
i_1_d,i_1_q = sym.symbols('i_1_d,i_1_q', real = True)
R,X = sym.symbols('R,X', real = True)
Z_matrix = sym.Matrix([[-R,  X],
                       [-X, -R]])

v_1_dq = sym.Matrix([[v_1_d],
                     [v_1_q]])

v_2_dq = sym.Matrix([[v_2_d],
                     [v_2_q]])

i_1_dq = sym.Matrix([[i_1_d],
                     [i_1_q]])

eq = v_1_dq - (P*Z_matrix*P.inv())*i_1_dq - v_2_dq
sym.simplify(eq)


# In[ ]:





# In[ ]:





# In[ ]:


R_s = 0.02
X_s = 0.2

R_v = 0.01
X_v = 0.1

Z_s = R_s + 1j*X_s
Z_v = R_v + 1j*X_v

theta_s = 0.0
V_s = 1.0
v_s_ri = V_s*np.exp(1j*theta_s)

phi_s = 0.0
I_s = 0.5
i_s_ri = V_s*np.exp(1j*(theta_s+phi_s))

v_t_ri = v_s_ri + Z_s*i_s_ri

e_v_ri = v_t_ri + Z_v*i_s_ri

print(e_v_ri)


# In[ ]:





# In[ ]:


v_si = v_s_ri.imag
v_sr = v_s_ri.real
i_si = i_s_ri.imag
i_sr = i_s_ri.real

v_ti =  R_s*i_si + X_s*i_sr + v_si  
v_tr =  R_s*i_sr - X_s*i_si + v_sr 

e_vi =  R_v*i_si + X_v*i_sr + v_ti  
e_vr =  R_v*i_sr - X_v*i_si + v_tr 

theta_v = np.arctan2(e_vi,e_vr)


print(e_vr,e_vi)


# In[ ]:


v_si = v_s_ri.imag
v_sr = v_s_ri.real
i_si = i_s_ri.imag
i_sr = i_s_ri.real

# 0 = v_ti - R_s*i_si - X_s*i_sr - v_si
# 0 = v_tr - R_s*i_sr + X_s*i_si - v_sr 
v_ti =  R_s*i_si + X_s*i_sr + v_si  
v_tr =  R_s*i_sr - X_s*i_si + v_sr 

i_sD = i_si
i_sQ = i_sr
v_tD = v_ti
v_tQ = v_tr

e_vD =  R_v*i_sD + X_v*i_sQ + v_tD  
e_vQ =  R_v*i_sQ - X_v*i_sD + v_tQ 


delta = theta_v

v_td = v_tD * np.cos(delta) - v_tQ * np.sin(delta)   
v_tq = v_tD * np.sin(delta) + v_tQ * np.cos(delta)

i_sd = i_sD * np.cos(delta) - i_sQ * np.sin(delta)   
i_sq = i_sD * np.sin(delta) + i_sQ * np.cos(delta)

# 0 = e_vd - R_v*i_sd - X_v*i_sq - v_td  
# 0 = e_vq - R_v*i_sq + X_v*i_sd - v_tq 
e_vd =  R_v*i_sd + X_v*i_sq + v_td  
e_vq =  R_v*i_sq - X_v*i_sd + v_tq 

#print(e_vd,e_vq)

e_vD =  e_vd * np.cos(delta) + e_vq * np.sin(delta)   
e_vQ = -e_vd * np.sin(delta) + e_vq * np.cos(delta) 

e_vi = e_vD
e_vr = e_vQ

print(e_vr,e_vi)


# In[ ]:


e_vd


# In[ ]:


e_vq


# In[ ]:




