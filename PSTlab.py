import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt
import DMTF as dmtf
import Filters as fltr
from scipy import signal
from scipy.fft import fftshift

def Divide_Data(data,Tr,samplerate):
    minput = np.array(data)
    size = int(np.size(minput))
    out = []
    for i in range(0, int(size/(Tr*samplerate))):
        tmp = []
        for j in range(0, int(Tr*samplerate)):
            tmp.append(data[i* int(Tr*samplerate) + j])
        out.append(tmp)

    return out

def GetNoise(fname):
    data, samplerate = sf.read(fname)
    out = data
    print(len(data))
    return out

def AddNoise(sig,noise,samplerate):
    out = sig
    for i in range(0,len(sig)):
        out[i] = sig[i] + noise[i%samplerate];
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



# Liczenie spektrogramu DTMF
my = np.array(oy)
f,t,Sxx = signal.spectrogram(my,44100)
plt.pcolormesh(t,f,Sxx)
plt.xlabel('Time [Sec]')
plt.ylabel('Frequency [Hz]')
plt.savefig('Spect.png')
plt.show()

# podział na ramki
ramki = Divide_Data(x,0.1,44100)
print(np.size(ramki))
#print(ramki)
# Dodawnia szumu
pink = GetNoise('pinkn.wav');
an = AddNoise(oy,pink,44100)


plt.plot(ox, an)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.title("DMTF + pink noise")
plt.show()
WidmoAmp(an,44100)
plt.show()


# IIR BP

flt = fltr.FilterIIRbp(oy,650,1537,samplerate)
plt.plot(ox, flt)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.title("Bandpass IIR filter")
plt.show()
WidmoAmp(flt,44100)
plt.title("Bandpass IIR filter")
plt.show()

# IIR BS

flt = fltr.FilterIIRbs(oy,650,1537,samplerate)
plt.plot(ox, flt)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.title("Bandstop IIR filter")
plt.show()
WidmoAmp(flt,44100)
plt.title("Bandstop IIR filter")
plt.show()
# FIR BP

flt = fltr.FilterFIRbp(oy,650,1537,samplerate)
plt.plot(ox, flt)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.title("Bandpass FIR filter")
plt.show()
WidmoAmp(flt,44100)
plt.title("Bandpass FIR filter")
plt.show()
# FIR BS

flt = fltr.FilterFIRbs(oy,650,1537,samplerate)
plt.plot(ox, flt)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.title("Bandstop FIR filter")
plt.show()
WidmoAmp(flt,44100)
plt.title("Bandstop FIR filter")
plt.show()







# DFT

WidmoAmp(x,samplerate)
plt.show()
data2 = ComposeData(x,y)
# Zapis pliku wav



sf.write('new.wav', an, samplerate)
