import numpy as np

def Unite(input):
    r = len(input)
    mout = []
    for i in range(0,r):
        for j in range(0,len(input[i])):
            mout.append(input[i][j])
    return mout



def Spect(data,samplerate):
    frames = Divide_Data(data,0.6,samplerate)
    #frames = np.array(frames)
    r = len(frames)
    mt = []
    mf = []
    mout = []
    tindex = 0
    for i in range(0,r):
        tmp = np.array(frames[i])
        xf = np.fft.fft(tmp)
        samplelim = samplerate/2
        out = []
        outdb = []
        f = []
        for j in range(0,len(frames[i])-1):

            fk = j*(samplerate/len(frames[i]))
            if fk>samplerate/4:
                break
            f.append(fk)
            mf.append(fk)
            mt.append(tindex/samplerate)
            tindex = tindex+1;
            a = xf[j].real
            b = xf[j].imag
            out.append((a*a)+(b*b))
            out[j] = out[j]*(2/len(frames[i]))

        if len(out) < samplerate:
            for j in range(0,samplerate-len(out)):
                fk = j*(samplerate/len(frames[i]))
                f.append(fk)
                mf.append(fk)
                mt.append(tindex/samplerate)
                tindex = tindex+1;
                out.append(0)

        maxv = max(out)
        minv = min(out)
        for j in range(0,len(out)):
            out[j] = out[j] - minv
            out[j] = out[j] / (maxv - minv);
            out[j] = out[j] * 255;
        mout.append(out);

    mout = Unite(mout);
    return mt,mf,mout
