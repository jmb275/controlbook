# Single link arm Parameter File
import hw16 as P16
from control import bode, margin, mag2db
import matplotlib.pyplot as plt

# flag to define if using dB or absolute scale for M(omega)
dB_flag = P16.dB_flag

# assigning plant and controller from past HW (to make sure
# we don't introduce additional errors)
Plant = P16.Plant
C_pid = P16.C_pid

if __name__ == '__main__':
    # Calculate the phase and gain margins
    if dB_flag:
        gm, pm, Wcg, Wcp = margin(Plant*C_pid)
        gm = mag2db(gm)
        print("Inner Loop:", "gm: ",gm,
              " pm: ", pm," Wcg: ", Wcg, " Wcp: ", Wcp)

    else:
        gm, pm, Wcg, Wcp = margin(Plant*C_pid)
        print("Inner Loop:", "gm: ", gm,
              " pm: ", pm, " Wcg: ", Wcg, " Wcp: ", Wcp)

    # display bode plots of transfer functions
    fig1 = plt.figure()

    # this makes two bode plots for open and closed loop
    bode([Plant * C_pid, 
          Plant*C_pid/(1+Plant*C_pid)], 
          dB=dB_flag)
    
    # now we can add lines to show where we calculated the GM and PM
    fig1.axes[0].plot([Wcg, Wcg],
                      plt.ylim(), 'k--', label='GM')
    fig1.axes[1].plot([Wcp, Wcp], plt.ylim(), 'b--', label='PM')

    # finally, we can format and add legends for clarity
    mag_legend = ['C(s)P(s) - Open-loop', 
                  r'$\frac{P(s)C(s)}{1+P(s)C(s)}$ - Closed-loop', 
                  'GM']
    phase_legend = ['Open-loop', 'Closed-loop', 'PM']
    fig1.axes[0].legend(mag_legend)
    fig1.axes[1].legend(phase_legend)

    # setting axis title
    fig1.axes[0].set_title('Single Link Robot Arm - '+
                           'GM:'+str(round(gm, 2))+
                           ', PM:'+str(round(pm, 2)))
    fig1.suptitle('Bode Plots for Single Link Robot Arm')
    plt.show()
