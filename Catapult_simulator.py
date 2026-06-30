import numpy as np
import matplotlib.pyplot as plt

#constants

g = 9.81
m_cow = 550
R_cow = (((m_cow/1000)*3)/(4*np.pi))**(1/3)  # find radius of cow given a density of 1000kg*m^-3
h_0 = 60.0
time_step = 0.0001

def calc_Force_t(phi, R, L_0, k_e):
    L = np.sqrt((2*(R**2)) - (2*(R**2)) * np.cos((np.pi / 2) - phi))
    if L <= L_0:
        return 0.0

    delta_L = L - L_0
    F_e = k_e * delta_L
    dR = R * np.sin(phi)
    alpha = np.arcsin((R - dR) / L)
    F_e_t = F_e * np.sin(alpha + phi)
    F_g_t = -m_cow * g * np.cos(phi)

    return F_e_t + F_g_t

def calc_force_flight(v):
    C_d = 0.7
    rho = 1.225

    v_mag = np.sqrt((v[0]**2) + (v[1]**2))
    v_direction = [(i / v_mag) for i in v]

    F_D_mag = C_d * 0.5 * rho * (v_mag ** 2) * np.pi * (R_cow ** 2)
    F_D = [-i*F_D_mag for i in v_direction]
    F_g = [0, -m_cow * g]
    F_net = [(F_D[i] + F_g[i]) for i in range(2)]

    return F_net
    
def get_launch_vector(omega, phistop, R):
    v_mag = omega * R
    launch_angle = (np.pi/2) - phistop
    grad = np.tan(launch_angle)
    v_direction = [1 / np.sqrt(1 + grad ** 2), grad / np.sqrt(1 + grad ** 2)]
    v = [(i * v_mag) for i in v_direction]
    return v
    

def lob_cow_at_english(R, phistart, phistop, L_0, k_e):
    omega = 0
    phi = phistart

    x = [-R * np.cos(phistart)]
    y = [R * np.sin(phistart)]
    flight_path_angles = [np.pi/2]
    speeds = [0]
    time = [0]

    while phi <= phistop:
        F_t = calc_Force_t(phi, R, L_0, k_e)
        a = F_t / m_cow
        ang_a = a / R
        omega_1 = omega + ang_a * time_step
        time.append(time[-1] + time_step)
        phi += omega*time_step
        omega = omega_1
        
        x.append(-R*np.cos(phi))
        y.append(R*np.sin(phi))
        speeds.append(omega * R)

        flight_path_angle = np.pi/2 - phi
        
        flight_path_angles.append(flight_path_angle)

    v = get_launch_vector(omega, phistop, R)

    while y[-1] >= -h_0:
        F_vector = calc_force_flight(v)
        a_vector = [i/m_cow for i in F_vector]
        v_0 = v.copy()
        for i in range(2):
            v[i] += a_vector[i] * time_step

        time.append(time[-1] + time_step)
        x.append(x[-1] + v_0[0]*time_step)
        y.append(y[-1] + v_0[1]*time_step)
        speeds.append(np.sqrt((v[0]**2) + (v[1]**2)))
        flight_path_angles.append(np.arctan2(v[1], v[0]))
        

    return [x, y, flight_path_angles, speeds, time]

#values of phistop that work: 0.6754424205218055, 1.4451326206513047, 1.4608405839192538

results = lob_cow_at_english(10.0, 0, 1.4608405839192538, 0.5, 15000)

x = np.array(results[0])
y = np.array(results[1])
flight_path_angles = np.array(results[2])
speeds = np.array(results[3])
time = np.array(results[4])

plt.subplot(311)
plt.plot(x, y)
plt.xlabel("distance [m]")
plt.ylabel("height [m]")

plt.subplot(312)
plt.plot(time, flight_path_angles)
plt.xlabel("time [s]")
plt.ylabel("Flight Path Angle [radians]")

plt.subplot(313)
plt.plot(time, speeds)
plt.xlabel("time [s]")
plt.ylabel("speed [ms^-1]")

plt.show()










    
    

