#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pydae.grid_tools as gt
import pydae.ssa as ssa
from IPython.core.display import HTML,SVG
from pydae.svg_tools import svg
import scipy.optimize as sopt
get_ipython().run_line_magic('config', "InlineBackend.figure_formats = ['svg']")


# ## Kundur example 12.6 with PSS

# In[2]:


SVG('https://raw.githubusercontent.com/pydae/pydae/master/examples/grids/k12p6/sp_k12p6.svg')


# In[3]:


from k12p6_pss import k12p6_pss_class


# ## Initialization

# In[4]:


xy_0_dict = {
"V_1":1.0,"V_2":1.0,"V_3":1.0,"V_4":1.0,
"V_5":1.0,"V_6":1.0,"V_7":1.0,"V_8":1.0,
"V_9":1.0,"V_10":1.0,"V_11":1.0
}


# In[5]:


900*3


# In[6]:


grid = k12p6_pss_class()

K_delta = 0.001
K_sec = 2
K_a = 200.0
T_r = 0.02
D = 0.1

params = {'P_7':-967e6,'P_9':-1_767e6,'Q_7':150e6,'Q_9':250e6,
                  'K_delta_1':K_delta,'K_delta_2':K_delta,
                  'K_delta_3':K_delta,'K_delta_4':K_delta,
                  'K_a_1':K_a,'K_a_2':K_a,'K_a_3':K_a,'K_a_4':K_a,
                  #'T_r_1':T_r,'T_r_2':T_r,'T_r_3':T_r,'T_r_4':T_r,
                  'p_c_1':200.4/900,'p_c_2':900/900,'p_c_4':900/900,
                  #'v_ref_1':1.03,'v_ref_2':1.01,'v_ref_3':1.03,'v_ref_4':1.01,
          'T_gov_3_4':2.0,
                  'K_sec_1':0,'K_sec_2':K_sec,'K_sec_3':K_sec,'K_sec_4':0,
                  'K_imw_1':0.1, 'K_imw_2':0.0,'K_imw_3':0.0, 'K_imw_4':0.5,
                  'D_1':D,'D_2':D,'D_3':D,'D_4':D
                    }
T_1 = 0.64
T_2 = 0.15
K_stab = 10
grid.set_values({'K_stab_1':K_stab,'K_stab_2':K_stab,'K_stab_3':K_stab,'K_stab_4':K_stab})
grid.set_values({'T_1_1':T_1,'T_1_2':T_1,'T_1_3':T_1,'T_1_4':T_1})
grid.set_values({'T_2_1':T_2,'T_2_2':T_2,'T_2_3':T_2,'T_2_4':T_2})

grid.initialize([params],
                   xy_0_dict,compile=True)

grid.simulate([
         {'t_end':  1.0,'v_ref_1': 1.03, 'P_7':-967e6,'Dt':0.1,'decimation':10},
         {'t_end':  1.3,'v_ref_1': 1.03, 'S_n_1':0,'p_c_1':0.0},
         {'t_end':  300.0,'v_ref_1': 1.03, 'Q_7':350e6, 'Q_9':650e6},
],'prev');

fig,axes = plt.subplots()
#axes.plot(grid.T,grid.get_values('omega_1'),label='omega_1')
axes.plot(grid.T,grid.get_values('omega_2'),label='omega_2')
axes.plot(grid.T,grid.get_values('omega_3'),label='omega_3')
axes.plot(grid.T,grid.get_values('omega_4'),label='omega_4')
axes.plot(grid.T,grid.get_values('omega_coi'),label='omega_coi')
axes.legend()


# In[102]:


fig,axes = plt.subplots()
#axes.plot(grid.T,grid.get_values('p_m_1'),label='p_m_1')
axes.plot(grid.T,grid.get_values('p_m_2'),label='p_m_2')
axes.plot(grid.T,grid.get_values('p_m_3'),label='p_m_3')
axes.plot(grid.T,grid.get_values('p_m_4'),label='p_m_4')
axes.legend()






# In[103]:


