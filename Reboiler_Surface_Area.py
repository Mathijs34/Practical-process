import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad #<------ add to model
import scipy.optimize as optimize #<------ add to model
from scipy.integrate import trapz

#\/\/add to model\/\/#

def A_r(V):
    """
    Input: total liquid [m^3], ouput: liquid surface
    V_max = 0.00484*pi m^3
    V<0 -> 0, V>V_max -> A_tube
    At certain volume ~0.01428 area will be area of column
    """
    V_max = 0.00484*np.pi #m^3
    depth_reboiler = 400 #mm
    r_reboiler = 110 #mm
    A_tube = 0.25 * 57**2 * np.pi

    if V<0:
        return 0
    elif V>V_max:
        return A_tube * 1e-6
    else:
        S = V*1e9/depth_reboiler #1e9 to convert to mm^3
        def w(x):
            return 2 * (2*r_reboiler*x-x**2)**(1/2)

        def integral(x,S):
            result, _ = quad(w,0,x)
            return result - S

    
        x_initial = r_reboiler
        x_solution = optimize.fsolve(integral, x_initial, args=(S,), maxfev=800)
        width = w(x_solution[0])
        if x_solution > 195:
            Area =  A_tube # once the liquid reaches the column tube the usefull area is reduced
        else:
            Area = width * depth_reboiler
        return Area * 1e-6 #convert to m^2

#/\/\add to model/\/\#

V = 0.00242*np.pi*0.7 #mm^2 This should be total liquid volume in reboiler
print(A_r(V))


V_max = 0.00484*np.pi
x = np.linspace(-0.1*V_max,1.1*V_max,1000)
y = [A_r(x) for x in x]
plt.plot(x,y)
plt.title("Liquid Area in Reboiler")
plt.xlabel("Volume [m]")
plt.ylabel("Area [m^2]")
plt.grid(1)
plt.show()
