#Assignment 1!!!

#import package(s) (and correct american spelling):

import math as maths

#Define sea level conditions:

P_SL = 101325.0
rho_SL = 1.225
T_SL = 288.15

#Define const. values (incl. thermal gradient a):

R = 287.05287
g_0 = 9.80665

#Define atmospheric layers by min. Alt. and thermal gradient in 2 lists:

a = [-0.0065, 0, 0.0010, 0.0028, 0, -0.0028, -0.0020]
H_base = [0, 11000, 20000, 32000, 47000, 51000, 71000]

#Define functions to calculate temperature, pressure (gradient and isothermal regions) and density at altitude h[m]:

def Temp(h, H_0, T_0, grad):
    T = T_0 + grad*(h-H_0)
    return T

def Pressure_grad(h, H_0, T_0, P_0, grad):
    P = P_0 * (Temp(h, H_0, T_0, grad)/T_0)**(-g_0/(grad*R))
    return P

def Pressure_iso(h, H_0, T_0, P_0):
    P = P_0*maths.e**((-g_0/(R*T_0))*(h-H_0))
    return P
    

def density(h, H_0, T_0, P_0, grad):
    if grad != 0:
        rho = Pressure_grad(h, H_0, T_0, P_0, grad)/(R*Temp(h, H_0, T_0, grad))
    else:
        rho = Pressure_iso(h, H_0, T_0, P_0)/(R*Temp(h, H_0, T_0, grad))
    return rho

#Calculate base temperatures, pressures and densities for each altitude range

T_base = [T_SL]
P_base = [P_SL]
rho_base = [rho_SL]

for i in range(6):
    if a[i] == 0:
        P_base.append(Pressure_iso(H_base[i+1], H_base[i], T_base[i], P_base[i]))
        T_base.append(T_base[i])
        rho_base.append(density(H_base[i+1], H_base[i], T_base[i], P_base[i], a[i]))        
    else:
        T_base.append(Temp(H_base[i+1], H_base[i], T_base[i], a[i]))
        P_base.append(Pressure_grad(H_base[i+1], H_base[i], T_base[i], P_base[i], a[i]))
        rho_base.append(density(H_base[i+1], H_base[i], T_base[i], P_base[i], a[i]))
        

#collect input altitude from user:

is_running = True

while is_running == True:
    print("     ", "*****ISA Calculator*****")
    print()
    print("1. Calculate ISA for altitude in meters")
    print("2. Calculate ISA for altitude in feet")
    print("3. Calculate ISA for altitude in FL")

    menu = int(input("Enter your choice of units: "))

    if menu == 1:
        H = float(input("Enter altitude [m]: "))
    elif menu == 2:
        H = float(input("Enter altitude [ft]: ")) * 0.3048
    else:
        H = float(input("Enter altitude [FL]: ")) * 0.3048 * 100


    #check that altitude range and calculate temperatures/pressure/density. Then return these values to the user:

    T=T_SL
    P=P_SL
    rho=rho_SL

    for i in range (len(T_base)):
        if H_base[i] <= H:
            if a[i] == 0:
                T = T_base[i]
                P = Pressure_iso(H, H_base[i], T_base[i], P_base[i])
            else:
                T = Temp(H, H_base[i], T_base[i], a[i])
                P = Pressure_grad(H, H_base[i], T_base[i], P_base[i], a[i])
            rho = density(H, H_base[i], T_base[i], P_base[i], a[i])
            

    #Return desired values to user

    print("Temperature: ", T, "K ", "(", (T-273.150), "C)")
    print("Pressure: ", P, "Pa ", "(", (P/P_SL)*100, "% SL)")
    print("Density: ", rho, "kg/m^3 ", "(", (rho/rho_SL)*100, "% SL)")

    done = input("are you finished (yes/no): ")
    
    if done == "yes":
        is_running = False
