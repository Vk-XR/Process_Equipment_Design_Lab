import math

#Temperatures
T_e_in = 120 # °C
T_e_out = 120 # °C
T_w_in = 30 # °C
T_w_out = 50 # °C
LMTD = (((T_e_in-T_w_out)-(T_e_out-T_w_in))/math.log((T_e_in-T_w_out)/(T_e_out-T_w_in))) # °C

# Fluid properties
# Steam at 120 °C
s_cp = 2121 # J/kg°C
s_rho = 1.129  # kg/m³
s_mu = 0.000013 # Pa-s
s_k = 0.0275  # W/m°C
s_lambda = 2201590 # J/kg
s_Pr = (s_cp*s_mu)/s_k

# Water at 40 °C
w_cp = 4178 # J/kg°C
w_rho = 992.224  # kg/m³
w_mu = 0.000653 # Pa-s
w_k = 0.630635 # W/m°C
w_Pr = (w_cp*w_mu)/w_k

# Tube dimensions
tube_OD = 0.75*0.0254 # m
tube_ID = tube_OD-(0.00211*2) # m
tube_L = 6*12*0.0254 # m

m_s = 2.77 # kg/s
Q = (m_s*s_lambda) # W
m_w = Q/(w_cp*(T_w_out-T_w_in)) # kg/s

U_assumed = 1500 # W/m²-°C
overall_heat_transfer_area = Q/(U_assumed*LMTD) # m²
N_tubes_calculated = overall_heat_transfer_area/(math.pi*tube_OD*tube_L)
N_tubes_practical = 534
D_shell = 27*0.0254 # m

# Water on Tube side
tube_flow_area = (N_tubes_practical/2)*math.pi*(tube_ID**2)/4 # m²
Re_tube = (m_w/tube_flow_area)* tube_ID/ w_mu
Nu_tube = 0.023*(Re_tube**0.8)*(w_Pr**0.4)
h_tube = Nu_tube*w_k/tube_ID # W/sq.m-C

Pitch = 0.0254 # m
baffle_spacing = 0.152 if 0.2*D_shell<0.152 else 0.2*D_shell # m 
effective_length = 0.8*tube_L # m
baffle_length = 0.75*D_shell # m
N_baffles = math.ceil((effective_length/baffle_spacing)-1)

h_shell_assumed = 8517.45 # W/m²-°C
h_shell_calc = 0 # W/m²-°C
counter = 0
while(not(math.isclose(h_shell_assumed,h_shell_calc,abs_tol=50))):
    print("Assumed value of H_shell is not near the calculated value.\n")
    if counter>0:
        h_shell_assumed = h_shell_calc
    h_io = h_tube*tube_ID/tube_OD
    T_wall = 40 + (h_shell_assumed*(120-40)/(h_shell_assumed+h_io))
    T_film = (T_wall+120)/2
    K_tf = float(input(f"Enter K at film temperature ({T_film}) in W/m°C: "))
    rho_tf = float(input(f"Enter density at film temperature ({T_film}) in kg/m³: "))
    mu_tf = float(input(f"Enter viscosity at film temperature ({T_film}) in Pa-s: "))
    Db = 0.01905*((N_tubes_practical/0.249)**(1/2.207))
    Nr = math.ceil(Db/Pitch)
    gamma = m_s/(tube_L*N_tubes_practical)
    h_shell_calc = (0.95*K_tf*(Nr**(-1/3)))*((rho_tf*(rho_tf-s_rho)*9.81/(gamma*mu_tf))**(1/3))
    print(f"H_shell_calculated for this iteration: {h_shell_calc}\n")
    counter += 1
print("H_shell is close enough now. Proceeding with shell side calculations.\n")
D_shell_effective = ((4*Pitch*Pitch*0.866) - (math.pi*tube_OD*tube_OD))/(math.pi*tube_OD) # m
shell_area = (D_shell*(Pitch-tube_OD)*baffle_spacing)/Pitch # sq.m
Re_shell = (m_s/shell_area)*D_shell_effective/s_mu

U = 1/((1/h_tube)+(1/h_shell_calc)+(0.0005*0.1761))

tube_side_pressure_drop = ((8*3.5e-3*tube_L/tube_ID)+2.5)*w_rho*((m_w/(tube_flow_area*w_rho))**2)*0.5
shell_side_pressure_drop = 0.25*1*8*3.3e-2*(D_shell/D_shell_effective)*(tube_L/baffle_spacing)*s_rho*((m_s/(shell_area*s_rho))**2)

print(f'''
Corrected LMTD : {LMTD} °C
Q : {Q} W
Steam flow rate : {m_s} kg/s
Water flow rate : {m_w} kg/s

Assumed overall HTC : {U_assumed} W/m²-°C
Overall Heat Transfer area : {overall_heat_transfer_area} m²
Number of Tubes : {N_tubes_calculated} 
Practical Number of Tubes: {N_tubes_practical}

Re for tube : {Re_tube}
Nu for tube : {Nu_tube}
Tube side HTC : {h_tube} W/m²-°C

Shell Diameter : {D_shell} m
Baffle Spacing : {baffle_spacing} m
Number of baffles : {N_baffles}
Effective Shell Diameter : {D_shell_effective} m
Shell Heat Transfer Area : {shell_area} m²

Re for shell : {Re_shell}
Shell Side HTC : {h_shell_calc} W/m²-°C

Calculated Overall HTC : {U} W/m²-°C

Friction factor for tube side = 3.5e-3
Tube side pressure drop : {tube_side_pressure_drop/1000} kPa

Friction factor for shell side = 3.3e-2
Shell side pressure drop : {shell_side_pressure_drop/1000} kPa
''')
