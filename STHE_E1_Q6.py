import math

#Temperatures
T_e_in = 75 # C
T_e_out = 40 # C
T_w_in = 25 # C
T_w_out = 35 # C
corrected_LMTD = 0.9*(((T_e_in-T_w_out)-(T_e_out-T_w_in))/math.log((T_e_in-T_w_out)/(T_e_out-T_w_in)))

# Fluid properties
# Ethanol at 57.5 C
e_cp = 2960  # J/kg°C
e_rho = 789  # kg/m^3
e_mu = 0.000686  # Pa*s
e_k = 0.160  # W/m°C
e_Pr = (e_cp*e_mu)/e_k

# Water at 30 C
w_cp = 4180  # J/kg°C
w_rho = 1000  # kg/m^3
w_mu = 0.000853  # Pa-s
w_k = 0.61  # W/m°C
w_Pr = (w_cp*w_mu)/w_k

# Tube dimensions
tube_OD = 0.0254 # m
tube_ID = 0.0221 # m
tube_L = 4.88 # m

m_e = 27.77 # kg/s
Q = m_e*e_cp*(T_e_in-T_e_out) # W
m_w = Q/(w_cp*(T_w_out-T_w_in)) # kg/s

U_assumed = 140*5.6783 # W/sq.m/C
overall_heat_transfer_area = Q/(U_assumed*corrected_LMTD) # sq.m
N_tubes_calculated = overall_heat_transfer_area/(math.pi*tube_OD*tube_L)
N_tubes_practical = 454
D_shell = 31*0.0254 # m

tube_flow_area = (N_tubes_practical/2)*math.pi*(tube_ID**2)/4 #sq.m
Re_tube = (m_w/tube_flow_area)* tube_ID/ w_mu
Nu_tube = 0.023*(Re_tube**0.8)*(w_Pr**0.4)
h_tube = Nu_tube*w_k/tube_ID # W/sq.m-C

Pitch = 1.25*tube_OD # m
baffle_spacing = 0.2*D_shell # m 
effective_length = 0.8*tube_L # m
baffle_length = 0.75*D_shell # m
N_baffles = (effective_length/baffle_spacing)-1

D_shell_effective = ((4*Pitch*Pitch*0.866) - (math.pi*tube_OD*tube_OD))/(math.pi*tube_OD) # m
shell_area = (D_shell*(Pitch-tube_OD)*baffle_spacing)/Pitch # sq.m
Re_shell = (m_e/shell_area)*D_shell_effective/e_mu
Nu_shell = 0.36*(Re_shell**0.55)*(e_Pr**0.33)
h_shell = Nu_shell*e_k/D_shell_effective # W/sq.m-C

U = 1/((1/h_tube)+(1/h_shell)+(0.002*0.1761))

tube_side_pressure_drop = (2*((8*4e-3*(tube_L/tube_ID))+(2.5))*w_rho*(m_w/(tube_flow_area*w_rho))**2)/2
shell_side_pressure_drop = (1*8*4e-2*(D_shell/D_shell_effective)*(tube_L/baffle_spacing)*e_rho*(m_e/(shell_area*e_rho))**2)/2

print(f'''
Corrected LMTD : {corrected_LMTD} C
Q : {Q} W
Ethanol flow rate : {m_e} kg/s
Water flow rate : {m_w} kg/s

Assumed overall HTC : {U_assumed} W/sq.m-C
Overall Heat Transfer area : {overall_heat_transfer_area} sq.m
Number of Tubes : {N_tubes_calculated} 

Re for tube : {Re_tube}
Nu for tube : {Nu_tube}
Tube side HTC : {h_tube} W/sq.m-C

Shell Diameter : {D_shell} m
Number of baffles : {N_baffles}
Effective Shell Diameter : {D_shell_effective} m
Shell Heat Transfer Area : {shell_area} sq.m

Re for shell : {Re_shell}
Nu for Shell : {Nu_shell}
Shell Side HTC : {h_shell}

Calculated Overall HTC : {U} W/sq.m-C

Tube Side Pressure Drop : {tube_side_pressure_drop/1000:.2f} kPa
Shell Side Pressure Drop : {shell_side_pressure_drop/1000:.2f} kPa \n(For 25% baffle spacing)
''')
