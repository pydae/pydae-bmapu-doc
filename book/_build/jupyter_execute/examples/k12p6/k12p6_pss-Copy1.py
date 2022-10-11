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
import numba as nb
import time
import scipy.sparse as sspa


# ## Kundur example 12.6 with PSS

# In[2]:


#SVG('https://raw.githubusercontent.com/pydae/pydae/master/examples/grids/k12p6/sp_k12p6.svg')


# In[3]:


from k12p6_pss import k12p6_pss_class,sp_jac_ini_eval_up,sp_jac_ini_eval_xy,sp_jac_ini_eval_num,slu2pydae
from k12p6_pss import jac_ini_ss_eval_xy,jac_ini_ss_eval_up,jac_ini_ss_eval_num
from k12p6_pss import jac_trap_eval_xy,jac_trap_eval_up,jac_trap_eval_num

from k12p6_pss import f_ini_eval as f_ini_eval_n
from scipy.sparse.linalg import spsolve,spilu,splu


# In[4]:


grid = k12p6_pss_class()


# ## Initialization

# In[5]:


grid = k12p6_pss_class()

K_delta = 0.001
K_sec = 0.01
K_a = 200.0
T_r = 0.02
D = 0.1
lf = 1.0
params = {'P_7':-967e6*lf,'P_9':-1_767e6*lf,'Q_7':100e6*lf,'Q_9':250e6*lf,
                  'K_delta_1':K_delta,'K_delta_2':0,
                  'K_delta_3':0,'K_delta_4':0,
                  'K_a_1':K_a,'K_a_2':K_a,'K_a_3':K_a,'K_a_4':K_a,
                  #'T_r_1':T_r,'T_r_2':T_r,'T_r_3':T_r,'T_r_4':T_r,
                  'p_c_1':701.4/900*lf,'p_c_2':701.4/900*lf,'p_c_4':701.4/900*lf,
                  'v_ref_1':1.03,'v_ref_2':1.01,'v_ref_3':1.03,'v_ref_4':1.01,
                     'K_sec_1':0,'K_sec_2':0,'K_sec_3':K_sec,'K_sec_4':0,
                  'K_imw_1':0.001, 'K_imw_2':0.001,'K_imw_3':0.0, 'K_imw_4':0.001,
                  'D_1':D,'D_2':D,'D_3':D,'D_4':D
                    }

#grid.xy_0  = grid.xy_prev[:,0]

grid.ini(params,xy_0='xy_0.json')
#grid.eval_preconditioner_ini()
#grid.spini(params,xy_0='xy_0.json')


# In[5]:


import numba.core.typing.cffi_utils as cffi_support
import cffi
ffi = cffi.FFI()
import mod5 as jacs

cffi_support.register_module(jacs)
f_ini_eval = jacs.lib.f_ini_eval
g_ini_eval = jacs.lib.g_ini_eval
f_run_eval = jacs.lib.f_run_eval
g_run_eval = jacs.lib.g_run_eval
h_eval  = jacs.lib.h_eval

de_jac_ini_xy_eval = jacs.lib.de_jac_ini_xy_eval
de_jac_ini_up_eval = jacs.lib.de_jac_ini_up_eval
de_jac_ini_num_eval = jacs.lib.de_jac_ini_num_eval

sp_jac_ini_xy_eval = jacs.lib.sp_jac_ini_xy_eval
sp_jac_ini_up_eval = jacs.lib.sp_jac_ini_up_eval
sp_jac_ini_num_eval = jacs.lib.sp_jac_ini_num_eval

de_jac_trap_xy_eval= jacs.lib.de_jac_trap_xy_eval            
de_jac_trap_up_eval= jacs.lib.de_jac_trap_up_eval        
de_jac_trap_num_eval= jacs.lib.de_jac_trap_num_eval

sp_jac_trap_xy_eval= jacs.lib.sp_jac_trap_xy_eval            
sp_jac_trap_up_eval= jacs.lib.sp_jac_trap_up_eval        
sp_jac_trap_num_eval= jacs.lib.sp_jac_trap_num_eval


# In[6]:


