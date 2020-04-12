import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf

def T9Convert(str):
    out = []
    lettersdict = {
        ",": "1",
        ".": "11",
        "?": "111",
        "!": "1111",
        "a" : "2",
        "b" : "22",
        "c": "222",
        "d": "3",
        "e": "33",
        "f": "333",
        "g": "4",
        "h": "44",
        "i": "444",
        "j": "5",
        "k": "55",
        "l": "555",
        "m": "6",
        "n": "66",
        "o": "666",
        "p": "7",
        "q": "77",
        "r": "777",
        "s": "7777",
        "t": "8",
        "u": "88",
        "v": "888",
        "w": "9",
        "x": "99",
        "y": "999",
        "z": "9999",
        " ": "0",
        "*": "*",
        "#": "#"
    }
    for i in range(0,len(str)):
        for j in range(0,len(lettersdict[str[i]])):
            out.append(lettersdict[str[i]][0])
    return out

def DMTFconv(data,amp,samplerate):
    minput = np.array(data)
    size = int(np.size(minput))
    Tsound = 0.5;
    Tbreak = 0.1;
    ox = []
    oy = []
    xind = 0;
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
    for i in range(0,size-1):
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
