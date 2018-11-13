import threading;
import Utils.EEG.EEG.eeg as eeg;

# creating a decorator for threading a function.
def thread(func):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs);
        thread.start();
        return thread;
    return wrapper;

def computeFFT(data, fs):
    return eeg.computeFFT(data, fs);

def fftHighPassFilter(fft, freqs, cutOff):
    fft[(freqs < cutOff)] = 0.0;
    return  fft;

def fftLowPassFilter(fft, freqs, cutOff):
    fft[(freqs > cutOff)] = 0.0;
    return fft;

def fftBandStopFilter(fft, freqs, cutOff_lo, cutOff_hi):
    return fftLowPassFilter(fft.copy(), freqs, cutOff_lo) + fftHighPassFilter(fft.copy(), freqs, cutOff_hi);

def fftBandPassFilter(fft, freqs, cutOff_lo, cutOff_hi):
    fft = fftLowPassFilter(fft.copy(), freqs, cutOff_hi);
    return fftHightPassFilter(fft, freqs, cutOff_lo);


def Print(STRING):
    #STRING = "\n" + STRING + "\n";
    print(STRING);
    

def getComputerIP():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = (s.getsockname()[0]);
    s.close()
    return ip;

def msg2dict(msg):
    if msg is None:
        return None;
    (sender, receiver, dispatchTime, reactionToMsgAtTime, data, otherData) = msg.unpack();
    x = {
        "sender" : sender,
        "receiver" : receiver,
        "dispatchTime" : dispatchTime,
        "reactionToMsgAtTime" : reactionToMsgAtTime,
        "data" : data,
        "otherData" : otherData
    };
    return x;