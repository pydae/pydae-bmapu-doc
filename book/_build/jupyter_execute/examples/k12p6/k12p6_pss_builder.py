#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import sympy as sym
import json
import sympy as sym
import pydae.buildfast as db
import pydae.build_cffi as dbc

from pydae.grid_bpu import bpu


# In[2]:


file_path = 'k12p6_pss.json'
bpu_obj = bpu(data_input=file_path)


# In[3]:


g_list = bpu_obj.dae['g'] 
h_dict = bpu_obj.dae['h_dict']
f_list = bpu_obj.dae['f']
x_list = bpu_obj.dae['x']
params_dict = bpu_obj.dae['params_dict']

sys = {'name':'k12p6_pss',
       'params_dict':params_dict,
       'f_list':f_list,
       'g_list':g_list,
       'x_list':x_list,
       'y_ini_list':bpu_obj.dae['y_ini'],
       'y_run_list':bpu_obj.dae['y_run'],
       'u_run_dict':bpu_obj.dae['u_run_dict'],
       'u_ini_dict':bpu_obj.dae['u_ini_dict'],
       'h_dict':h_dict}

sys = db.system(sys)
db.sys2num(sys)



# In[6]:


sysc = dbc.system(sys)
dbc.jacobians(sysc)
defs,source = dbc.sym2src(sysc)
dbc.compile_module('k12p6_pss_c_cffi',defs,source)
dbc.sys2num('k12p6_pss_c',sysc, verbose=True)


# In[5]:


from sympy.matrices.sparsetools import _doktocsr
from sympy import SparseMatrix

Fx_ini = sys['Fx_ini']
Fy_ini = sys['Fy_ini']
Gx_ini = sys['Gx_ini']
Gy_ini = sys['Gy_ini']

Fx_run = sys['Fx_run']
Fy_run = sys['Fy_run']
Gx_run = sys['Gx_run']
Gy_run = sys['Gy_run']

jac_ini = sym.Matrix([[Fx_ini, Fy_ini],[Gx_ini,Gy_ini]])  
sp_jac_ini_list = _doktocsr(SparseMatrix(jac_ini))


N_x = len(x_list)
eye = sym.eye(N_x, real=True)
Dt = sym.Symbol('Dt',real=True)
jac_trap = sym.Matrix([[eye - 0.5*Dt*Fx_run, -0.5*Dt*Fy_run],[Gx_run,Gy_run]])  
sp_jac_trap_list = _doktocsr(SparseMatrix(jac_trap))


# In[157]:





# In[ ]:





# In[122]:


import time
import re
from sympy.codegen.ast import Assignment
LHS = sym.Symbol('LHS')
#init_printing(use_unicode=True)

matrix_name = 'out'
matrix = jac_trap
string_sym = ''
string = ''
string_xy = ''
string_up = ''
string_num = ''

t_0 = time.time()

N = matrix.shape[0]
for irow in range(N):
    for icol in range(N):
        if not matrix[irow,icol] == 0:
            string_sym += sym.ccode(Assignment(LHS,matrix[irow,icol])).replace('LHS',f'{matrix_name}[{N*irow+icol}]') +'\n'
            
string = sym2xyup(string_sym,sys)

print(time.time()-t_0)
print(string)


# In[ ]:





# In[124]:


LHS = sym.Symbol('LHS')
#init_printing(use_unicode=True)

matrix_name = 'out'
matrix = jac_trap
string = ''
string_xy = ''
string_up = ''
string_num = ''

t_0 = time.time()
for irow in range(matrix.shape[0]):
    for icol in range(matrix.shape[1]):
        if not matrix[irow,icol] == 0:
            string_sym = sym.ccode(Assignment(LHS,matrix[irow,icol])).replace('LHS',f'{matrix_name}[{irow*N+icol}]') +'\n'
            string_i = sym2xyup(string_sym,sys)
            
            if 'x[' in string_i or 'y[' in string_i:
                string_xy += string_i 
            elif 'p[' in string_i or 'u[' in item or 'Dt' in string_i:
                string_up += string_i 
            else:
                string_num += string_i 
    
            

print(time.time()-t_0)

print(string_xy)


# In[175]:


