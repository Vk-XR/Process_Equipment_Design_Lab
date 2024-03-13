import math
import numpy as np

#Given
F = 6.944 # kg/s
xF = 0.05
xP = 0.35

CpF = 3700 #J/kg°C
CpP = 3200 #J/kg°C
Cp1 = Cp2 = 4186 #J/kg°C

TF = 30 # °C
TS = 120.62 # °C at 2 atm
T3 = 53.5 # °C at 110mm Hg pressure

lambda_ts = 2706833.4 # J/kg

U1 = 2500 # W/m²K
U2 = 2000 # W/m²K
U3 = 1500 # W/m²K

# Calculations
P = F*xF/xP
V = F-P


del_T_total = TS-T3
del_T1 = del_T_total/(1+(U1/U2)+(U1/U3))
del_T2 = del_T1*(U1/U2)
del_T3 = del_T1*(U1/U3)

while True:
    T1 = TS-del_T1
    T2 = T1-del_T2

    lambda_s1 = float(input("Enter value of enthalpy of vaporisation at T1 in J/kg: "))
    lambda_s2 = float(input("Enter value of enthalpy of vaporisation at T2 in J/kg: "))
    lambda_s3 = float(input("Enter value of enthalpy of vaporisation at T3 in J/kg: "))

    a = np.array([[1,1,1,0],
                  [lambda_s1,0,0,-lambda_ts],
                  [(Cp1*(T1-T2))-lambda_s1,lambda_s2,0,0],
                  [(Cp2*(T2-T3)),(Cp2*(T2-T3)-lambda_s2),lambda_s3,0]])
    b = np.array([V,(F*CpF*(TF-T1)),(F*CpF*(T1-T2)),(F*CpF*(T2-T3))])
    x = np.linalg.solve(a,b)
    ms1 = x[0].item()
    ms2 = x[1].item()
    ms3 = x[2].item()
    S = x[3].item()

    A1 = (S*lambda_ts)/(U1*del_T1)
    A2 = (ms1*lambda_s1)/(U2*del_T2)
    A3 = (ms2*lambda_s2)/(U3*del_T3)

    print(f"""
    del_T1 = {del_T1}
    del_T2 = {del_T2}
    del_T3 = {del_T3}

    T1 = {T1}
    T2 = {T2}
    T3 = {T3}

    ms1 = {ms1}
    ms2 = {ms2}
    ms3 = {ms3}
    S = {S}

    A1 = {A1}
    A2 = {A2}
    A3 = {A3}
    """)

    if math.isclose(A1,A2,rel_tol=0.1) and math.isclose(A2,A3,rel_tol=0.1):
        print("Calculated areas are in +-10% range. Proceeding with calculations.  ")
        break
    else:
        print("Calculated areas are not nearly equal. Going for next iteration...")
        Amean = (A1*del_T1+A2*del_T2+A3*del_T3)/del_T_total
        del_T1 *= (A1/Amean)
        del_T2 *= (A2/Amean)
        del_T3 *= (A3/Amean)

        print(f"""
        A mean = {Amean}
        new del T1 = {del_T1}
        new del T2 = {del_T2}
        new del T3 = {del_T3}
        """)
        continue

tube_OD = 0.0254 # m
tube_L = 4.88 # m
Pitch = 1.25*0.0254 # m triangular pitch
Amean = (A1+A2+A3)/3 # m²
N = Amean/(math.pi*0.0254*4.88)
Aactual = N*Pitch*Pitch*math.sin(math.pi/3)/0.7
Adowncomer = 0.4*Aactual
Atotal = Aactual+Adowncomer

Dshell = math.sqrt(4*Atotal/math.pi)
Ddowncomer = math.sqrt(4*Adowncomer/math.pi)
H_evap = tube_L+(1.5*Dshell)

print(f"""
Feed Flow Rate = {F} kg/s
Vapor Flow Rate = {V} kg/s
Product Flow Rate = {P} kg/s
Steam Flow Rate = {S} kg/s 
Steam Economy = {(V/S)}

We calculated the properties of the evaporators assuming equal areas.
The final areas were found to be:
A1 = {A1} m²
A2 = {A2} m²
A3 = {A3} m²

Average of the areas above = {Amean} m²
Considering 1\" O.D. tubes, 4.88m long on a 1.25\" triangular pitch.
Number of tubes = {N}
Actual area = {Aactual} m²
Downcomer Area = {Adowncomer} m²
Total area = {Atotal} m²

Shell Diameter = {Dshell} m
Downcomer diameter = {Ddowncomer} m

Height of evaporator column = {H_evap} m
""")

