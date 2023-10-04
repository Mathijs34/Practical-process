import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data_1 = r"C:\Users\20202055\Documents\PPT\PPT CODE\02-10-2023_semi-batch_1.csv"
data_2 = r"C:\Users\20202055\Documents\PPT\PPT CODE\04-10-2023_semi-batch_2.csv"
data_3 = r"C:\Users\20202055\Documents\PPT\PPT CODE\temp11_09batch.csv"

df = pd.read_csv(data_1)
df_2 = pd.read_csv(data_2)
df_3 = pd.read_csv(data_3)

df['TE11_PV']=df['TE11_PV'].replace(',', '.', regex=True)
df['TE11_PV']=df['TE11_PV'].astype(float)

df['TE12_PV']=df['TE12_PV'].replace(',', '.', regex=True)
df['TE12_PV']=df['TE12_PV'].astype(float)

df_2['TE11_PV']=df_2['TE11_PV'].replace(',', '.', regex=True)
df_2['TE11_PV']=df_2['TE11_PV'].astype(float)

df_2['TE12_PV']=df_2['TE12_PV'].replace(',', '.', regex=True)
df_2['TE12_PV']=df_2['TE12_PV'].astype(float)

df_3['TE11_PV']=df_3['TE11_PV'].replace(',', '.', regex=True)
df_3['TE11_PV']=df_3['TE11_PV'].astype(float)

df_3['TE12_PV']=df_3['TE12_PV'].replace(',', '.', regex=True)
df_3['TE12_PV']=df_3['TE12_PV'].astype(float)

df_3['Heater_Sp']=df_3['Heater_Sp'].replace(',', '.', regex=True)
df_3['Heater_Sp']=df_3['Heater_Sp'].astype(float)

print(df['TE11_PV'])

plt.plot(df['TE12_PV'])
plt.plot(df['TE11_PV'])
plt.plot(df_2['TE12_PV'])
plt.plot(df_2['TE11_PV'])
plt.show()

dT_cooling = [df['TE12_PV']-df['TE11_PV']]


df["dT_cooling"] = df['TE12_PV'] - df['TE11_PV']
df_2["dT_cooling"] = df_2['TE12_PV'] - df_2['TE11_PV']
df_3["dT_cooling"] = df_3['TE12_PV'] - df_3['TE11_PV']
plt.plot(df['dT_cooling'])
plt.plot(df_2['dT_cooling'])
plt.show()

plt.plot(df['TE11_PV'], c="b")
plt.plot(df['TE12_PV'], c="r")
plt.show()

Avg_dT = df.loc[8000:12000, "dT_cooling"].mean()
print("average dt =", Avg_dT)

P_cooling_old = 0.05 * 0.997* 4186 * Avg_dT
print("The average cooling power = ", P_cooling_old, "J/s")
# Unfortunately this could be a function of the heater, but it shouldn't be.

plt.plot(df_3['TE11_PV'], c="b")
plt.plot(df_3['TE12_PV'], c="r")
plt.show()
plt.plot(df_3['dT_cooling'])
plt.show()

avg_1 = df_3[df_3['Heater_Sp'] == 12.5]["dT_cooling"].mean()
avg_2 = df_3[df_3['Heater_Sp'] == 25]["dT_cooling"].mean()
avg_3 = df_3[df_3['Heater_Sp'] == 37.5]["dT_cooling"].mean()
avg_4 = df_3[df_3['Heater_Sp'] == 50]["dT_cooling"].mean()
avg_5 = df_3[df_3['Heater_Sp'] == 62.5]["dT_cooling"].mean()
avg_6 = df_3[(df_3['Heater_Sp'] == 75) & (df_3.index < 8500)]["dT_cooling"].mean()

average_dT = [avg_1, avg_2, avg_3, avg_4, avg_5, avg_6]
print(average_dT)
plt.plot(average_dT)
plt.show()

Heater_Sp = [12.5, 25, 37.5, 50, 62.5, 75]

a, b = np.polyfit(Heater_Sp, average_dT, deg=1)

plt.plot(Heater_Sp, average_dT, "o")
plt.plot(Heater_Sp, np.polyval((a, b),Heater_Sp), "-")
plt.xlabel('Heater %')
plt.ylabel('dT') 
plt.title('dT of cooling water')
plt.show()

print(a, b) # a=0.07290542757193519, b=-0.4868014781932162




####################################
### Copy Paste this in Modelfile ###
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/#

def P_cooling_curve (Heater_sp):
    P_cooling = 0.05 * 0.997 * 4186 * (0.07290542757193519*Heater_sp - 0.4868014781932162)
    return P_cooling

#/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\#
### Copy Paste this in Modelfile ###
####################################



x = np.linspace(0,100)
plt.plot(x, P_cooling_curve(x))
plt.show()

