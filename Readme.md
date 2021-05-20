Music Genre Classification

Domain: Machine Learning

Technologies & Concepts: GTZAN Dataset, SoX, FFT ( Fast Fourier Transform), MFCC ( Mel Frequency Cepstral Co-efficient), Librosa, SciPy, Matplotlib.py plot, Confusion Matrix, Sklearn, Vgg-16 architecture, LR, KNN, SVM, CNN, convo 2D, Maxpooling 2D, Dl, ML, AI

The purpose of this project was to implement Machine Learning to classify music into different genres. The Machine Learning Algorithms used for this purpose were Logistic Regression, KNN, SVM. To have a benchmark comparison, a deep learning algorithm, CNN was also used, and the performances were evaluated.
The dataset used was the GTZAN dataset from the Marysas Website. It consists of music of 6 genres each having audio clips in .au
The audio files are converted to .wav format.
Features are extracted using FFT and MFCC.
CNN model is built using Vgg-16 Architecture (16 Layers) i.e., four Layers are run four times. The layers consist of Convo2D Layer twice, Maxpooling 2D, Dropout Layer.
Model is tested on the Validation dataset.
Performance is compared.
While FFT gave results of 67.5% for LR, 70% for KNN, 75% for SVM. 
MFCC gave results of 85% for LR, 77.5% for KNN, 85% for SVM, 95% for CNN.
Our project concludes that MFCC-CNN pair performed the best amongst all the models yielding an accuracy of 95%.