fig,axes = plt.subplots()
axes.plot(grid.T,grid.get_values('V_1'),label='V_1')
axes.plot(grid.T,grid.get_values('V_2'),label='V_2')
axes.plot(grid.T,grid.get_values('V_3'),label='V_3')
axes.plot(grid.T,grid.get_values('V_4'),label='V_4')
axes.plot(grid.T,grid.get_values('V_7'),label='V_7')
axes.plot(grid.T,grid.get_values('V_9'),label='V_9')
axes.legend()


# In[58]:


import ipywidgets
get_ipython().run_line_magic('matplotlib', 'widget')


# In[21]:


grid.report_params()


# In[28]:


grid = k12p6_pss_class()

K_delta = 0.001
K_sec = 0.1
K_a = 200.0
T_r = 0.02
D = 0.1

params = {'P_7':-967e6,'P_9':-1_767e6,'Q_7':100e6,'Q_9':250e6,
                  'K_delta_1':K_delta,'K_delta_2':K_delta,
                  'K_delta_3':K_delta,'K_delta_4':K_delta,
                  'K_a_1':K_a,'K_a_2':K_a,'K_a_3':K_a,'K_a_4':K_a,
                  #'T_r_1':T_r,'T_r_2':T_r,'T_r_3':T_r,'T_r_4':T_r,
                  'p_c_1':701.4/900,'p_c_2':701.4/900,'p_c_4':701.4/900,
                  #'v_ref_1':1.03,'v_ref_2':1.01,'v_ref_3':1.03,'v_ref_4':1.01,
                     'K_sec_1':0,'K_sec_2':0,'K_sec_3':K_sec,'K_sec_4':0,
                  'K_imw_1':0.01, 'K_imw_2':0.01,'K_imw_3':0.0, 'K_imw_4':0.01,
                  'D_1':D,'D_2':D,'D_3':D,'D_4':D
                    }


T_1 = 0.64
T_2 = 0.15
K_stab = 10
grid.set_values({'K_stab_1':K_stab,'K_stab_2':K_stab,'K_stab_3':K_stab,'K_stab_4':K_stab})
grid.set_values({'T_1_1':T_1,'T_1_2':T_1,'T_1_3':T_1,'T_1_4':T_1})
grid.set_values({'T_2_1':T_2,'T_2_2':T_2,'T_2_3':T_2,'T_2_4':T_2})

fig,axes = plt.subplots()
axes.plot(grid.T,grid.get_values('omega_1'),label='omega_1')
axes.plot(grid.T,grid.get_values('omega_2'),label='omega_2')
axes.plot(grid.T,grid.get_values('omega_3'),label='omega_3')
axes.plot(grid.T,grid.get_values('omega_4'),label='omega_4')
axes.legend()
fig


# In[16]:


plt.ioff()
plt.clf()

fig,axes = plt.subplots()

K_delta,K_sec = 0.001,0.001
K_a = 100.0
K_stab = 10
T_1 = 0.2

grid.initialize([{'K_a_1':K_a,'K_a_2':K_a,'K_a_3':K_a,'K_a_4':K_a,
                  'K_stab_1':K_stab,'K_stab_2':K_stab,'K_stab_3':K_stab,'K_stab_4':K_stab,
                  'T_1_1':T_1,'T_1_2':T_1,'T_1_3':T_1,'T_1_4':T_1}],
                   xy_0_dict,compile=True)

ssa.eval_A(grid)
damp = ssa.damp_report(grid)
eig_values,eig_vectors = np.linalg.eig(grid.A)

fig.tight_layout()

fig = ssa.plot_eig(grid,x_min=-2,x_max=0.01,y_min=0,y_max=1.5);
ax = fig.axes[0]
eigen_plot = ax.get_children()[8]


sld_T_1  = ipywidgets.FloatSlider(orientation='horizontal',description = "T_1", 
                                value=0.1, min=0.05,max= 2.0, 
                                step=0.01)


sld_T_2  = ipywidgets.FloatSlider(orientation='horizontal',description = "T_2", 
                                value=0.1, min=0.05,max= 2.0, 
                                step=0.01)