def matsym2c(fun_name,matrix,matrix_name,sparse = True,xyupn=True,inirun='ini'):
    LHS = sym.Symbol('LHS')
    #init_printing(use_unicode=True)

    string = ''
    string_xy = ''
    string_up = ''
    string_num = ''
    
    rhs_list = []
    

    if sparse:
        for irow in range(len(matrix)):
            if not matrix[irow] == 0:
                string_sym = sym.ccode(Assignment(LHS,matrix[irow])).replace('LHS',f'{matrix_name}[{irow}]') +'\n'
                string_i = sym2xyup(string_sym,sys)

                if 'x[' in string_i or 'y[' in string_i:
                    string_xy += string_i 
                elif 'p[' in string_i or 'u[' in string_i or 'Dt' in string_i:
                    string_up += string_i 
                else:
                    string_num += string_i
    else:
        N_col = matrix.shape[1]
        for irow in range(matrix.shape[0]):
            for icol in range(N_col):
                if not matrix[irow,icol] == 0:
                    string_sym = sym.ccode(Assignment(LHS,matrix[irow,icol])).replace('LHS',f'{matrix_name}[{irow*N_col+icol}]') +'\n'
                    string_i = sym2xyup(string_sym,sys)
                    
                    if xyupn:

                        if 'x[' in string_i or 'y[' in string_i:
                            string_xy += string_i 
                        elif 'p[' in string_i or 'u[' in string_i or 'Dt' in string_i:
                            string_up += string_i 
                        else:
                            string_num += string_i 
                            
                    else:
                        string += string_i
    

    defs = ''
    if xyupn:
        defs += f'void {fun_name}_xy_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt);' + '\n' 
        defs += f'void {fun_name}_up_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt);' + '\n' 
        defs += f'void {fun_name}_num_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt);' + '\n' 
    else:
        defs += f'void {fun_name}_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt);' + '\n' 
        
    source = '' 
    if xyupn:
        source += f'void {fun_name}_xy_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt)' + '{' +'\n'*2
        source += string_xy
        source += '\n}\n\n'
        source += f'void {fun_name}_up_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt)'  + '{'+ '\n'*2
        source += string_up
        source += '\n}\n\n'
        source += f'void {fun_name}_num_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt)'  + '{'+ '\n'*2
        source += string_num
        source += '\n}\n\n'
    else:
        source += f'void {fun_name}_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt)' + '{' +'\n'*2
        source += string
        source += '\n}\n\n'            
    
    return defs,source


#print(string)

funcs = [
    ('f_ini',sys['f'],'f',False,False,'ini'),
    ('f_run',sys['f'],'f',False,False,'run'),
    ('g_ini',sys['g'],'g',False,False,'ini'),
    ('g_run',sys['g'],'g',False,False,'run'),
    ('h_run',sys['h'],'h',False,False,'run'),
    ('jac_ini',jac_ini,'jac_ini',False,True,'ini'),
    ('sp_jac_ini',sp_jac_ini_list[0],'sp_jac_ini',True,True,'ini'),
    ('jac_trap',jac_trap,'jac_trap',False,True,'run'),
    ('sp_jac_trap',sp_jac_trap_list[0],'sp_jac_trap',True,True,'run'),
]


t_0 = time.time()
defs = ''
source = ''
for fun_name,matrix,matrix_name,sparse,xyupn,inirun in funcs:
    defs_i,source_i = matsym2c(fun_name,matrix,matrix_name,sparse = sparse, xyupn=xyupn, inirun=inirun)
    defs += defs_i
    source += source_i
print(time.time()-t_0)


# In[6]:


import time
import re
from sympy.codegen.ast import Assignment

def sym2xyup(string,sys,inirun):
    i = 0
    for item in sys['x']:
        string = re.sub(f"\\b{item}\\b"  ,f'x[{i}]',string)
        i+=1

    i = 0
    for item in sys[f'y_{inirun}']:
        string = re.sub(f"\\b{item}\\b"  ,f'y[{i}]',string)
        i+=1

    i = 0
    for item in sys[f'u_{inirun}']:
        string = re.sub(f"\\b{item}\\b"  ,f'u[{i}]',string)
        i+=1

    i = 0
    for item in params_dict:
        string = re.sub(f"\\b{item}\\b"  ,f'p[{i}]',string)
        i+=1
        
    return string

def sym2str(fun_name,vector,sys,inirun):
    LHS = sym.Symbol('LHS')

    string = ''
    for irow in range(len(vector)):
        string_sym = sym.ccode(Assignment(LHS,vector[irow])).replace('LHS',f'out[{irow}]') +'\n'
        string += sym2xyup(string_sym,sys,inirun=inirun)

    defs   = f'void {fun_name}_eval(double *out,double *x,double *y,double *u,double *p,double Dt);' + '\n' 
    source = f'void {fun_name}_eval(double *out,double *x,double *y,double *u,double *p,double Dt)'  + '{'+ '\n'*2
    source += string + '\n}\n'
    return defs,source
        
        
                
def sym2rhs(data,indices,indptr,shape,sys,inirun):
    LHS = sym.Symbol('LHS')
    #init_printing(use_unicode=True)

    string = ''
    string_xy = ''
    string_up = ''
    string_num = ''
    
    rhs_list = []
    

    for irow in range(len(indptr)-1):
        for k in range(indptr[irow],indptr[irow+1]):
            icol = indices[k]
            data_k = data[k]
            if not data[irow] == 0:
                string_sym = sym.ccode(data_k) + ';\n'
                string_i = sym2xyup(string_sym,sys,inirun)

                tipo = 'num'
                if 'x[' in string_i or 'y[' in string_i:
                    tipo = 'xy' 
                elif 'p[' in string_i or 'u[' in string_i or 'Dt' in string_i:
                    tipo = 'up' 
               
                rhs_list += [(string_i,tipo,irow,icol)]
                
    return rhs_list

def rhs2str(rhs_list,lhs_name,shape,mode='crs'):
    string_xy = ''
    string_up = ''
    string_num = ''
    N_col = shape[1]

    k = 0    
    for data_i,tipo,irow,icol in rhs_list:
        if mode == 'crs':
            idx = k
        if mode == 'dense':
            idx = irow*N_col+icol
        if mode == '2d':
            idx = f'{irow},{icol}'
            
        if tipo == 'xy':
            string_xy += f'{lhs_name}[{idx}] = {data_i}'
        if tipo == 'up':
            string_up += f'{lhs_name}[{idx}] = {data_i}'
        if tipo == 'num':
            string_num += f'{lhs_name}[{idx}] = {data_i}'  
        k+=1
                
    return string_xy,string_up,string_num
        

def str2src(fun_name,matrix_xy,matrix_up,matrix_num,matrix_name='out'):
   

    defs = ''
    defs += f'void {fun_name}_xy_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt);' + '\n' 
    defs += f'void {fun_name}_up_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt);' + '\n' 
    defs += f'void {fun_name}_num_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt);' + '\n' 
        
    source = '' 
    source += f'void {fun_name}_xy_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt)' + '{' +'\n'*2
    source += string_xy
    source += '\n}\n\n'
    source += f'void {fun_name}_up_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt)'  + '{'+ '\n'*2
    source += string_up
    source += '\n}\n\n'
    source += f'void {fun_name}_num_eval(double *{matrix_name},double *x,double *y,double *u,double *p,double Dt)'  + '{'+ '\n'*2
    source += string_num
    source += '\n}\n\n'
    
    return defs,source


## de_jac_ini
defs_f_ini,source_f_ini = sym2str('f_ini',sys['f'],sys,'ini')
defs_g_ini,source_g_ini = sym2str('g_ini',sys['g'],sys,'ini')




# In[31]:


105**2


# In[13]:


defs_f_ini,source_f_ini = sym2str('f_ini',sys['f'],sys,'ini')
defs_g_ini,source_g_ini = sym2str('g_ini',sys['g'],sys,'ini')

defs_f_run,source_f_run = sym2str('f_run',sys['f'],sys,'run')
defs_g_run,source_g_run = sym2str('g_run',sys['g'],sys,'run')

defs_h,source_h = sym2str('h',sys['h'],sys,'run')

sp_jac_ini_list = _doktocsr(SparseMatrix(jac_ini))

data = sp_jac_ini_list[0]
indices = sp_jac_ini_list[1]
indptr = sp_jac_ini_list[2]
shape = sp_jac_ini_list[3]

t_0 = time.time()
#sym2rhs(data,indices,indptr,shape,sys,inirun)
rhs_list = sym2rhs(data,indices,indptr,shape,sys,'ini')       
print(time.time()-t_0)

defs_de_ini,source_de_ini = str2src('de_jac_ini',string_xy,string_up,string_num,matrix_name='out')
#rhs2str(rhs_list,lhs_name,shape,mode='crs')
string_xy,string_up,string_num = rhs2str(rhs_list,'out',shape,mode='dense')

string_xy,string_up,string_num = rhs2str(rhs_list,'out',shape,mode='crs')
defs_sp_ini,source_sp_ini = str2src('sp_jac_ini',string_xy,string_up,string_num,matrix_name='out')

defs = defs_de_ini + defs_sp_ini
source = source_de_ini + source_sp_ini

sp_jac_trap_list = _doktocsr(SparseMatrix(jac_trap))

data = sp_jac_trap_list[0]
indices = sp_jac_trap_list[1]
indptr = sp_jac_trap_list[2]

t_0 = time.time()
rhs_list = sym2rhs(data,indices,indptr,shape,sys,'run')       
print(time.time()-t_0)

string_xy,string_up,string_num = rhs2str(rhs_list,'out',shape,mode='dense')
defs_de_run,source_de_run = str2src('de_jac_trap',string_xy,string_up,string_num,matrix_name='out')

string_xy,string_up,string_num = rhs2str(rhs_list,'out',shape,mode='crs')
defs_sp_run,source_sp_run = str2src('sp_jac_trap',string_xy,string_up,string_num,matrix_name='out')

defs = defs_f_ini + defs_g_ini + defs_f_run + defs_g_run + defs_h + defs_de_ini + defs_sp_ini + defs_de_run + defs_sp_run
source = source_f_ini + source_g_ini + source_f_run + source_h +source_g_run+ source_de_ini + source_sp_ini + source_de_run + source_sp_run


# In[19]:


jac_ini.shape


# In[14]:


import cffi

ffi = cffi.FFI()
ffi.cdef(defs, override=True)
ffi.set_source(module_name="mod5",source=source)
t_0 = time.time()
ffi.compile()
print(time.time()-t_0)


# In[ ]:


defs = ''    
defs += 'void sp_jac_trap_xy_eval(double *out,double *x,double *y,double *u,double *p,double Dt);' + '\n' 
defs += 'void sp_jac_trap_up_eval(double *out,double *x,double *y,double *u,double *p,double Dt);' + '\n' 
defs += 'void sp_jac_trap_num_eval(double *out,double *x,double *y,double *u,double *p,double Dt);' + '\n' 

source = ''    
source += 'void sp_jac_trap_xy_eval(double *out,double *x,double *y,double *u,double *p,double Dt){' + '\n'*2
source += 'out[0][0] = 0.0;\n'
source += '\n}\n'


# In[103]:


ffi.cdef(defs, override=True)
ffi.set_source(module_name="test",source=source)
ffi.compile()


# In[14]:


import mod4 as jacs

cffi_support.register_module(jacs)
sp_jac_trap_xy_eval_c = jacs.lib.sp_jac_trap_xy_eval
sp_jac_trap_up_eval_c = jacs.lib.sp_jac_trap_up_eval
sp_jac_trap_num_eval_c = jacs.lib.sp_jac_trap_num_eval

@nb.njit("float64[:](float64[:,:],float64[:],float64[:],float64[:],float64[:],float64)")
def jac_trap_xy_eval(J_d,x,y,u,p,Dt):   
        
    J_d_c_ptr=ffi.from_buffer(np.ascontiguousarray(J_d))
    x_c_ptr=ffi.from_buffer(np.ascontiguousarray(x))
    y_c_ptr=ffi.from_buffer(np.ascontiguousarray(y))
    u_c_ptr=ffi.from_buffer(np.ascontiguousarray(u))
    p_c_ptr=ffi.from_buffer(np.ascontiguousarray(p))
    
    sp_jac_trap_xy_eval_c(J_d_c_ptr,x_c_ptr,y_c_ptr,u_c_ptr,p_c_ptr,Dt)
    return J_d


