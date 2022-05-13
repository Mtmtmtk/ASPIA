import matplotlib.pylab as plt
import numpy as np
import scipy.signal as signal
from scipy.io.wavfile import write
import math
omega1 = 2*math.pi*22
omega2 = 2*math.pi*22000
fs = 44100
T  = 10

t = np.arange(0, T, 1/fs)
print(t)
t_inv = np.arange(T, 0, -1/fs)
print(t_inv)
k = 1 / np.exp(t*np.log(omega2/omega1)/T)

s     = np.sin(omega1*T/np.log(omega2/omega1) * (np.e**(t/T*np.log(omega2/omega1)) - 1))
s_inv = k * s[::-1]
write('swept_sine.wav', fs, s)
write('inv_swept_sine.wav', fs, s_inv)
#Print(s)
#Print(s_inv)
#
#Write('swept_sine.wav', fs, s)
#Write('inv_swept_sine.wav', fs, s_inv)

##see https://gsmcustomeffects.hatenablog.com/entry/2019/01/17/191215
#f1 = 22        # start frequency
#f2 = 22000       # end frequency
#fs = 96000      # sampling frequency
#T = 10          # time duration of the sweep
#fade = [48000, 480]   # samlpes to fade-in and fade-out the input signal
#
#
#L = T/np.log(f2/f1)                    # parametre of exp.swept-sine
#t = np.arange(0,np.round(fs*T-1)/fs,1/fs)  # time axis
#s = np.sin(2*np.pi*f1*L*np.exp(t/L))       # generated swept-sine signal
#
## fade-in the input signal
#if fade[0]>0:
#    s[0:fade[0]] = s[0:fade[0]] * ((-np.cos(np.arange(fade[0])/fade[0]*np.pi)+1) / 2)
#
## fade-out the input signal
#if fade[1]>0:
#    s[-fade[1]:] = s[-fade[1]:] *  ((np.cos(np.arange(fade[1])/fade[1]*np.pi)+1) / 2)
#    
#write('swept_sine.wav', fs, s)
