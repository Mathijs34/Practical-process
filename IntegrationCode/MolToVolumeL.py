import numpy as np
import matplotlib.pyplot as plt

dens_me = 1
dens_iso = 1
M_me = 1
M_iso = 1
Vm_me = M_me/1000/dens_me
Vm_iso = M_iso/1000/dens_iso

Nme_L = 1
Niso_L = 1
N_L_tot = Nme_L + Niso_L

#\/\/add to model]\/\/#

Vm_L = Vm_me * (Nme_L/N_L_tot) + Vm_iso * (Niso_L/N_L_tot)
V_L_tot = Vm_L * N_L_tot 