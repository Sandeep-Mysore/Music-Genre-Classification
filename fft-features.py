import scipy
import scipy.io.wavfile
import os

import sys
import glob
import matplotlib.pyplot as plt
import numpy as np
from utils2 import GENRE_DIR, GENRE_LIST


# Extracts frequencies from a wavile and stores in a file
def create_fft(wavfile):
    sample_rate, song_array = scipy.io.wavfile.read(wavfile)
    print(sample_rate)
    print(song_array)
    # y = np.fft.fft(song_array)
    # y = np.fft.fft(y)[0:int(N/2)]/N
    # y[] =
    # Pxx = np.abs(y)
    # fs = 22050
    # T = (1/fs)
    # t = 0.1
    # N = fs*t
    # f = fs*(np.arange((N/2))/N)
    # fig,ax = plt.subplots()
    # plt.plot(f, Pxx)
    # plt.show()
    fft_features = abs(scipy.fft(song_array[:20000]))
    print(fft_features)
    plt.plot(fft_features)
    plt.show()
    base_fn, ext = os.path.splitext(wavfile)
    data_fn = base_fn + ".fft"
    np.save(data_fn, fft_features)


def main():
    for label, genre in enumerate(GENRE_LIST):
        for fn in glob.glob(os.path.join(GENRE_DIR, genre)):
            for wavfile in os.listdir(fn):
                if wavfile.endswith("wav"):
                    create_fft(os.path.join(GENRE_DIR, genre, wavfile))


if __name__ == "__main__":
    main()