sld_K_stab  = ipywidgets.FloatSlider(orientation='horizontal',description = "K_stab", 
                                value=0.0, min=0.0,max= 19.0, 
                                step=0.1)

ckbox_gain = ipywidgets.Checkbox(
    value=False,
    description='Gain compensation',
    disabled=False
)

txt_damp = ipywidgets.Text(
    value='0.0',
    placeholder='Type something',
    description='Damping:',
    disabled=False)

def update(change):
    
    T_1 = sld_T_1.value
    T_2 = sld_T_2.value
    K_stab  = sld_K_stab.value
 
    grid.set_values({'K_stab_1':K_stab,'K_stab_2':K_stab,'K_stab_3':K_stab,'K_stab_4':K_stab})
    grid.set_values({'T_1_1':T_1,'T_1_2':T_1,'T_1_3':T_1,'T_1_4':T_1})
    grid.set_values({'T_2_1':T_2,'T_2_2':T_2,'T_2_3':T_2,'T_2_4':T_2})

    grid.ss()
    grid.eval_jacobians()
    ssa.eval_A(grid)
    eig_values,eig_vectors = np.linalg.eig(grid.A)
    
    eigen_plot.set_data(eig_values.real,eig_values.imag/(2*np.pi))

    zetas = -eig_values.real/np.abs(eig_values) 

    txt_damp.value = f'{100*np.min(zetas):4.1f}'
    
    fig.canvas.draw_idle()
      
sld_T_1.observe(update, names='value')
sld_T_2.observe(update, names='value')
sld_K_stab.observe(update, names='value')
ckbox_gain.observe(update, names='value')

layout_row1 = ipywidgets.HBox([fig.canvas])
layout_row2 = ipywidgets.HBox([sld_T_1,sld_T_2, sld_K_stab])
layout_row3 = ipywidgets.HBox([txt_damp])
layout = ipywidgets.VBox([layout_row1,layout_row2,layout_row3])
layout


# In[25]:


grid.simulate([
         {'t_end': 1.0,'v_ref_1': 1.03, 'Dt':0.01,'decimation':1,
         #'H_1':1e8,'H_2':1e8,'H_3':1e8,'H_4':1e8
         },
         {'t_end':15.0,'v_ref_1': 1.03*1.05}],'prev');

fig,axes = plt.subplots()
axes.plot(grid.T,grid.get_values('omega_1'),label='omega_1')
axes.plot(grid.T,grid.get_values('omega_2'),label='omega_2')
axes.plot(grid.T,grid.get_values('omega_3'),label='omega_3')
axes.plot(grid.T,grid.get_values('omega_4'),label='omega_4')
axes.legend()
fig


# In[26]:


fig,axes = plt.subplots()
axes.plot(grid.T,grid.get_values('v_pss_1'),label='v_pss_1')
axes.plot(grid.T,grid.get_values('v_pss_2'),label='v_pss_2')
axes.plot(grid.T,grid.get_values('v_pss_3'),label='v_pss_3')
axes.plot(grid.T,grid.get_values('v_pss_4'),label='v_pss_4')
axes.legend()
fig


# ## PSS design

# In[239]:


grid = k12p6_class()

K_delta = 0.001
K_sec = 0.01
K_a = 300.0
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


# In[240]:


V_1_ini = grid.get_values('V_1')[0]
V_1_end = grid.get_values('V_1')[-1]
ΔV_1 = V_1_end - V_1_ini
ΔV_1_e = (1-1/np.e)*ΔV_1
V_1_e = ΔV_1_e + V_1_ini
idx = np.argmax(grid.get_values('V_1')>V_1_e)
Tau_V = grid.T[idx] -1


# K_a = 150 V,p_e 0.08,0.11 0.09
# K_a = 100 V,p_e 0.13,0.16 
# K_a =  50  0.25,0.31 0.22
p_e_1_ini = grid.get_values('p_e_1')[0]
p_e_1_end = grid.get_values('p_e_1')[-1]
Δp_e_1 = p_e_1_end - p_e_1_ini
Δp_e_1_e = (1-1/np.e)*Δp_e_1
p_e_1_e = Δp_e_1_e + p_e_1_ini
idx = np.argmax(grid.get_values('p_e_1')>p_e_1_e)
Tau_p_e = grid.T[idx] -1   