# In[104]:


J_d = np.ones((500,500),dtype=np.float64)
x = np.ones(1000,dtype=np.float64)
y = np.ones(1000,dtype=np.float64)
u = np.ones(1000,dtype=np.float64)
p = np.ones(2000,dtype=np.float64)
Dt = 0.02
jac_trap_xy_eval(J_d,x,y,u,p,Dt)


# In[107]:


import cffi
import numpy as np

ffi = cffi.FFI()
ffi.cdef("""
    extern double dist(const double s[3][3], const double t[3][3]);
""")
lib = ffi.dlopen("./dist.so")

S = np.array([[-1.63538,  0.379116, -1.16372],[-1.63538, 0.378137, -1.16366 ],[-1.63193, 0.379116, -1.16366]], dtype=np.float32)
T = np.array([[-1.6467834, 0.3749715, -1.1484985],[-1.6623441, 0.37410975, -1.1647063 ],[-1.6602284, 0.37400728, -1.1496595 ]], dtype=np.float32)
Sp = ffi.cast("double(*) [3]", S.ctypes.data)
Tp = ffi.cast("double(*) [3]", T.ctypes.data)

dd = lib.dist(Sp,Tp);


# In[16]:


import numpy as np
import numba as nb
#from numba import cffi_support
import numba.core.typing.cffi_utils as cffi_support
import cffi
ffi = cffi.FFI()
import mod4 as jacs

cffi_support.register_module(jacs)
sp_jac_trap_xy_eval_c = jacs.lib.sp_jac_trap_xy_eval
sp_jac_trap_up_eval_c = jacs.lib.sp_jac_trap_up_eval
sp_jac_trap_num_eval_c = jacs.lib.sp_jac_trap_num_eval

@nb.njit("float64[:](float64[:],float64[:],float64[:],float64[:],float64[:],float64)")
def sp_jac_trap_xy_eval(J_d,x,y,u,p,Dt):   
        
    J_d_c_ptr=ffi.from_buffer(np.ascontiguousarray(J_d))
    x_c_ptr=ffi.from_buffer(np.ascontiguousarray(x))
    y_c_ptr=ffi.from_buffer(np.ascontiguousarray(y))
    u_c_ptr=ffi.from_buffer(np.ascontiguousarray(u))
    p_c_ptr=ffi.from_buffer(np.ascontiguousarray(p))
    
    sp_jac_trap_xy_eval_c(J_d_c_ptr,x_c_ptr,y_c_ptr,u_c_ptr,p_c_ptr,Dt)
    return J_d

@nb.njit("float64[:](float64[:],float64[:],float64[:],float64[:],float64[:],float64)")
def sp_jac_trap_up_eval(J_d,x,y,u,p,Dt):   
        
    J_d_c_ptr=ffi.from_buffer(np.ascontiguousarray(J_d))
    x_c_ptr=ffi.from_buffer(np.ascontiguousarray(x))
    y_c_ptr=ffi.from_buffer(np.ascontiguousarray(y))
    u_c_ptr=ffi.from_buffer(np.ascontiguousarray(u))
    p_c_ptr=ffi.from_buffer(np.ascontiguousarray(p))
    
    sp_jac_trap_up_eval_c(J_d_c_ptr,x_c_ptr,y_c_ptr,u_c_ptr,p_c_ptr,Dt)
    return J_d

@nb.njit("float64[:](float64[:],float64[:],float64[:],float64[:],float64[:],float64)")
def sp_jac_trap_num_eval(J_d,x,y,u,p,Dt):   
        
    J_d_c_ptr=ffi.from_buffer(np.ascontiguousarray(J_d))
    x_c_ptr=ffi.from_buffer(np.ascontiguousarray(x))
    y_c_ptr=ffi.from_buffer(np.ascontiguousarray(y))
    u_c_ptr=ffi.from_buffer(np.ascontiguousarray(u))
    p_c_ptr=ffi.from_buffer(np.ascontiguousarray(p))
    
    sp_jac_trap_num_eval_c(J_d_c_ptr,x_c_ptr,y_c_ptr,u_c_ptr,p_c_ptr,Dt)
    return J_d


J_d = np.ones(500,dtype=np.float64)
x = np.ones(1000,dtype=np.float64)
y = np.ones(1000,dtype=np.float64)
u = np.ones(1000,dtype=np.float64)
p = np.ones(2000,dtype=np.float64)
Dt = 0.02
sp_jac_trap_xy_eval(J_d,x,y,u,p,Dt)
sp_jac_trap_up_eval(J_d,x,y,u,p,Dt)
sp_jac_trap_num_eval(J_d,x,y,u,p,Dt)


# In[119]:


from sympy.printing.c import C99CodePrinter
printer = C99CodePrinter()
#print(printer.doprint(jac_trap))
rhs_result = sym.MatrixSymbol('out', jac_trap.shape[0], jac_trap.shape[1])
#print(printer.doprint(jac_trap, assign_to=rhs_result))
print(rhs_result)


# In[ ]:


#include <stdio.h>
void print(int *arr, int m, int n)
{
    int i, j;
    for (i = 0; i < m; i++)
      for (j = 0; j < n; j++)
        printf("%d ", *((arr+i*n) + j));
}
 
int main()
{
    int arr[][3] = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}};
    int m = 3, n = 3;
 
    // We can also use "print(&arr[0][0], m, n);"
    print((int *)arr, m, n);
    return 0;
}


# In[ ]:





# In[42]:


def getIndex(s, i): 
  
    # If input is invalid. 
    if s[i] != '(':
        return -1
  
    # Create a deque to use it as a stack. 
    d = deque() 
  
    # Traverse through all elements 
    # starting from i. 
    for k in range(i, len(s)): 
  
        # Pop a starting bracket 
        # for every closing bracket 
        if s[k] == ')': 
            d.popleft() 
  
        # Push all starting brackets 
        elif s[k] == '(': 
            d.append(s[i]) 
  
        # If deque becomes empty 
        if not d: 
            return k 
  
    return -1
  
def arg2np(string,function_name):
    idx_end = 0
    for it in range(3):
        if function_name in string[idx_end:]:
            #print(string[idx_end:])
            idx_ini = string.find(f'{function_name}(',idx_end)+len(f'{function_name}(')
            idx_end = getIndex(string, idx_ini-1)
            string = string.replace(string[idx_ini:idx_end],f'np.array([{string[idx_ini:idx_end]}])')
    else: pass
    return string   

def arg2cp(string,function_name,i_pwise):
    idx_end = 0
    for it in range(3):
        if function_name in string[idx_end:]:
            #print(string[idx_end:])
            idx_ini = string.find(f'{function_name}(',idx_end)+len(f'{function_name}(')
            idx_end = getIndex(string, idx_ini-1)
            string_inline = string.replace(string[idx_ini:idx_end],'pwise[0]').replace(f'{function_name}(','').replace(')','')
            string_pwise = string[idx_ini:idx_end]
    else: pass
    return string_pwise,string_inline 


# In[120]:


import cffi
import numpy as np

ffi = cffi.FFI()
ffi.cdef("""
    extern double dist(const double s[3][3], const double t[3][3]);
""")
lib = ffi.dlopen("./dist.so")

S = np.array([[-1.63538,  0.379116, -1.16372],[-1.63538, 0.378137, -1.16366 ],[-1.63193, 0.379116, -1.16366]], dtype=np.float32)
T = np.array([[-1.6467834, 0.3749715, -1.1484985],[-1.6623441, 0.37410975, -1.1647063 ],[-1.6602284, 0.37400728, -1.1496595 ]], dtype=np.float32)
Sp = ffi.cast("double(*) [3]", S.ctypes.data)
Tp = ffi.cast("double(*) [3]", T.ctypes.data)

dd = lib.dist(Sp,Tp);


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[45]:


from collections import deque 

string = str(sys['g'][-3])


# In[47]:


string_pwise,string_inline =  arg2cp(string,'Piecewise',0)
string_pwise_list = string_pwise.split(',')


# In[50]:


string_pwise_list

for it in range(int(len(string_pwise_list)/2)):
    string_pwise_list[2*it] = string_pwise_list[2*it][1:] 
    string_pwise_list[2*it+1] = string_pwise_list[2*it+1][:-1] 
    
    
string_pwise_list    


# In[ ]:




