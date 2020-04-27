import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import DMTF as dmtf
import Spectro as spec
from scipy import signal
from scipy.fft import fftshift


def WhiteNoiseGen(samples):
    mean = 0;
    std = 0.1;
    num_samples = samples
    out = np.random.normal(mean,std,size=num_samples)
    return out

def AddNoise(sig,noise):
    out = sig + noise
    return out



def Get_XY(data):
    minput = np.array(data)
    print(np.size(minput))
    mx = []
    my = []
    size = int(np.size(minput)/2)

    for i in range(0, size-1):
        mx.append(minput[i][0])
        my.append(minput[i][1])
    return mx, my

def ComposeData(x,y):
    data = []
    for i in range(0,len(x)-1):
        data.append([x[i],y[i]])
    return data


def WAV_Plot(x,y):
    plt.plot(x,y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
def WidmoAmp(x,samplerate):
    xf = np.fft.fft(x)
    samplelim = samplerate/2
    out = []
    outdb = []
    f = []
    for i in range(0,len(x)-1):
        fk = i*(samplerate/len(x))
        if fk>samplerate/4:
            break
        f.append(fk)
        a = xf[i].real
        b = xf[i].imag
        out.append((a*a)+(b*b))
        outdb.append(10*(np.log(out[i])/np.log(10)))
        out[i] = out[i]*(2/len(x))
    plt.plot(f,out)
    plt.ylabel("Amplitude")
    plt.xlabel("Frequency")


# Odczyt pliku wav
data, samplerate = sf.read('ATrain.wav')
x,y = Get_XY(data);

# DFT
WidmoAmp(x,samplerate)
plt.show()

# Analiza
str = "maciej.kukulkaaa"
tmp = dmtf.T9Convert(str)
print(tmp)
ox, oy = dmtf.DMTFconv(tmp, 0.1, 44100)
plt.plot(ox, oy)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.show()

WidmoAmp(oy,44100)
plt.show()

wn = WhiteNoiseGen(740880)
an = AddNoise(oy,wn)

plt.plot(ox, an)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.show()

WidmoAmp(an,44100)
plt.show()

f,t,Sxx = signal.spectrogram(an,44100)
plt.pcolormesh(t,f,Sxx)
plt.xlabel('Time [Sec]')
plt.ylabel('Frequency [Hz]')
plt.savefig('Spect.png')
plt.show()

ramki = spec.Divide_Data(x,0.1,44100)
print(np.size(ramki))
#print(ramki)



# DFT

WidmoAmp(x,samplerate)
plt.show()
data2 = ComposeData(x,y)
# Zapis pliku wav



sf.write('new.wav', an, samplerate)