Tau = Tau_p_e

w = 2*np.pi*0.5
phi_sm = np.angle(1/(Tau*1j*w+1))
T_2 = 0.1

def res(x):
    T_1 = x
    phi = np.angle((T_1*1j*w+1)/(T_2*1j*w+1))
    return phi + phi_sm

T_1 = sopt.newton(res,0.1)[0]

gain_l = np.abs((T_1*1j*w+1)/(T_2*1j*w+1))
gain_l

gain_p = np.abs((1)/(Tau*1j*w+1))
gain_p


print(f'T_1 = {T_1:0.2f} s')
print(f'T_2 = {T_2:0.2f} s')


# In[ ]:





# In[ ]:





# In[241]:


fig,axes = plt.subplots()
axes.plot(grid.T,grid.get_values('p_e_1')-grid.get_values('p_e_1')[0],label='p_e_1')
axes.plot(grid.T,2*(grid.get_values('V_1')-grid.get_values('V_1')[0]),label='V_1')

#axes.set_xlim((0,3))
axes.legend()


# In[242]:


fig,axes = plt.subplots()
axes.plot(grid.T,grid.get_values('V_1'),label='V_1')
#axes.set_xlim((0,3))
axes.legend()


# ### PSS simulation

# In[243]:


Δt = 0.01  # latencia del control (cada cuanto se ejecuta el controlador)
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
omega_1_0 = grid_pss.get_value('omega_1') # se guarda la tensión de excitación inicial
omega_3_0 = grid_pss.get_value('omega_3') # se guarda la tensión de excitación inicial

# diseño del control:
## PSS
K_stab_1,K_stab_3 = 70.0/gain_l,70.0/gain_l
x_l_1,x_l_3 = 0.0,0.0
T_1_1,T_1_3 = 0.1,0.1
T_2_1,T_2_3 = 0.1,0.1

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
    x_l_1 = x_l_1 + Δt*(u_l_1 - x_l_1)/T_2_1          # compensador de adelanto        
    v_pss_1 = K_stab_1*(T_1_1/T_2_1*(u_l_1-x_l_1) + x_l_1)
    
    ## PSS 3
    u_l_3 = (omega_3 - omega_3_0)   # medición de velocidad
    x_l_3 = x_l_1 + Δt*(u_l_3 - x_l_3)/T_2_3          # compensador de adelanto        
    v_pss_3 = K_stab_3*(T_1_3/T_2_3*(u_l_3-x_l_3) + x_l_3)
    
    # se actualiza v_f y se ejecuta la simulación para el nuevo tiempo t    
    events=[{'t_end':t,'v_pss_1':v_pss_1,'v_pss_3':v_pss_3,'v_ref_1':v_ref_1}]
    grid_pss.run(events)
    
    U_l[it] = u_l_1
    V_s[it] = v_pss_1
    it += 1

grid_pss.post();


# In[244]:


fig,axes = plt.subplots()
axes.plot(grid_pss.T,grid_pss.get_values('omega_1')-1,label='omega_1')
axes.plot(grid_pss.T,grid_pss.get_values('omega_2')-1,label='omega_2')
axes.plot(grid_pss.T,grid_pss.get_values('omega_3')-1,label='omega_3')
axes.plot(grid_pss.T,grid_pss.get_values('omega_4')-1,label='omega_4')
axes.legend()


# In[236]:


fig,axes = plt.subplots()
axes.plot(grid_pss.T,grid_pss.get_values('V_1')-grid_pss.get_values('V_1')[-1],label='V_1')
axes.set_xlim(0.9,10.2)
axes.legend()


# In[ ]:


#ciclos = 1/(2*pi*zeta)
ciclos = 2
zeta = 1/(2*np.pi*ciclos)
zeta


# In[ ]:


-0.003*0.37


# In[ ]:





# In[104]:


import numba


# In[105]:


numba.__version__


# In[ ]:




