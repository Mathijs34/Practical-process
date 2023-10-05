import numpy as np
import matplotlib.pyplot as plt

#Cp at 1 bar in J/(mol*K)
Temperature = [50,100,150,200,273.15,298.15,300,400,500,600,700]
Cp_v_Me_data = [34,36.95,38.64,39.71,42.59,44.06,44.17,51.63,59.7,67.19,73.86]
Cp_v_Iso_data = [35.32,46.04,57.98,68.28,83.72,89.32,89.74,112.15,131.96,148.3,161.75]

a_Me_v, b_Me_v, c_Me_v = np.polyfit(Temperature, Cp_v_Me_data, deg=2)
a_Iso_v, b_Iso_v, c_Iso_v = np.polyfit(Temperature, Cp_v_Iso_data, deg=2)
K = np.linspace(0, 1000)
plt.plot(Temperature, Cp_v_Me_data,"o")
plt.plot(Temperature, Cp_v_Iso_data, "o")
plt.plot(K, np.polyval((a_Me_v,b_Me_v,c_Me_v), K))
plt.plot(K, np.polyval((a_Iso_v,b_Iso_v,c_Iso_v), K))
plt.show()

print(a_Me_v, b_Me_v, c_Me_v)
print(a_Iso_v, b_Iso_v, c_Iso_v)





##\/\/\/\/PUT THIS IN MODEL CODE\/\/\/\/###
def Cp_v_Me(T):
    Cp_v_Me =  4.853229866724107e-05*T**2 + 0.026393190719809542*T + 32.831657334235835
    return Cp_v_Me
def Cp_v_Iso(T):
    Cp_v_Iso = -6.900678097360619e-05*T**2 + 0.250658478269019*T + 21.727358906262694
    return Cp_v_Iso
def Cp_mix_y(Me_frac,T):
    Cp_mix_y = Me_frac*Cp_v_Me(T) + (1-Me_frac)*Cp_v_Iso(T)
    return Cp_mix_y
###/\/\/\/\PUT THIS IS MODEL CODE/\/\/\/\###





Me_frac = 0.5
plt.plot(K,Cp_v_Me(K))
plt.plot(K,Cp_v_Iso(K))
plt.plot(K,Cp_mix_y(Me_frac,K))
plt.show()


