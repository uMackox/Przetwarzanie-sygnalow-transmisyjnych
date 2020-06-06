import soundfile as sf
import numpy as np
import matplotlib.pyplot as plt

def Delta_code(input,fs,delta):
    size = len(input)
    print(size)
    T = float(size) / fs;
    dt = 1.0/fs;
    t = np.arange(0,T,dt);
    N = len(t)
    x = input[0:N]
    print(len(x))
    mdelt = dt * delta;
    e=[]
    y=[]
    e.append(1)
    y.append(x[0])
    for i in range(1,N):
        e.append(x[i] - y[i-1])

        if e[i]<0:
            e[i] = -1
        else:
            e[i] = 1
        y.append(y[i-1] + e[i]*mdelt)
    return t,e,y

def Save_Delta(fname,delta,e,y0,samplerate):
    f = open(fname,'w')
    f.write(str(y0)+"\n")
    f.write(str(delta)+"\n")
    f.write(str(samplerate)+"\n")
    tmpstr = ''
    charperline = 100
    charcount =0;
    for i in range(0,len(e)):
        if e[i] == -1:
            f.write('0')
        else:
            f.write('1')
    f.close()
    return 0

def Read_delta(fname):
    f = open(fname,'r')
    y0 = float(f.readline())
    delta = float(f.readline())
    samplerate = float(f.readline())
    e = []
    lines = f.readlines()
    for line in lines:
        for i in range(0,len(line)-1):
            if(line[i] == '0'):
                e.append(-1)
            else:
                e.append(1)
    f.close()
    return y0,delta,samplerate,e

def Delta_From_File(y0,delta,samplerate,e):
    t = []
    y = []
    t.append(0)
    y.append(y0)
    for i in range(1,len(e)):
        t.append(float(i)/samplerate)
        y.append(y[i-1] + e[i]*delta)
    return t,y

#data, samplerate = sf.read('female_speech.wav')
#t,e,y = Delta_code(data,samplerate,500)
#Save_Delta("test.txt",500,e,y[0],samplerate)

#plt.subplot(2,1,1)
#plt.plot(t,data)


#y0,delta,samplerate,e2 = Read_delta("test.txt")
#t,mod = Delta_From_File(y0,delta,samplerate,e2)

#for i in range(0,len(e)-2):
#    if(e[i] == e2[i]):
#        continue
#    else:
#        print("nack")
#        print(i)
#        break

#plt.subplot(2,1,2)
#plt.plot(t,mod)
#plt.show()

#sf.write('deltatest.wav',mod,samplerate)
