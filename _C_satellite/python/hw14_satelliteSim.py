import matplotlib.pyplot as plt
import numpy as np
import satelliteParam as P
from signalGenerator import signalGenerator
from satelliteAnimation import satelliteAnimation
from dataPlotter import dataPlotter
from satelliteDynamics import satelliteDynamics
from dataPlotterObserver import dataPlotterObserver
from ctrlDisturbanceObserver import ctrlDisturbanceObserver

# instantiate satellite, controller, and reference classes
satellite = satelliteDynamics(alpha=0.2)
controller = ctrlDisturbanceObserver()
reference = signalGenerator(amplitude=15.0*np.pi/180.0,
                            frequency=0.03)
disturbance = signalGenerator(amplitude=1.0)
noise_phi = signalGenerator(amplitude=0.001)
noise_th = signalGenerator(amplitude=0.001)

# instantiate the simulation plots and animation
dataPlotObserver = dataPlotterObserver()
dataPlot = dataPlotter()
animation = satelliteAnimation()

t = P.t_start  # time starts at t_start
y = satellite.h()  # output of system at start of simulation

while t < P.t_end:  # main simulation loop
    # Propagate dynamics in between plot samples
    t_next_plot = t + P.t_plot

    # updates control and dynamics at faster simulation rate
    while t < t_next_plot:  
        r = reference.square(t)  # reference input
        d = disturbance.step(t)  # input disturbance

        # simulate sensor noise
        n = np.array([[noise_phi.random(t)],
                      [noise_th.random(t)]])  

        # update controller
        u, xhat, dhat = controller.update(r, y + n)  
        y = satellite.update(u + d)  # propagate system
        t += P.Ts  # advance time by Ts

    # update animation and data plots
    animation.update(satellite.state)
    dataPlot.update(t, satellite.state, u, r)
    dataPlotObserver.update(t, satellite.state, xhat, d, dhat)
    plt.pause(0.0001)  

# Keeps the program from closing until user presses a button.
print('Press key to close')
plt.waitforbuttonpress()
plt.close()
