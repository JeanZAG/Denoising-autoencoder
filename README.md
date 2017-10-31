# Denoising-autoencoder

Implementation of the Denoising-autoencoder algorithm, it's an unsupervised deep-learning methode that can be used for many task from preprocessing to computer vision.

This code was originally intended for the SyncPy library : https://github.com/syncpy/SyncPy and is also avalable in https://github.com/syncpy/SyncPy/tree/master/src/Methods/utils


This algorithm comes with two exemple of utilisation:

  -One that shows you exactly how the autoencoder is reconstructing data : it's a visual proof that the algortihm works properly.  
  -One is an exemple of how you should this code if you are doing preprocessing.

Both exemples works on MNIST dataset.

dependencies : Python 2.7, TensorFlow, numpy, matplotlib

If you are using Python with version > 3 you have to change in the last line of DAE\_exemple.py the "raw\_input" into "input" and it should work just fine (tested for python 3.6.2)

