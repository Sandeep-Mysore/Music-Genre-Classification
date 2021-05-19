import scipy
import scipy.io.wavfile
import os
import sys
import glob
import matplotlib.pyplot as plt
import numpy as np
from utils1 import GENRE_DIR, GENRE_LIST, DIR_2


# Extracts frequencies from a wavile and stores in a file
def create_fft(wavfile):
    sample_rate, song_array = scipy.io.wavfile.read(wavfile)
    print(sample_rate)
    print(song_array)
    fft_features = abs(scipy.fft(song_array[:10000]))
    print(fft_features)

    # plt.plot(fft_features)
    # plt.show()
    base_fn, ext = os.path.splitext(wavfile)

    # base_fn_1, ext = os.path.
    data_fn = base_fn + ".fft"
    np.save(data_fn, fft_features)
    np.append(DIR_2, fft_features)


def main():
    for label, genre in enumerate(GENRE_LIST):
        for fn in glob.glob(os.path.join(DIR, genre)):
            for wavfile in os.listdir(fn):
                if wavfile.endswith("wav"):
                    print("In Genre -> ", genre)
                    create_fft(os.path.join(GENRE_DIR, genre, wavfile))
                # append_fft(os.path.join())


if __name__ == "__main__":
    main()