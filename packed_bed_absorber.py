import math

y1 = 0.05
y2 = 0.005
G = 1000 #kmol/hr-m²
Gs = 950 #kmol/hr-m²
Kga = 300 #kmol/hr-m³-atm
Y1 = y1/(1-y1)
Y2 = y2/(1-y2)
X2 = 0
X1_star = (y1/0.27)/(1-(y1/0.27))
Ls_min = (Gs*(Y1-Y2))/(X1_star-X2) #kmol/hr-m²
Ls_actual = 2*Ls_min # kmol/hr-m²
X1 = (Gs*(Y1-Y2)/Ls_actual)+X2
x1_star = X1/(1-X1)
y1_star = 0.27*x1_star
Y1_star = (y1_star)/(1-(y1_star))
NTU = ((Y1-Y2)/((Y1-Y1_star)-(Y2-0)))/math.log((Y1-Y1_star)/(Y2-0))

rho_feed = 0.0759 #lb/ft³
rho_absorbent = 62.677 #lb/ft³
mu_absorbent = 2.0355 #cp
Flv = (Ls_actual/Gs)*math.sqrt(rho_feed/rho_absorbent)
U_flooding = math.sqrt((Flv*64.301*(0.73**3)*32.2)/(58*0.0759*(2.0355**0.2))) # ft/s
U_operating = U_flooding*0.5 #ft/s

V = G*0.0821*298*0.001 # m³/m²-hr
A = V/(U_operating*1097) # m

D = math.sqrt(4*A/math.pi) # m
HTU_OG = G/Kga # m
H = HTU_OG*math.ceil(NTU) # m
H_practical = H+(0.2*H) # m

print(
f'''
Y1 : {Y1}
Y2 : {Y2}
X2 : 0
X1* : {X1_star}
Ls_min : {Ls_min} kmol/hr-m²
Ls_actual : {Ls_actual} kmol/hr-m²
X1 : {X1}
Y1* : {Y1_star}

NTU : {NTU}

Flv : {Flv}
Flooding velocity : {U_flooding} ft/s
Operating Velocity : {U_operating} ft/s

Total gas flow rate : {V} m³/m²-hr
Cross sectional area of tower : {A} m
Column diameter : {D} m

HTU : {HTU_OG}
Calculated height of Tower : {H} m
Practical tower height (assuming 20% excess space): {H_practical} m
'''
)