# Simulation

```
import smib
model = smib.model()
```



```
model.ini({},'xy_0.json')
model.run( 1.0,{'v_ref_1':1.0})
model.run( 15.0,{'v_ref_1':1.02})

model.post();
```


 

```
model = smib.model()
model.Dt = 0.01

Δt = 0.5  #  
times = np.arange(0,30,Δt)   # times for which the control will be executed 
                             # (in this case, the simulation will be for 30 s)

# initialization
model.ini({},'xy_0.json')

# save initial values
v_ref_1_0 = model.get_value('v_ref_1')

# simulation loop
for it,t in enumerate(times):
    
    # a change is applied at t = 1.0
    v_ref_1 = v_ref_1_0
    if t>1.0: 
        v_ref_1 = v_ref_1_0*1.05
      
    # v_ref_1 is updated:  
    model.set_value({'v_ref_1':v_ref_1})

    # the simulation is run for the new time t :
    model.run(t,{})

model.post();
```