@nb.njit("float64[:](float64[:],float64[:],float64[:],float64[:],float64[:],float64)")
def test_jac_ini(f,x,y,u,p,Dt):   
        
    f_c_ptr=ffi.from_buffer(np.ascontiguousarray(f))
    x_c_ptr=ffi.from_buffer(np.ascontiguousarray(x))
    y_c_ptr=ffi.from_buffer(np.ascontiguousarray(y))
    u_c_ptr=ffi.from_buffer(np.ascontiguousarray(u))
    p_c_ptr=ffi.from_buffer(np.ascontiguousarray(p))
    
    f_ini_eval(f_c_ptr,x_c_ptr,y_c_ptr,u_c_ptr,p_c_ptr,Dt)
    return f


f = np.copy(0*grid.x)
x = grid.x
y = grid.y_ini
u = grid.u_ini
p = grid.p
Dt = 0.02
get_ipython().run_line_magic('timeit', 'solver(f,x,y,u,p,Dt)')


# In[ ]:


grid.N_xy = grid.N_x + grid.N_y

de_jac_ini = np.zeros((grid.N_xy,grid.N_xy), dtype=np.float64)
x = grid.x
y = grid.y_ini
u = grid.u_ini
p = grid.p
Dt = 0.02
test_de_jac_ini_eval(de_jac_ini,x,y,u,p,Dt)

jac_ini = np.zeros((grid.N_xy,grid.N_xy), dtype=np.float64)

jac_ini_ss_eval_xy(jac_ini,x,y,u,p,Dt)
jac_ini_ss_eval_up(jac_ini,x,y,u,p,Dt)
jac_ini_ss_eval_num(jac_ini,x,y,u,p,Dt)

np.allclose(jac_ini,de_jac_ini)


# In[16]:


grid.N_xy = grid.N_x + grid.N_y

de_jac_trap = np.zeros((grid.N_xy,grid.N_xy), dtype=np.float64)
x = grid.x
y = grid.y_run
u = grid.u_run
p = grid.p
Dt = 0.02
de_jac_trap_eval(de_jac_trap,x,y,u,p,Dt)

jac_trap = np.zeros((grid.N_xy,grid.N_xy), dtype=np.float64)

jac_trap_eval_xy(jac_trap,x,y,u,p,Dt)
jac_trap_eval_up(jac_trap,x,y,u,p,Dt)
jac_trap_eval_num(jac_trap,x,y,u,p,Dt)

np.allclose(jac_trap,de_jac_trap)


# In[ ]:


get_ipython().run_line_magic('timeit', 'test_de_jac_ini_eval(de_jac_ini,x,y,u,p,Dt)')


# In[17]:


get_ipython().run_line_magic('pinfo', 'de_jac_ini_eval')


# In[196]:


get_ipython().run_line_magic('timeit', 'f_ini_eval_n(f,x,y,u,p)')


# In[197]:


f_n = np.copy(0*grid.x)

f_ini_eval_n(f_n,2*x,y,u,p)

np.allclose(f_n,solver(f,2*x,y,u,p,Dt))


# In[15]:


get_ipython().run_line_magic('pinfo', 'np.linalg.solve')


# In[11]:


import numba 







# In[12]:


from k12p6_pss import sprichardson,csr2pydae


# In[13]:


def spss_ini(self):
    J_d,J_i,J_p = csr2pydae(self.sp_jac_ini)

    xy_ini,it,iparams = spsstate(self.xy,self.u_ini,self.p,
             J_d,J_i,J_p,
             self.P_d,self.P_i,self.P_p,self.perm_r,self.perm_c,
             self.N_x,self.N_y,
             max_it=self.max_it,tol=self.itol,
             lmax_it=self.lmax_it_ini,
             ltol=self.ltol_ini,
             ldamp=self.ldamp)


    self.xy_ini = xy_ini
    self.N_iters = it
    self.iparams = iparams

    return xy_ini
    



                
def run(self,t_end,up_dict):
    for item in up_dict:
        self.set_value(item,up_dict[item])

    t = self.t
    p = self.p
    it = self.it
    it_store = self.it_store
    xy = self.xy
    u = self.u_run

    t,it,it_store,xy =  daesolver(t,t_end,it,it_store,xy,u,p,
                              self.jac_trap,
                              self.Time,
                              self.X,
                              self.Y,
                              self.Z,
                              self.iters,
                              self.Dt,
                              self.N_x,
                              self.N_y,
                              self.N_z,
                              self.decimation,
                              max_it=50,itol=1e-8,store=1)

    self.t = t
    self.it = it
    self.it_store = it_store
    self.xy = xy
    


# In[32]:


def sprun(self,t_end,up_dict):
    
    for item in up_dict:
        self.set_value(item,up_dict[item])

    t = self.t
    p = self.p
    it = self.it
    it_store = self.it_store
    xy = self.xy
    u = self.u_run
    self.iparams_run = np.zeros(10,dtype=np.float64)

    t,it,it_store,xy = spdaesolver(t,t_end,it,it_store,xy,u,p,
                              self.jac_trap,
                              self.J_run_d,self.J_run_i,self.J_run_p,
                              self.P_run_d,self.P_run_i,self.P_run_p,self.perm_run_r,self.perm_run_c,
                              self.Time,
                              self.X,
                              self.Y,
                              self.Z,
                              self.iters,
                              self.Dt,
                              self.N_x,
                              self.N_y,
                              self.N_z,
                              self.decimation,
                              self.iparams_run,
                              max_it=self.max_it,itol=self.max_it,store=self.store,
                              lmax_it=self.lmax_it,ltol=self.ltol,ldamp=self.ldamp,mode=self.mode)

    self.t = t
    self.it = it
    self.it_store = it_store
    self.xy = xy


# In[56]:



    
    


# In[1]:


grid_3 = k12p6_pss_class()
grid_3.Dt = 0.01
grid_3.ini(params_new,xy_0='xy_0.json')  
eval_preconditioner_ini(grid_3)
eval_preconditioner_run(grid_3)

t_0 = time.time()
sprun(grid_3,1,{})
sprun(grid_3,30,{'P_1':-600e6})
grid_3.post()
print(time.time()-t_0)


# In[24]:





# In[39]:


import time

grid_1 = k12p6_pss_class()
grid_2 = k12p6_pss_class()
grid_1.Dt = 0.01
grid_2.Dt = 0.01

params_new = params.copy()
params_new['P_1'] = 00e6

grid_1.ini(params_new,xy_0='xy_0.json')
t_0 = time.time()
grid_1.run(1,{})
grid_1.run(30,{'P_1':-600e6})
grid_1.post()
print(time.time()-t_0)

grid_2.ini(params_new,xy_0='xy_0.json')    
t_0 = time.time()
run(grid_2,1,{})
run(grid_2,30,{'P_1':-600e6})
grid_2.post()
print(time.time()-t_0)



# In[53]:


fig,axes = plt.subplots()
axes.plot(grid_1.Time,grid_1.get_values('omega_1'),label='omega_1')
axes.plot(grid_2.Time,grid_2.get_values('omega_1'),label='omega_1')
axes.plot(grid_3.Time,grid_3.get_values('omega_1'),label='omega_1')

#axes.legend()


# In[399]:


grid_2.report_u()


# In[97]:


get_ipython().run_line_magic('timeit', 'spss_ini(grid)')


# In[222]:


xy_0 = np.hstack((x,y))

def tests(P_1s):
    #P_1s = np.linspace(0,400e6,N)
    for P_1 in P_1s:
        grid.u_ini[0] = -P_1
        spss_ini(grid)

N = 10_000
    

P_1s = np.random.rand(N)*100e6 + 200e6
get_ipython().run_line_magic('timeit', 'tests(P_1s)')


# In[157]:


grid.u_ini[0] = -10.0e6
spss_ini(grid)


# In[56]:


jac_ini = grid.jac_ini
x = grid.x
y = grid.y_ini
u = grid.u_ini
p = np.copy(grid.p)
N_x = grid.N_x
N_y = grid.N_y
xy = np.hstack((x,y))



# In[80]:


xy_0 = np.hstack((x,y))

def tests(P_1s):
    #P_1s = np.linspace(0,400e6,N)
    for P_1 in P_1s:
        u[0] = -P_1
        xy,it = sstate(xy_0,u,p,jac_ini,N_x,N_y,max_it=50,tol=1e-8)

N = 10_000
    

P_1s = np.random.rand(N)*400e6
get_ipython().run_line_magic('timeit', 'tests(P_1s)')


# In[74]:


8960/N


# In[70]:





# In[43]:


def eval_preconditioner_ini(self):

    sp_jac_ini_eval_up(self.sp_jac_ini.data,
                    self.x,self.y_ini,self.u_ini,self.p,self.Dt)
    sp_jac_ini_eval_xy(self.sp_jac_ini.data,
                    self.x,self.y_ini,self.u_ini,self.p,self.Dt)

    P_slu = spilu(sspa.csc_matrix(self.sp_jac_ini),fill_factor=self.fill_factor_ini,
                  drop_tol=self.drop_tol_ini,drop_rule = self.drop_rule_ini)

    self.P_slu3 = P_slu
    P_d,P_i,P_p,perm_r,perm_c = slu2pydae(P_slu)   
    self.P_d = P_d
    self.P_i = P_i
    self.P_p = P_p

    self.perm_r = perm_r
    self.perm_c = perm_c
    
eval_preconditioner_ini(grid)


# In[59]:


grid.report_u()


# In[45]:


get_ipython().run_line_magic('timeit', "grid.spini(params,xy_0='xy_0.json')")


# In[56]:


import numba
from numba import cuda
import math
from numba.pycc import CC


# In[96]:


t_0 = time.time()


@cuda.jit(device=True)
def Piecewise(a_val,a_test,b_val,b_test,c_val,c_test,out,i):
    out[i] = 0.0
    if a_test:
        out[i] = a_val
        return
    if b_test:
        out[i] = b_val
        return
    if c_test:
        out[i] = c_val
        return
                     

#cc = CC('jac_mod2')

#@numba.njit('(float64[:,:],float64[:],float64[:],float64[:],float64[:])')
#@numba.njit
#@cc.export('jac_ini_eval', '(float64[:,:],float64[:],float64[:],float64[:],float64[:])')
@numba.cuda.jit()
def jac_ini_ss_eval_xy(jac_ini,x,y,u,p,aux):
        
    Piecewise(10, 2>5,-p[55], True,0.0,True,aux,0)    
    y[0] = aux[0]

print(time.time()-t_0)               


# In[97]:


N_i = 1

# manage nr of threads (threads)
threads_per_block = 1
blocks_per_grid = (N_i + (threads_per_block - 1)) \
        // threads_per_block



# start timer
start = time.perf_counter()





jac_ini_d = cuda.to_device(grid.jac_ini)
x_d = cuda.to_device(grid.x)
y_ini_d = cuda.to_device(grid.y_ini)
u_ini_d = cuda.to_device(grid.u_ini)
p_d = cuda.to_device(grid.p)
aux_d = cuda.to_device(np.array([0.0,0.0,0.0,0.0]))
jac_ini_ss_eval_xy[blocks_per_grid, threads_per_block](jac_ini_d,x_d,y_ini_d,u_ini_d,p_d,aux_d)
# start parallel simulations
cuda.synchronize()
# measure time elapsed
end = time.perf_counter()

y_ini_n = y_ini_d.copy_to_host()

y_ini_n[0]


# In[95]:


p[55]


# In[ ]:





# In[70]:


import numba
@numba.njit
def foo(n):
    c = 0
    for i in range(n):
        for j in range(i):
            c += j
    return c

numba.config.LLVM_PASS_TIMINGS = True

jac_ini_ss_eval_xy(grid.jac_ini,grid.x,grid.y_ini,grid.u_ini,grid.p)

md = jac_ini_ss_eval_xy.get_metadata(jac_ini_ss_eval_xy.signatures[0])
print(md['llvm_pass_timings'])


# In[89]:


jac_ini_ss_eval_xy.signatures[0]


# In[50]:


t_0 = time.time()
get_ipython().run_line_magic('timeit', 'jac_ini_ss_eval_xy(grid.jac_ini,grid.x,grid.y_ini,grid.u_ini,grid.p)')
print(time.time()-t_0)               


# In[37]:


10.6 µs ± 469 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)


# In[52]:


from numba import cfunc, carray
from numba.types import float64, CPointer, void, intp

# A callback with the C signature `void(double *, double *, size_t)`

@cfunc(void(CPointer(float64), CPointer(float64), intp))
def invert(in_ptr, out_ptr, n):
    in_ = carray(in_ptr, (n,))
    out = carray(out_ptr, (n,))
    for i in range(n):
        out[i] = 1 / in_[i]


