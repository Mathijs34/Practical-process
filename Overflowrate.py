import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import scipy.optimize as optimize
"""
V = N_L_tot * Vm_L
Vm_L = (Nme_L/N_L_tot) * Vm_me * (Niso_L/N_L_tot) * Vm_iso
Vm_me = M_Me/1000/dens_Me
Vm_iso = M_Iso/1000/dens_Iso
"""
#tube: 3/8" x 22 swg
A_tube = 0.25 * 8.103 *1e-3 * np.pi
g = 9.81

"""Import H_r in code"""

def Overflow(V):
    A_tube = 0.25 * 8.103 * 1e-3 * np.pi #3/8" x 22 SWG
    g = 9.81
    V_max = 0.00484*np.pi #m^3
    depth_reboiler = 400 #mm
    r_reboiler = 110 #mm
    

    if V<0:
        return 0
    elif V>V_max:
        return np.sqrt(2*g*((110)*1e-3)) * A_tube
    else:
        S = V*1e9/depth_reboiler #1e9 to convert to mm^3
        def w(x):
            return 2 * (2*r_reboiler*x-x**2)**(1/2)

        def integral(x,S):
            result, _ = quad(w,0,x)
            return result - S

    
        x_initial = r_reboiler
        x_solution = optimize.fsolve(integral, x_initial, args=(S,), maxfev=800)
        h = x_solution[0]
        if h < 110:
            flow = 0
        else:
            flow = np.sqrt(2*g*((h-110)*1e-3)) * A_tube
        return flow




def overflow1(x):
    if x<110:
        return 0
    else: 
        return np.sqrt(2*g*((x-110)*1e-3)) * A_tube

V_max2 = 0.00484*np.pi


x2 = np.linspace(0,1.2*V_max2)
y2 = [Overflow(x2) for x2 in x2]
plt.plot(x2,y2, c="r")
plt.xlabel("Volume [m^3]")
plt.ylabel("Overflowrate [m^3/s]")
plt.title("Overflowrate")
plt.show()


x = np.linspace(0,220)
y = [overflow1(x) for x in x]
plt.plot(x,y)
plt.show()
                
print(H_r(0.00484*np.pi*0.5))

Area_tray = ((50 * 1e-3) ** 2) * 0.25* np.pi

print(Area_tray)
