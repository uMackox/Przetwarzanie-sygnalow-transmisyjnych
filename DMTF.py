import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

freqdvert = {
    "1" : 1209,
    "4" : 1209,
    "7" : 1209,
    "*" : 1209,
    "2" : 1336,
    "5" : 1336,
    "8" : 1336,
    "0" : 1336,
    "3" : 1477,
    "6" : 1477,
    "9" : 1477,
    "#" : 1477,

}
freqdhoriz = {
    "1" : 697,
    "2" : 697,
    "3" : 697,
    "4" : 770,
    "5" : 770,
    "6" : 770,
    "7" : 852,
    "8" : 852,
    "9" : 852,
    "*" : 941,
    "0" : 941,
    "#" : 941
}
lettersdict = {
    ",": "10",
    ".": "110",
    "?": "1110",
    "!": "11110",
    "a" : "20",
    "b" : "220",
    "c": "2220",
    "d": "30",
    "e": "330",
    "f": "3330",
    "g": "40",
    "h": "440",
    "i": "4440",
    "j": "50",
    "k": "550",
    "l": "5550",
    "m": "60",
    "n": "660",
    "o": "6660",
    "p": "70",
    "q": "770",
    "r": "7770",
    "s": "77770",
    "t": "80",
    "u": "880",
    "v": "8880",
    "w": "90",
    "x": "990",
    "y": "9990",
    "z": "99990",
    " ": "00",
    "*": "*0",
    "#": "#0"
}


def T9Convert(str):
    out = []

    for i in range(0,len(str)):
        for j in range(0,len(lettersdict[str[i]])):
            out.append(lettersdict[str[i]][j])
    return out

def DMTFconv(data,amp,samplerate):
    minput = np.array(data)
    size = int(np.size(minput))
    Tsound = 0.5;
    Tbreak = 0.1;
    ox = []
    oy = []
    xind = 0;
    for i in range(0,size):
        for j in range(0,int(Tsound*samplerate)):
            ox.append(xind/samplerate)
            s1 = amp * np.sin(2 * np.pi * freqdvert[data[i]] * (xind / samplerate))
            s2 = amp * np.sin(2 * np.pi * freqdhoriz[data[i]] * (xind / samplerate))
            xind = xind + 1
            oy.append(s1+s2)
        for j in range(0,int(Tbreak*samplerate)):
            ox.append((xind/samplerate))
            xind = xind+1
            oy.append(0)

    return ox,oy

def Goertz(N,f,fs,input):
    k = int(0.5 + ((N*f)/fs))
    w = (2.0 * np.pi * k) / N;
    cosine = np.cos(w)
    sine = np.sin(w);

    coeff = 2 * cosine;
    q0 = 0;
    q1 = 0;
    q2 = 0;

    for i in range(0,N):
        q0 = coeff *q1 - q2 + input[i]
        q2 = q1
        q1 = q0

    real = (q1 - q2 * cosine)
    imag = (q2 * sine)
    mag = real*real + imag*imag
    return np.sqrt(mag)

def DMTFdecode(input, fs):
    signaltime = len(input)/fs;
    #print(signaltime)
    blocktime = 0.6

    blockcount = int( signaltime / blocktime);
    blocksize = blocktime * fs;
    out = []

    for i in range(blockcount):
        offset = int(i*blocksize)
        for kh in freqdhoriz:
            test = Goertz(int(blocksize),freqdhoriz[kh],fs,input[offset:int(offset+blocksize)])
            if(test > 50.0):
                test = Goertz(int(blocksize),freqdvert[kh],fs,input[offset:int(offset+blocksize)])
                if(test > 50):
                    out.append(kh)
    if (len(out) == 0):
        print("Unable to decode dmtf")
    return out

def GetCharFromDict(str):
    for key in lettersdict:
        if(lettersdict[key] == str):
            return key
    return '';
def T9Decode(input):
    size = len(input)
    cstr = ''
    out = ''
    for i in range(0,size):
        #print("CSTR : "+cstr);
        cstr= cstr + input[i]
        if(input[i] == '0'):
            if(len(cstr) == 1):
                cstr = "00"
            out = out + GetCharFromDict(cstr)
            cstr = ''
    out = out + GetCharFromDict(cstr)

    return out


#str = "maciej kukulka jest najlepszy"
#tmp = T9Convert(str)
#print(tmp)
#ox,oy = DMTFconv(tmp,0.1,44100)
#test = DMTFdecode(oy,44100)
#print(test)

#out = T9Decode(test)
#print(out)
