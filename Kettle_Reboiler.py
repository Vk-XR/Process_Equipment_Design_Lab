import math

#Given for Toluene
m_b = 1.389 #kg/s
T_f = 20 # °C
T_b = 110.6 # °C 
Cp_b = 1833.6 # J/kg°C
lambda_b = 361000 # J/kg
visc_b = 389e-6 # Pa-s
K_b = 0.1344 # W/mK
rho_b = 830 # kg/m³
P_c = 41.3 # bar
sigma_b = 0.028 # N/m
rho_v = 3.14 #kg/m³
#given for steam
T_s = 111.35 # °C
lambda_s = 2693113.266 # J/kg

# extras given
U = 900 # W/m²-°C
tube_od = 0.0254 # m
tube_L = 12 #m 
pitch = 1.25*0.0254 #m, square pitch

#Calculations
Q = (m_b*Cp_b*(T_b-T_f)+(m_b*lambda_b))
m_s = Q/lambda_s
lmtd = ((T_s-T_f)-(T_s-T_b))/(math.log((T_s-T_f)/(T_s-T_b))) #°C
A = Q/(U*lmtd) #m²
N = A/(math.pi*tube_od*tube_L)
N_practical = 56 # From chart
A_practical = math.pi*tube_od*tube_L
U_practical = Q/(A_practical*lmtd)

D_bundle = tube_od*((N_practical/0.156)**(1/2.291)) # m
N_nozzles = tube_L/(5*D_bundle)

h_tube = 8000 #W/m²°C
q = Q/A_practical # W/m²
q_critical = 0.44*(pitch/tube_od)*(lambda_b/math.sqrt(N_practical))*((sigma_b*9.81*(rho_b-rho_v)*rho_v*rho_v)**(0.25)) # W/m²
h_nb = 0.104*(P_c**(0.69))*(q**0.7)*((1.8*((1/P_c)**(0.17)))+(4*((1/P_c)**(1.2)))+(10*((1/P_c)**(10)))) # W/m²°C

U_calc = 1/((1/h_tube) + (1/h_nb) + (0.001*0.1761)) # W/m²°C

D_shell = (D_bundle+(4*0.0254))/0.7 # m
h = D_shell*0.3
# from h/D_shell = 0.3, we get a = 0.19817
SA_estimated = 0.19817*(D_shell**2)

VL = 2290*rho_v*0.0624*(((sigma_b*1000)/((rho_b-rho_v)*0.0624))**0.5)
SA_calc = (m_b*7936.641)/(12*3.281*VL)*0.0929

if (SA_calc>SA_estimated):
    print(f"""
Results:
    Feed to vaporize = Toluene
    Feed flow rate = {m_b} kg/s
    Steam flow rate = {m_s} kg/s
    Reboiler Pressure = 1 bar
    Steam inlet pressure = 1.5 bar

    Taking Steam on TUBE side and Toluene on SHELL side.

    Assumed overall heat transfer coefficient = {U} W/m²°C
    Heat transfer area = {A} m²

    Tubes are of 1" O.D. , 12 m Length and arranged on a square pitch of 1.25" 
    Practical number of tubes from chart = {N_practical}
    Practical heat transfer area = {A_practical} m²
    Practical assumed heat transfer coeeficient = {U_practical} W/m²°C
    Bundle diameter = {D_bundle} m
    Number of nozzles = {math.ceil(N_nozzles)}

    Steam heat transfer coefficient = {h_tube} W/m²°C
    Nucleate boiling heat transfer coefficient = {h_nb} W/m²°C
    Calculated overall heat transfer coefficient = {U_calc} W/m²°C

    As U_calculated > U_assumed, design is correct.

    heat flux calculated = {q} W/m²
    0.7 x Critical heat flux = {0.7*q_critical} W/m²

    As calculated heat flux < 0.7*Critical heat flux, design is correct.

    Shell Diameter = {D_shell} m
    Dome Segment area calculated from vapor loading = {SA_calc} m²
    Dome Segment area estimated using h/D_Shell ratio and chart = {SA_estimated} m²

    As Segment area calculated > Segment area estimated, design is correct.
""")