# In[63]:


from numba import cfunc
def integrand(t):
        return np.exp(-t[0]) / t**2

nb_integrand = cfunc("float64(float64[:])")(integrand)


# In[81]:


from numba import cfunc, types, carray

c_sig = types.void(types.CPointer(types.double),
                   types.CPointer(types.double),
                   types.intc, types.intc)

@cfunc(c_sig)
def my_callback(in_, out, m, n):
    in_array = carray(in_, (m, n))
    out_array = carray(out, (m, n))
    for i in range(m):
        for j in range(n):
            out_array[i, j] = 2 * in_array[i, j]
            
my_callback(np.ones((4,4)),np.ones((4,4)),4,4)


# In[121]:


from numba.pycc import CC

cc = CC('my_module2')
# Uncomment the following line to print out the compilation steps
#cc.verbose = True

@cc.export('multf', 'f8(f8, f8)')
def mult(a, b):
    return a * b

@cc.export('square', 'f8(f8)')
def square(a):
    return a ** 2


@cc.export('centdiff_1d', '(f8[:],f8[:],f8)')
def centdiff_1d(u,D,dx):
    D = np.empty_like(u)
    D[0] = 0
    D[-1] = 0
    for i in range(1, len(D) - 1):
        D[i] = (u[i+1] - 2 * u[i] + u[i-1]) / dx**2
    return D


# In[127]:


t_0 = time.time()
cc.compile()
print(time.time()-t_0)


# In[128]:


import jac_mod2
t_0 = time.time()
jac_mod2.jac_ini_eval(grid.jac_ini,grid.x,grid.y_ini,grid.u_ini,grid.p)
print(time.time()-t_0)               


# In[ ]:





# In[ ]:





# In[61]:


get_ipython().run_line_magic('timeit', 'integrand(2.0)')


# In[56]:


import scipy.integrate as si
def do_integrate(func):
        """
        Integrate the given function from 1.0 to +inf.
        """
        return si.quad(func, 1, np.inf)

do_integrate(integrand)


# ## Small signal analysis

# ### Eigenvalues

# In[67]:


ssa.A_eval(grid)
damp = ssa.damp_report(grid)
damp.sort_values('Damp').round(3)


# ### Participation factors

# In[68]:


ssa.participation(grid).abs().round(2)['Mode 18'].sort_values()


# ### Mode shapes

# In[69]:


ssa.shape2df(grid).loc['Mode 18'][[f'omega_{it+1}' for it in range(4)]]
#ssa.shape2df(grid).loc['Mode 24'][[f'e1d_{it+1}' for it in range(4)]]


# In[70]:


svg_string = ssa.plot_shapes(grid,mode='Mode 18',states=[f'omega_{it+1}' for it in range(4)])
SVG(svg_string)


# ## Time domain simulation

# In[15]:


grid.ini(params,xy_0='xy_0.json')
grid.eval_preconditioner_ini()
grid.Dt = 0.01
grid.spini(params)        #'H_1':1e8,'H_2':1e8,'H_3':1e8,'H_4':1e8
grid.eval_preconditioner_run()


# In[16]:


get_ipython().run_cell_magic('timeit', '', "grid.ini(params)        #'H_1':1e8,'H_2':1e8,'H_3':1e8,'H_4':1e8\n\ngrid.run( 1.0,{'v_ref_1': 1.03})        #'H_1':1e8,'H_2':1e8,'H_3':1e8,'H_4':1e8\ngrid.run(15.0,{'v_ref_1': 1.03*1.05})\ngrid.post()\n")


# In[294]:


#grid = k12p6_pss_class()

fig,axes = plt.subplots()
axes.plot(grid.Time,grid.get_values('omega_1'),label='omega_1')
axes.plot(grid.Time,grid.get_values('omega_2'),label='omega_2')
axes.plot(grid.Time,grid.get_values('omega_3'),label='omega_3')
axes.plot(grid.Time,grid.get_values('omega_4'),label='omega_4')
axes.legend()
fig


# In[12]:


import ipywidgets
get_ipython().run_line_magic('matplotlib', 'widget')


# In[ ]:





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





# In[84]:





# In[ ]:




