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
    #print(len(data))
    return out

def AddNoise(sig,noise,samplerate,alpha):
    out = sig
    for i in range(0,len(sig)):
        out[i] = sig[i]*alpha + (noise[i%samplerate]*(1-alpha));
    return out



def Get_XY(data):
    minput = np.array(data)
    #print(np.size(minput))
    mx = []
    my = []
    size = int(np.size(minput)/2)
    #print(size)
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



# Generowanie sygnału DMTF
str = "maciej"
print(str)
tmp = dmtf.T9Convert(str)
print(tmp)
ox, oy = dmtf.DMTFconv(tmp, 0.1, 44100)
data = ComposeData(oy,oy)
sf.write('dmtf.wav',data, 44100)



# Odczyt pliku wav
data, samplerate = sf.read('dmtf.wav')
x,y = Get_XY(data);

# DFT
WidmoAmp(x,samplerate)
plt.show()



# Analiza


# Liczenie spektrogramu DTMF
my = np.array(oy)
f,t,Sxx = signal.spectrogram(my,44100)
plt.pcolormesh(t,f,Sxx)
plt.xlabel('Time [Sec]')
plt.ylabel('Frequency [Hz]')
plt.title('Spektrogram sygnału')
plt.savefig('Spect.png')
plt.show()


# podział na ramki
#ramki = Divide_Data(x,0.1,44100)
#print(np.size(ramki))
#print(ramki)

# Dodawnia szumu
pink = GetNoise('./noises/pinkn.wav');
an = AddNoise(oy,pink,44100,0.85)
plt.figure()
plt.subplot(1,2,1)
plt.plot(ox, an)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.title("Sygnal + pink noise")
plt.subplot(1,2,2)
WidmoAmp(an,44100)
plt.show()


# IIR BP

flt = fltr.FilterIIRbp(oy,650,1537,samplerate)

plt.figure()
plt.subplot(1,2,1)
plt.plot(ox, flt)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.title("Bandpass IIR filter")
plt.subplot(1,2,2)
WidmoAmp(flt,44100)
plt.title("Bandpass IIR filter")
plt.show()

decode = dmtf.DMTFdecode(flt,44100)
print(decode)
strrec = dmtf.T9Decode(decode)
print(strrec)

# IIR BS

flt = fltr.FilterIIRbs(oy,650,1537,samplerate)
plt.figure()
plt.subplot(1,2,1)
plt.plot(ox, flt)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.title("Bandstop IIR filter")
plt.subplot(1,2,2)
WidmoAmp(flt,44100)
plt.title("Bandstop IIR filter")
plt.show()

# FIR BS

flt = fltr.FilterFIRbs(oy,650,1537,samplerate)
plt.figure()
plt.subplot(1,2,1)
plt.plot(ox, flt)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.title("Bandstop FIR filter")
plt.subplot(1,2,2)
WidmoAmp(flt,44100)
plt.title("Bandstop FIR filter")
plt.show()

# FIR BP

flt = fltr.FilterFIRbp(oy,650,1537,samplerate)
plt.figure()
plt.subplot(1,2,1)
plt.plot(ox, flt)
plt.ylabel("Amp")
plt.xlabel("Time")
plt.title("Bandpass FIR filter")
plt.subplot(1,2,2)
WidmoAmp(flt,44100)
plt.title("Bandpass FIR filter")
plt.show()





# DFT

WidmoAmp(x,samplerate)
plt.show()
data2 = ComposeData(x,y)
# Zapis pliku wav



sf.write('new.wav', flt, samplerate)
