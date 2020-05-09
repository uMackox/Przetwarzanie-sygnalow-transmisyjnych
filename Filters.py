from scipy import signal
import matplotlib.pyplot as plt
import numpy as np


def FilterIIRbp(source,f1,f2,fs):
    sos = signal.iirfilter(17,[f1, f2],rs = 60, btype='bandpass',analog=False,fs = fs,ftype='cheby2',output='sos')
    w,h = signal.sosfreqz(sos,44100,fs=fs)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.semilogx(w, 20 * np.log10(np.maximum(abs(h),1e-5)))
    ax.axis((10, 1000, -100, 10))
    ax.grid(which='both',axis='both')
    plt.title("IIR bandpass characteristic");
    plt.show();
    out = signal.sosfilt(sos,source)
    return out

def FilterIIRbs(source,f1,f2,fs):
    sos = signal.iirfilter(17,[f1, f2],rs = 60, btype='bandstop',analog=False,fs = fs,ftype='cheby2',output='sos')
    w,h = signal.sosfreqz(sos,44100,fs=fs)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.semilogx(w, 20 * np.log10(np.maximum(abs(h),1e-5)))
    ax.axis((10, 1000, -100, 10))
    ax.grid(which='both',axis='both')
    plt.title("IIR bandstop characteristic");
    plt.show();
    out = signal.sosfilt(sos,source)
    return out

def FilterFIRbp(source,f1,f2,fs):
    nt = int(fs/2)
    fil = signal.firwin(nt, [f1, f2], fs=fs, pass_zero=False)
    w,h = signal.freqz(fil,worN=8000)
    plt.plot((w/np.pi)*nt,np.abs(h),linewidth=2)
    plt.xlabel("Frequency [Hz]");
    plt.ylabel("Gain")
    plt.title("FIR BP Frequency Response");
    plt.show()
    out = signal.lfilter(fil,[1.0],source)
    return out

def FilterFIRbs(source,f1,f2,mfs):
    nt = int(mfs/2 + 1)
    fil = signal.firwin(nt, [f1, f2], fs=mfs)
    w,h = signal.freqz(fil,worN=8000)
    plt.plot((w/np.pi)*nt,np.abs(h),linewidth=2)
    plt.xlabel("Frequency [Hz]");
    plt.ylabel("Gain")
    plt.title("FIR BS Frequency Response");
    plt.show()


    out = signal.lfilter(fil,[1.0],source)

    return out
