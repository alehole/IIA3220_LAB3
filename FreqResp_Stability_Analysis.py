
import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt
import control
# Process Parameters
Kh = 3.5
theta_t = 22
theta_d = 2
# Transfer Function Process
num = np. array ([Kh])
den = np. array ([theta_t , 1])
Hp1 = control.tf(num , den)
print('Hp(s) =', Hp1)

H = signal.TransferFunction(num , den)


# Step Response
t, y = signal.step(H)
# Plotting
plt.plot(t, y)
plt.title("Step Response")
plt.xlabel("t")
plt.ylabel("y")
plt.grid()
plt.show()



# Frequencies
w_start = 0.01
w_stop = 10
step = 0.01
N = int((w_stop-w_start)/step)
w = np.linspace(w_start,w_stop, N)

# Bodeplot
omega, mag ,phase = signal.bode(H)

plt.figure()
plt.subplot(2,1,1)
plt.semilogx(omega, mag)
plt.title("Bode Plot")
plt.grid(b=None, which='major', axis='both')
plt.grid(b=None, which='minor', axis='both')
plt.ylabel("Magnitude (dB)")

plt.subplot(2,1,2)
plt.semilogx(omega, phase)
plt.grid(b=None, which='major', axis='both')
plt.grid(b=None, which='minor', axis='both')
plt.ylabel("Phase (deg)")
plt.xlabel("Frequency (rad/sec)")
plt.show()


# Ploting Bode plot with margins
control.bode(Hp1, dB=True, deg=True, margins=True)
# Stability margins and crossover frequencies
gm, pm, w180, wc = control.margin(Hp1)
#convert gm to dB
gmdB = 20*np.log10(gm)

print("wc =",f'{wc:.2f}', "rad/s" )
print("w180 =",f'{w180:.2f}', "rad/s" )

print("GM =",f'{gm:.2f}')
print("GM =",f'{gmdB:.2f}', "dB" )
print("PM =",f'{pm:.2f}', "deg" )




z = control.zero(Hp1)
print ('z =', z)
p = control.pole(Hp1)
print ('p =', p)
control.pzmap(Hp1)