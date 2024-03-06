import math

# Given
F = 25000/3600 #kg/s
C_F, C_L = 0.05,0.35
T_F = 30 # °C
P_S = 2.5 * 101325 # Pa
T_S = 127.85 # °C
P_Evaporator = (760 - 600) * 133.322 # Pa
T_Evaporator = 61.457 # °C
Cp_F = 3700 # J/kg°C
Cp_L = 3200 # J/kg°C
T1 = T_Evaporator+5 # °C
H_S = 2717106 # J/kg
H_V = 2611378 # J/kg
U = 1500 # W/m²-°C

# Calculation
L = F*0.05/0.35 # kg/s
V = F-L # kg/s
S = ((V*H_V) + (F*Cp_F*(T1-T_F)))/H_S # kg/s
del_T = T_S - T1 # °C
Q = S*H_S # J/s
A = Q/(U*del_T) # m²
tube_OD = 1*0.0254 # 1 inch --> m
tube_L = 4.88 # m
pitch = 1.25 * 0.0254 # 1.25 inch --> m

N = A/(math.pi*tube_OD*tube_L)
A_actual = N*pitch*pitch*math.sin(math.pi/3)/0.7 # sq-m
A_downcomer = 0.4*A_actual # m²
A_total = A_actual+A_downcomer # m²
D_shell = math.sqrt(4*A_total/math.pi) # m
D_downcomer = math.sqrt(4*A_downcomer/math.pi) # m
H_column = tube_L+(1.5*D_shell) # m

print(f"""
Product Flow Rate = {L} kg/s
Vapor Flow Rate = {V} kg/s
Steam Flow Rate = {S} kg/s

del_T = {del_T} °C
Area calculated from overall HTC = {A} m²
Assuming 1" O.D. Tubes of 4.88m long, on a 1 1/4" triangular pitch
Number of tubes = {N}
Actual area (from number of tubes) = {A_actual} m²
Downcomer area = {A_downcomer} m²
Total area = {A_total} m²

Shell diameter = {D_shell} m
Downcomer diameter = {D_downcomer} m
Height of column = {H_column} m
""")