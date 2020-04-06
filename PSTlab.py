import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

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
    

# Odczyt pliku wav
data, samplerate = sf.read('ATrain.wav')
x,y = Get_XY(data);

# DFT
data2 = ComposeData(x,y)
xf = np.fft.fft(x)
print(xf)
plt.plot(data2)
plt.show()

# Analiza

# DFT

# Zapis pliku wav

sf.write('new.wav', data2, samplerate)


