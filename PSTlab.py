
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

def WAV_Plot(x,y):
    plt.plot(x,y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()
print("aaa")

data, samplerate = sf.read('ATrain.wav')

print(samplerate)

x = data[0]
y=data[1]
plt.plot(data)
plt.show()

sf.write('new.wav', data, samplerate)


