import scipy.io as sio;
import numpy;
from numpy import sin, linspace, pi
from pylab import plot, show, title, xlabel, ylabel, subplot
from scipy import fft, arange
import time;


def getFFT(y, Fs):
    L = len(y);
    Y = numpy.fft.rfft(y);
    freq = numpy.fft.fftfreq(L);
    plot(freq, Y.real);
    show();

x = sio.loadmat("Sub1_singletarget.mat");
eegData = x["Data"]["EEG"];
print(x["Data"])
eegData = numpy.asmatrix(eegData[0][0]);
d0 = eegData[:,2];
print(len(d0));
print (numpy.asarray(d0));

(Hz, dataFFT) = eeg.computeFFT(d0, 512);
plot(Hz, dataFFT);
show();