#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install --upgrade pydae')


# In[2]:


import numpy as np
import matplotlib.pyplot as plt
import pydae.grid_tools as gt
import pydae.ssa as ssa
from IPython.core.display import HTML
from pydae.svg_tools import svg
import scipy.optimize as sopt
get_ipython().run_line_magic('config', "InlineBackend.figure_formats = ['svg']")


# In[3]:


from IPython.display import SVG


# ## Sistema ejemplo Kundur 12.6

# In[4]:


SVG('https://raw.githubusercontent.com/pydae/pydae/master/examples/grids/k12p6/sp_k12p6.svg')


# ## Initialization

# In[5]:


from pydae.systems.atydse.k12p6 import k12p6_class
grid = k12p6_class()


# In[6]:


xy_0_dict = {
"V_1":1.0,"V_2":1.0,"V_3":1.0,"V_4":1.0,
"V_5":1.0,"V_6":1.0,"V_7":1.0,"V_8":1.0,
"V_9":1.0,"V_10":1.0,"V_11":1.0
}


# In[7]:


K_delta = 0.001
K_sec = 0.01
K_a = 150.0
T_r = 0.02
D = 1
grid.initialize([{'P_7':-967e6,'P_9':-1_767e6,'Q_7':100e6,'Q_9':250e6,
                  'K_delta_1':K_delta,'K_delta_2':K_delta,
                  'K_delta_3':K_delta,'K_delta_4':K_delta,
                  'K_a_1':K_a,'K_a_2':K_a,'K_a_3':K_a,'K_a_4':K_a,
                  'T_r_1':T_r,'T_r_2':T_r,'T_r_3':T_r,'T_r_4':T_r,
                  'p_c_1':700/900,'p_c_2':700/900,'p_c_4':700/900,
                  'v_ref_1':1.03,'v_ref_2':1.01,'v_ref_3':1.03,'v_ref_4':1.01,
                  'K_sec_1':0,'K_sec_2':0,'K_sec_3':K_sec,'K_sec_4':0,
                  'D_1':D,'D_2':D,'D_3':D,'D_4':D}],
                   xy_0_dict,compile=True)


# In[8]:


A = ssa.eval_A(grid)
damp = ssa.damp_report(grid)
damp


# In[9]:


ssa.plot_eig(grid,x_min=-1,x_max=0.01,y_min=0,y_max=1.5);


# In[10]:


ssa.participation(grid).abs().round(2)['Mode 11']


# In[11]:


ssa.shape2df(grid).loc['Mode 11'][['omega_1','omega_2','omega_3','omega_4']]


# In[12]:


svg_string = ssa.plot_shapes(grid,mode='Mode 13',states=[f'omega_{it+1}' for it in range(4)])
SVG(svg_string)


# ## Simulación

# In[13]:


K_delta = 0.001
K_sec = 0.01
K_a = 150.0
T_r = 0.02
D = 1
grid.initialize([{'P_7':-967e6,'P_9':-1_767e6,'Q_7':100e6,'Q_9':250e6,
                  'K_delta_1':K_delta,'K_delta_2':K_delta,
                  'K_delta_3':K_delta,'K_delta_4':K_delta,
                  'K_a_1':K_a,'K_a_2':K_a,'K_a_3':K_a,'K_a_4':K_a,
                  'T_r_1':T_r,'T_r_2':T_r,'T_r_3':T_r,'T_r_4':T_r,
                  'p_c_1':700/900,'p_c_2':700/900,'p_c_4':700/900,
                  'v_ref_1':1.03,'v_ref_2':1.01,'v_ref_3':1.03,'v_ref_4':1.01,
                  'K_sec_1':0,'K_sec_2':0,'K_sec_3':K_sec,'K_sec_4':0,
                  'D_1':D,'D_2':D,'D_3':D,'D_4':D}],
                   xy_0_dict,compile=True)


# In[14]:


grid.simulate([
         {'t_end': 1.0,'v_ref_1': 1.03},
         {'t_end':15.0,'v_ref_1': 1.03*1.05}],'prev');


# In[15]:


fig,axes = plt.subplots()
axes.plot(grid.T,grid.get_values('omega_1'),label='omega_1')
axes.plot(grid.T,grid.get_values('omega_2'),label='omega_2')
axes.plot(grid.T,grid.get_values('omega_3'),label='omega_3')
axes.plot(grid.T,grid.get_values('omega_4'),label='omega_4')
axes.legend()


# ## PSS
# 
# Este es el diseño

# In[16]:


grid = k12p6_class()

