import math

# Given
Xf = 0.5
Xd = 0.9
Xb = 0.05
T = 30 #°C
P = 1 # atm ~ bar
F = 10000 #kg/hr
lambda_w = 41360 # J/mol
lambda_a = 28410 # J/mol
Cp_w = 75.3 #J/mol°C
Cp_a = 128 # J/mol°C
plate_spacing = 0.4 # m
del_P_per_plate = 1250 # Pa
efficiency = 0.7
BP_a = 56 # °C
BP_w = 100 # °C

#Calculations
D = ((F*Xf)-(F*Xb))/(Xd-Xb) 
B = F-D 
BP_mix = 60 
lambda_avg = Xf*lambda_a +(1-Xf)*Cp_w 
Cp_avg = Xf*Cp_a+(1-Xf)*Cp_w 

q = (Cp_avg*(BP_mix-T)+lambda_avg)/lambda_avg
R = 0.25
N_stages = 6.2
N_trays = math.ceil(N_stages-1) # Since reboiler is a stage
N_trays_actual = math.ceil(N_trays/efficiency)
H_column = (N_trays_actual*plate_spacing)+1 

Mol_wt_avg = (18+58)/2
Molar_flow_rate = F/Mol_wt_avg

D_molar = (F/Mol_wt_avg)*(Xf/Xd)
B_molar = (F/Mol_wt_avg)-D_molar

Mol_wt_d = Xd*58+(1-Xd)*18
V = D_molar*(1+R)
L = R*D_molar

slope_top_line = L/V
slope_bottom_line = 1.756
V_dash = B_molar/(slope_bottom_line-1)
L_dash = V_dash+B_molar

del_p_column = (del_P_per_plate*N_trays_actual)/1e5

P_bottom = P+del_p_column

# For Top
rho_vapor_top = (P*100*Mol_wt_d)/(8.314*(273+BP_mix))
rho_liquid_top = Xf*750+(1-Xf)*1000
sigma_top = 23e-3 
F_lv_top = (L/V)*math.sqrt(rho_vapor_top/rho_liquid_top)
K1_top = 0.0802

U_flooding_top = K1_top*math.sqrt((rho_liquid_top-rho_vapor_top)/rho_vapor_top)
Q_top = (V/rho_vapor_top)*(Mol_wt_d/3600) 
Uv_dash_top = U_flooding_top*efficiency

top_area = Q_top/Uv_dash_top
Ac_top = top_area/0.88

# For base
rho_vapor_base = (P_bottom*100*18)/(8.314*376.11)
rho_liquid_base = 956.211
sigma_base = 57e-3 
F_lv_base = (L_dash/V_dash)*math.sqrt(rho_vapor_base/rho_liquid_base)
K1_base = 0.0714

U_flooding_base = K1_base*math.sqrt((rho_liquid_base-rho_vapor_base)/rho_vapor_base)
Q_base = (V/rho_vapor_base)*(18/3600) 
Uv_dash_base = U_flooding_base*efficiency

base_area = Q_base/Uv_dash_base
Ac_base = top_area/0.88

D_column = math.sqrt((4*max(Ac_top,Ac_base))/math.pi)

Ah = (max(Ac_base,Ac_top)-(2*max(Ac_base,Ac_top)*0.12))*0.1
dh = 0.005
N_holes = Ah/(math.pi*dh*dh/4)

print(f'''
Feed flow rate = {F} kg/hr
Bottom product flow rate = {B} kg/hr
Distillate flow rate = {D} kg/hr

As feed is sub-cooled liquid, q>1
q = {q}

From McCabe-Thiele diagram,
Rmin = 0.154 
R = {R}
Number of stages = {N_stages}
Number of trays = {N_trays}
Actual number of trays = {N_trays_actual}
Slope of rectifying operating line = {slope_bottom_line}
Slope of stripping operating line = {slope_top_line}

Pressure at tower top = {P} bar
Pressure at tower bottom = {P_bottom} bar

Tower Top operating Velocity = {Uv_dash_top} m/s
Tower bottom operating velocity = {Uv_dash_base} m/s

Base area of column = {Ac_base} m²
Top area of column = {Ac_top} m²

Area of column = {max(Ac_base,Ac_top)} m²
Column diameter = {D_column} m
Height of Column = {H_column} m
No. of holes = {N_holes}
''')