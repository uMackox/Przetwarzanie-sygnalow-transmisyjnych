import soundfile as sf
import numpy as np
import math
import matplotlib.pyplot as plt

data, samplerate = sf.read('female_speech.wav')


def Probability(input):
    dict = {}
    for i in range(-2**16,2**16):
        dict[i] = 0
    for i in range(0,len(input)):
        dict[input[i]] = dict[input[i]] + 1
    out = []
    for key in dict:
        out.append(dict[key]/len(input))

    #print(input)
    print(len(input))
    return out
def Entropy(input):
    dict = {}
    for i in range(-2**16,2**16):
        dict[i] = 0
    for i in range(0,len(input)):
        dict[input[i]] = dict[input[i]] + 1
    sum = 0
    for key in dict:
        tmp = dict[key]/len(input)
        if tmp != 0:
            sum = sum + (tmp*np.log2(tmp))
    sum = -sum
    return sum


def LPC(input, r):
    out = [input[0]]
    print("Starting LPC")
    for i in range(1,r):
        x = input[i]
        xdiff = input[i-1]
        out.append(x-xdiff)
    R = []
    for n in range(r,len(input)):
        x = input[n]
        xdiff = 0.0;
        R = []
        P = []
        w = []
        tmp = []
        for j in range(1,r+1):
            for i in range(1,r+1):
                tmp.append(input[n-i]*input[n-j])
            R.append(tmp)
            tmp = []
        if np.linalg.det(R) == 0:
            xdiff = input[n-1]
        else:
            for j in range(1,r+1):
                P.append(input[n]*input[n-j])
            w = np.matmul(np.linalg.inv(R),P)
            for j in range(1,r+1):
                xdiff = xdiff + (w[j-1]*input[n-j])
        e = x -xdiff
        out.append(np.round(e))
    print("LPC Done")
    return out
x = []
for i in range(-2**16,2**16):
    x.append(i)


dataleft = []
dataright = []
for i in range(0,len(data)):
    dataleft.append(math.floor(data[i,0]*(2**15)+0.5))
    dataright.append(math.floor(data[i,1]*(2**15)+0.5))
#
#ent = Entropy(data,0)
left = LPC(dataleft,2)
right = LPC(dataright,2)
print(Entropy(dataleft))
print(Entropy(dataright))
print(Entropy(left))
print(Entropy(right))
plt.subplot(1,2,1)
y=Probability(left)
plt.semilogy(x,y,'r')
y=Probability(dataleft)
plt.semilogy(x,y,'b')
plt.title("Lewy kanał")
plt.subplot(1,2,2)
y=Probability(right)
plt.semilogy(x,y,'r')
y=Probability(dataright)
plt.semilogy(x,y,'b')
plt.title("Prawy kanał")
plt.show()