K_delta = 0.001
K_sec = 0.01
K_a = 150.0
T_r = 0.02
D = 1
grid.initialize([{'Dt':0.01,'decimation':1,
                      'P_7':-967e6,'P_9':-1_767e6,'Q_7':100e6,'Q_9':250e6,
                  'K_delta_1':K_delta,'K_delta_2':K_delta,
                  'K_delta_3':K_delta,'K_delta_4':K_delta,
                  'K_a_1':K_a,'K_a_2':K_a,'K_a_3':K_a,'K_a_4':K_a,
                  'T_r_1':T_r,'T_r_2':T_r,'T_r_3':T_r,'T_r_4':T_r,
                  'p_c_1':700/900,'p_c_2':700/900,'p_c_4':700/900,
                  'v_ref_1':1.03,'v_ref_2':1.01,'v_ref_3':1.03,'v_ref_4':1.01,
                  'v_pss_1':0,'v_pss_3':0,
                  'K_sec_1':0,'K_sec_2':0,'K_sec_3':K_sec,'K_sec_4':0,
                  'D_1':D,'D_2':D,'D_3':D,'D_4':D}],
                   xy_0_dict,compile=True)

grid.simulate([
         {'t_end': 1.0,'v_ref_1': 1.03, 
         #'H_1':1e8,'H_2':1e8,'H_3':1e8,'H_4':1e8
         },
         {'t_end':15.0,'v_ref_1': 1.03*1.05}],'prev');


# In[17]:


fig,axes = plt.subplots()
axes.plot(grid.T,grid.get_values('V_1'),label='V_1')
axes.set_xlim((0,2))
axes.legend()


# In[18]:


V_1_ini = grid.get_values('V_1')[0]
V_1_end = grid.get_values('V_1')[-1]
ΔV_1 = V_1_end - V_1_ini
ΔV_1_e = (1-1/np.e)*ΔV_1
V_1_e = ΔV_1_e + V_1_ini
idx = np.argmax(grid.get_values('V_1')>V_1_e)
Tau = grid.T[idx] -1
Tau


# In[19]:


freq_Hz = 0.5  # frecuencia del modo a amortiguar
w = 2*np.pi*freq_Hz
phi_sm = np.angle(1/(Tau*1j*w+1))  # fase del modelo v_ref -> V econtrado para la frequencia w
T_2 = 0.1 # se deja T_2 con un valor fijo

T_wo = 5.0  # constante de tiempo del washout
phi_wo = np.angle(T_wo*1j*w/(T_wo*1j*w+1))  # fase del washout para la frequencia w
gain_wo = np.abs(T_wo*1j*w/(T_wo*1j*w+1))   # ganancia del washout para la frequencia w

def res(x):  # función T_1 -> fase del compensador + fase del generador y sistema de excitación + fase washout
    T_1 = x
    phi = np.angle((T_1*1j*w+1)/(T_2*1j*w+1))
    return phi + phi_sm + phi_wo

T_1 = sopt.newton(res,0.1)[0]   # solución por medio de newton raphson

gain_l = np.abs((T_1*1j*w+1)/(T_2*1j*w+1)) 
gain_l

gain_p = np.abs((1)/(Tau*1j*w+1))
gain_p

gain = gain_wo*gain_l*gain_p

print(f'T_1 = {T_1:0.2f} s')
print(f'T_2 = {T_2:0.2f} s')


# In[20]:


Δt = 0.05  # latencia del control (cada cuanto se ejecuta el controlador)
grid_pss = k12p6_class()
times = np.arange(0,15,Δt)   # tiempos para los cuales se ejecutará el control 
                             # (en este caso la simulación sera de 15 s)

K_delta = 0.001
K_sec = 0.01
#K_a = 20.0
T_r = 0.02
D = 1
grid_pss.initialize([{'Dt':0.01,'decimation':1,
                      'P_7':-967e6,'P_9':-1_767e6,'Q_7':100e6,'Q_9':250e6,
                  'K_delta_1':K_delta,'K_delta_2':K_delta,
                  'K_delta_3':K_delta,'K_delta_4':K_delta,
                  'K_a_1':K_a,'K_a_2':K_a,'K_a_3':K_a,'K_a_4':K_a,
                  'T_r_1':T_r,'T_r_2':T_r,'T_r_3':T_r,'T_r_4':T_r,
                  'p_c_1':700/900,'p_c_2':700/900,'p_c_4':700/900,
                  'v_ref_1':1.03,'v_ref_2':1.01,'v_ref_3':1.03,'v_ref_4':1.01,
                  'v_pss_1':0,'v_pss_3':0,
                  'K_sec_1':0,'K_sec_2':0,'K_sec_3':K_sec,'K_sec_4':0,
                  'D_1':D,'D_2':D,'D_3':D,'D_4':D}],
                   xy_0_dict,compile=True)

