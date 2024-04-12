import math

# Given 
Fap = 1500
Xao = 0
Xaf = 0.6
T = 1073
P = 5
k1 = 0.072
Ea = 82
rho_a = 0.362
mu_a = 0.000874

Fao = Fap/0.6
k2 = k1*math.exp(-Ea/(0.00199*1073))/math.exp(-Ea/(0.00199*1000))
Vao = Fao*30/rho_a
V_PFR = (Vao/(k2*3600))*math.log((1-Xao)/(1-Xaf))
L = (36*V_PFR/math.pi)**(1/3)
D = L/3
S_T = V_PFR/(Vao/3600)
S_V = 1/S_T
T_R = ((P*101325*(D/2))/((96e6*0.85)+(0.6*P*101325)))+0.003
Q = 136.96*Xaf*(Fao/3600)
Hr = Q/V_PFR
Re = ((Fap*28/(3600*math.pi*D*D/4))*D)/mu_a
Jh = 0.027/(Re**0.2)
del_P = 4*Jh*3*rho_a*(((Vao/3600)/(math.pi*D*D/4))**2)

print(f'''
Reaction : Cracking of ethane to form ethene
T = 1073 K or 800 °C
P = 5 atm
Conversion = {Xaf}
Reactor Volume = {V_PFR} m³
Length of reactor = {L} m
Diameter of reactor = {D} m
Space Time = {S_T} s
Space Velocity = {S_V} 1/s
Reactor Thickness = {T_R} m
Heat Load = {Q} kJ.Kmol/s
Heat genearted per unit volume of reactor = {Hr} kJ.Kmol/m³-s
Pressure drop along length of reactor = {del_P} Pa/m
''')