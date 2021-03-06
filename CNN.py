import warnings
warnings.filterwarnings("ignore", category = FutureWarning)

import os
import keras
import h5py
import librosa
import itertools
import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

from keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

from keras.models import Sequential
from keras.layers import Dense, Input
from keras.layers import Activation
from keras.layers import Conv2D
from keras.layers import MaxPooling2D
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers import BatchNormalization
from keras.applications.vgg16 import VGG16


# # Read the data
# 
# > Helper functions to assist the process to read songs, split then and return an array of spectrograms/melspectrograms


"""
@description: Method to split a song into multiple songs using overlapping windows
"""
def splitsongs(X, y, window = 0.1, overlap = 0.5):
    # Empty lists to hold our results
    temp_X = []
    temp_y = []

    # Get the input song array size
    xshape = X.shape[0]
    chunk = int(xshape*window)
    offset = int(chunk*(1.-overlap))
    
    # Split the song and create new ones on windows
    spsong = [X[i:i+chunk] for i in range(0, xshape - chunk + offset, offset)]
    for s in spsong:
        temp_X.append(s)
        temp_y.append(y)

    return np.array(temp_X), np.array(temp_y)


"""
@description: Method to convert a list of songs to a np array of melspectrograms
"""
def to_melspectrogram(songs, n_fft = 1024, hop_length = 512):
    # Transformation function
    melspec = lambda x: librosa.feature.melspectrogram(x, n_fft = n_fft,
        hop_length = hop_length)[:,:,np.newaxis]

    # map transformation of input songs to melspectrogram using log-scale
    tsongs = map(melspec, songs)
    return np.array(list(tsongs))


def read_data(src_dir, genres, song_samples, spec_format, debug = True):    
    # Empty array of dicts with the processed features from all files
    arr_specs = []
    arr_genres = []

    # Read files from the folders
    for x,_ in genres.items():
        folder = src_dir + x
        
        for root, subdirs, files in os.walk(folder):
            for file in files:
                # Read the audio file
                file_name = folder + "/" + file
                
                if not file.endswith("wav"):
                    continue
                
                # Debug process
                if debug:
                    print("Reading file: {}".format(file_name))
                
                signal, sr = librosa.load(file_name)
                signal = signal[:song_samples]
                
                # Convert to dataset of spectograms/melspectograms
                signals, y = splitsongs(signal, genres[x])
                
                # Convert to "spec" representation
                specs = spec_format(signals)
                
                # Save files
                arr_genres.extend(y)
                arr_specs.extend(specs)
                
                
    return np.array(arr_specs), np.array(arr_genres)


# Parameters
gtzan_dir = r"X:\work\Freelancing\Upwork\Music\datasets\genres\\"
song_samples = 660000
# genres = {'metal': 0, 'disco': 1, 'classical': 2, 'hiphop': 3, 'jazz': 4, 
#           'country': 5, 'pop': 6, 'blues': 7, 'reggae': 8, 'rock': 9}
genres = {'disco': 0, 'classical': 1, 'hiphop': 2, 'blues': 3}

# Read the data
X, y = read_data(gtzan_dir, genres, song_samples, to_melspectrogram)


np.save('x_gtzan_npy.npy', X)
np.save('y_gtzan_npy.npy', y)


# One hot encoding of the labels
y = to_categorical(y)


# # Dataset Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42, stratify = y)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)


# Histogram for train and test 
values, count = np.unique(np.argmax(y_train, axis=1), return_counts=True)
plt.bar(values, count)

values, count = np.unique(np.argmax(y_test, axis=1), return_counts=True)
plt.bar(values, count)
plt.show()


# # Training

# Model Definition
input_shape = X_train[0].shape
num_genres = 4

def createCNN1():
    model = Sequential()
    # Conv Block 1
    model.add(Conv2D(16, kernel_size=(3, 3), padding="same", activation='relu', input_shape=input_shape))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.1))

    # Conv Block 2
    model.add(Conv2D(32, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.1))

    # Conv Block 3
    model.add(Conv2D(64, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.1))

    # Conv Block 4
    model.add(Conv2D(128, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.1))

    # # Conv Block 5
    model.add(Conv2D(256, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.1))

    # MLP
    model.add(Flatten())
    model.add(Dense(num_genres, activation='softmax'))

    model.summary()
    model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])
    return model


def createCNN2():
    model = Sequential()
    # Conv Block 1
    model.add(Conv2D(128, kernel_size=(3, 3), padding="same", activation='relu', input_shape=input_shape))
    model.add(Conv2D(128, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.5))

    model.add(Conv2D(64, kernel_size=(3, 3), padding="same", activation='relu'))
    model.add(Conv2D(64, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.5))
    
    model.add(Conv2D(32, kernel_size=(3, 3), padding="same", activation='relu'))
    model.add(Conv2D(32, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.5))
    
    model.add(Conv2D(16, kernel_size=(3, 3), padding="same", activation='relu'))
    model.add(Conv2D(16, (3, 3), padding="same", activation='relu'))
    model.add(MaxPooling2D(2))
    model.add(Dropout(0.5))
              
    model.add(Flatten())
    model.add(Dense(num_genres, activation='softmax'))

    model.summary()
    model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy'])
    return model


model = createCNN2()

hist = model.fit(X_train, y_train,
          batch_size=64,
          epochs=20,
          validation_split=0.2)


score = model.evaluate(X_test, y_test, verbose=0)
print("test_loss = {:.3f} and test_acc = {:.3f}".format(score[0], score[1]))


plt.figure(figsize=(15,7))

plt.subplot(1,2,1)
plt.plot(hist.history['acc'], label='train')
plt.plot(hist.history['val_acc'], label='validation')
plt.title('Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.legend()

plt.subplot(1,2,2)
plt.plot(hist.history['loss'], label='train')
plt.plot(hist.history['val_loss'], label='validation')
plt.title('Loss')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.legend()

plt.tight_layout()
plt.show()


#http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Oranges):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')


preds = np.argmax(model.predict(X_test), axis = 1)
y_orig = np.argmax(y_test, axis = 1)
cm = confusion_matrix(preds, y_orig)
print(cm)

keys = OrderedDict(sorted(genres.items(), key=lambda t: t[1])).keys()

plt.figure(figsize=(8,8))
plot_confusion_matrix(cm, keys, normalize=True)


# ## Save the model
# Save the model
model.save('../models/nbs_deeplearning.h5')