# del estado inicial se guardan las entradas o variables necesarias
v_ref_1_0 = grid_pss.get_value('v_ref_1') # se guarda la tensión de excitación inicial
p_m_1_0 = grid_pss.get_value('p_m_1') # se guarda la tensión de excitación inicial
omega_1_0 = grid_pss.get_value('omega_1') # se guarda la tensión de excitación inicial
omega_3_0 = grid_pss.get_value('omega_3') # se guarda la tensión de excitación inicial

# diseño del control:
## PSS
K_stab_1,K_stab_3 = 50.0/gain,50.0/gain
x_l_1,x_l_3 = 0.0,0.0
T_1_1,T_1_3 = T_1,T_1
T_2_1,T_2_3 = 0.1,0.1
x_wo_1,x_wo_3 = 0,0
T_wo_1,T_wo_3 = T_wo,T_wo
V_s = 0*times
U_l = 0*times

it = 0
for t in times:
    
    # perturbaciones o cambios de referencia
    v_ref_1 = v_ref_1_0
    if t>1.0: # se aplica un cambio para t = 1 s 
        #p_m = 1.2*p_m_0  # se propone como nuevo valor de potencia de un 20% más que el valor inicial
        v_ref_1 = 1.2*v_ref_1_0
    
    # medición de la tensión en terminales
    omega_1 = grid_pss.get_value('omega_1')
    omega_3 = grid_pss.get_value('omega_3')
    
    # Ley de control:
    ## PSS 1
    u_l_1 = (omega_1 - omega_1_0)   # medición de velocidad
    x_wo_1 = x_wo_1 + Δt*(u_l_1*T_wo_1 - x_wo_1)/T_wo_1 # washout
    y_wo_1 = (u_l_1 - x_wo_1)                     # washout
    x_l_1 = x_l_1 + Δt*(y_wo_1 - x_l_1)/T_2_1          # compensador de adelanto        
    v_pss_1 = K_stab_1*(T_1_1/T_2_1*(y_wo_1-x_l_1) + x_l_1)
    
    ## PSS 3
    u_l_3 = (omega_3 - omega_3_0)   # medición de velocidad
    x_wo_3 = x_wo_1 + Δt*(u_l_3*T_wo_3 - x_wo_3)/T_wo_3 # washout
    y_wo_3 = (u_l_3 - x_wo_3)                    # washout
    x_l_3 = x_l_3 + Δt*(y_wo_3 - x_l_3)/T_2_3          # compensador de adelanto        
    v_pss_3 = K_stab_3*(T_1_3/T_2_3*(y_wo_3-x_l_3) + x_l_3)
    
    # se actualiza v_f y se ejecuta la simulación para el nuevo tiempo t    
    events=[{'t_end':t,'v_pss_1':v_pss_1,'v_pss_3':v_pss_3,'v_ref_1':v_ref_1}]
    grid_pss.run(events)
    
    U_l[it] = u_l_1
    V_s[it] = v_pss_1
    it += 1

grid_pss.post();


# In[21]:


fig,axes = plt.subplots()
axes.plot(grid_pss.T,grid_pss.get_values('omega_1'),label='omega_1')
axes.plot(grid_pss.T,grid_pss.get_values('omega_2'),label='omega_2')
axes.plot(grid_pss.T,grid_pss.get_values('omega_3'),label='omega_3')
axes.plot(grid_pss.T,grid_pss.get_values('omega_4'),label='omega_4')
axes.legend()


# In[ ]:





# In[22]:


import scipy.signal as sctrl


# In[24]:


A,B,C,D = ssa.eval_ss(grid)


# In[27]:


grid.u_run_list.index('v_ref_1')


# In[82]:


A_red = grid.A
N_x = A_red.shape[0]
B_red = grid.B[:,grid.u_run_list.index('v_ref_1')].reshape(N_x,1)
C_red = grid.C[grid.outputs_list.index('p_e_1'),:].reshape(1,N_x)
D_red = grid.C[grid.outputs_list.index('p_e_1'),grid.u_run_list.index('v_ref_1')]
eig_values, eig_vectors = np.linalg.eig(A_red)
eig_values.imag/(2*np.pi)


# In[94]:


states =[f'omega_{it+1}' for it in range(4)]
states+=[f'delta_{it+1}' for it in range(4)]

sates_idx = [grid.x_list.index(item) for item in states]
sates_idx


# In[74]:


tf = sctrl.ss2zpk(A_red,B_red,C_red,D_red)
tf


# In[62]:


w, mag, phase = sctrl.bode(tf,w=np.linspace(0.1,20,500))


# In[63]:


fig,axes = plt.subplots(nrows=2)
axes[0].plot(w/(2*np.pi),mag)
axes[1].plot(w/(2*np.pi),phase)


# In[69]:


import control

sys = control.ss(A_red, B_red, C_red, D_red)
control.minreal(sys, tol=None, verbose=True)


# In[65]:


get_ipython().system('pip install control')


# In[70]:


get_ipython().system('pip install slycot')


# In[ ]:




