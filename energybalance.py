import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import odeint

## Energy Balance Reboiler

df_Me = pd.read_excel(r'c:\Users\20211782\OneDrive - TU Eindhoven\Documents\Cp_methanol.xlsx')
df_Iso = pd.read_excel(r'c:\Users\20211782\OneDrive - TU Eindhoven\Documents\Cp_isopropanol.xlsx')

# Heat Capacity Methanol

# Getting data from file and making fitted line
Temp_list_Me = df_Me['Temperature'].values.tolist()
Cp_list_Me = df_Me['Cp'].values.tolist()
a_Me, b_Me, c_Me = np.polyfit(Temp_list_Me, Cp_list_Me, deg=2)

'''plt.plot(Temp_list_Me, Cp_list_Me, "o")
plt.plot(Temp_list_Me, np.polyval((a_Me, b_Me, c_Me),Temp_list_Me), "-")
plt.xlabel('T[K]')
plt.ylabel('Cp') 
plt.title('Methanol heat capacity')
plt.show()'''

# Heat Capacity Isopropanol

# Getting data and making fitted line
Temp_list_Iso = df_Iso['Temp'].values.tolist()
Cp_list_Iso = df_Iso['Cp'].values.tolist()
a_Iso, b_Iso, c_Iso = np.polyfit(Temp_list_Iso, Cp_list_Iso, deg=2)
Temps_Iso_model = np.linspace(-20, 85, 22)
Temps_Iso_model_K  = [x+273.15 for x in Temps_Iso_model] # convert to Kelvin

'''plt.plot(Temp_list_Iso, Cp_list_Iso, "o")
plt.plot(Temps_Iso_model_K, np.polyval((a_Iso, b_Iso, c_Iso), Temps_Iso_model_K), "-")
plt.xlabel('T[K]') # label on the x axis
plt.ylabel('Cp') # label on the y axis
plt.title('Isopropanol heat capacity')
plt.show()'''

# Refractive Index Calibration Curve

#Measurements
Me_fraction = [0, 0.1, 0.3, 0.5, 0.7, 0.9, 1]
RI = [1.3765, 1.374, 1.369, 1.360, 1.3495, 1.342, 1.328]

#fitting line at multiple degrees
Cal_a_fit, Cal_b_fit = np.polyfit(RI, Me_fraction, deg=1)
Cal_a_fit2, Cal_b_fit2, Cal_c_fit2 = np.polyfit(RI, Me_fraction, deg=2)

plt.plot(RI, Me_fraction,"o")
plt.plot(RI, np.polyval((Cal_a_fit, Cal_b_fit), RI),"-")
plt.plot(RI, np.polyval((Cal_a_fit2, Cal_b_fit2, Cal_c_fit2), RI), "--")
plt.xlabel("RI")
plt.ylabel("Methanol fraction")
plt.title('Calibration curve')
plt.show()

def Calibration(RI):
    Me_ratio = RI**2*Cal_a_fit2 + RI*Cal_b_fit2 + Cal_c_fit2
    return Me_ratio

#use calibration function to get the methanol fraction
Me_frac = Calibration(1.338)
print(Me_frac)

def Cp_Iso(T):
    Cp_Iso = a_Iso * T**2 + b_Iso*T + c_Iso
    return Cp_Iso

def Cp_Me(T):
    Cp_Me = a_Me * T**2 + b_Me * T + c_Me
    return Cp_Me

def Cp_mix(Me_frac,T):
    Cp_mix = Me_frac*Cp_Me(T) + (1-Me_frac)*Cp_Iso(T)
    return Cp_mix

# Constants
dH_vap_Me = 35300 # Enthalpy of vaporisation methanol at boiling point [J/mol]
eff = 640/751 # Heater efficiency (around 0.85)
T0 = 298 #K
V  = 0.01 # Volume of mixture in reboiler [m^3]
Iso_frac = 1-Me_frac # Mole fraction isopropanol
dens_Me = 792 #kg/m3
dens_Iso = 786 #kg/m3
M_Me = 32.02 #g/mol
M_Iso = 60.1 #g/mol
Vm_Me = 40.75 # molar volume methanol [cm^3/mol]
Vm = (M_Me/1000/dens_Me)*Me_frac + (M_Iso/1000/dens_Iso)*(1-Me_frac) # Molar volume of mixture [m^3/mol]
n_total = V/Vm # Total number of moles in mixture
n_Me = Me_frac*n_total # Number of moles of methanol
n_Iso = Iso_frac*n_total # Number of moles of isopropanol
dens_mix = (n_Me*M_Me + n_Iso*M_Iso)/V # Density of mixture [kg/m^3]
M_mix = (n_Me*M_Me + n_Iso*M_Iso)/1000 #kg/mol
power_percent = 0.5
power = eff*power_percent*2000 #J/s (maximum power is 2kW)
params = {
    'Me_frac': Me_frac,   
    'n_total': n_total,
    'power': power
}


def model(T,t, params):
    n_total = params['n_total']
    Me_frac = params['Me_frac']
    power = params['power']
    if T<337.8:
        dTdt = (power)/(Cp_mix(Me_frac,T)*n_total)
    else:
        dTdt=0
    return dTdt

t = np.linspace(0, 1000)

# Solve the ODE using odeint
y = odeint(model, T0, t, args=(params,))

plt.plot(t, y, "h", mfc='none', label='y(t) odeint', c="magenta")
plt.axhline(337.8, c="b") # boiling point methanol
plt.axhline(355.6, c="r") # boiling point isopropanol
plt.xlabel("t(s)")
plt.ylabel("T(K)")
plt.title("Mixture warming up", c="navy")
plt.grid(1)
plt.show()

# Time needed to evaporate all methanol (after boiling point is reached)
t_evap = n_Me*dH_vap_Me/power
print(t_evap)

boilup_rate = n_Me*Vm_Me/t_evap
print(boilup_rate)