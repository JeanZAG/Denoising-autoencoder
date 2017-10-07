###Algorihtm first implemented for UPMC-Isir
###it's due to be integrated to SyncPy 
###https://github.com/syncpy/SyncPy/tree/master/src/Methods/utils
### it should appear soon in this link 
###
### module author : Jean Zagdoun 


import numpy as np
import tensorflow as tf


tf.reset_default_graph()
sess=tf.InteractiveSession()


def Gaussian(x):
    x = x + np.random.normal(0,1,x.shape)
    return x

def encoding_process(batch, Weight, Biases):
    H = tf.nn.sigmoid(tf.add(tf.matmul(batch,Weight),Biases))
    return H

def decoding_process(encoded_batch, Weight, Biases):
    H = tf.nn.sigmoid(tf.add(tf.matmul(encoded_batch,Weight),Biases))
    return H

def DAE(data, Archi, noise = Gaussian, batch_size = 500,pre_pross=True, training_epochs=5, learning_rate = 0.01, decoder=False,disp_step=30):
    """
   Computes the denoising-autoencoder algorithm:
       
   It's a non-supervised deep learning algorithm
   every layer of the neural net is trained to encode in the best way possible so that it will be able to reconstruct data from the previous layer.
   The algorithm can be used just for pre-processing in that case you are just interested in finding the encoding weights,
   but decoding weights can also be usefull for exemple if you want to compare imitation as a social behavior or 
   if you want to know if a part of an specific image is hidden by a random object

   **reference paper** : 
   
       -Pascal Vincent, Stacked Denoising Autoencoders: Learning Useful Representations in a Deep Network with a Local Denoising Criterion
       -Andrew NG, CS294A Lecture notes, Sparse autoencoder
   
   Almost every TensorFlow objects are writen as dictionnary as the architecture of the neural net is left to the user.
   Cost and optimizer are also stored in dictionnaries so that the graph is totally defined before any run 
   
   parameters :
       :param data: a numpy-array containing the training data
       
       :param Archi: a list containing the archistecture of your neural net each element of the list indicates the number of neurones per hidden layers
       (exemple [225,121] represent a neural network with 225 neurone in the first hidden layer and 121 in the second one)
       
       :param noise: just Gaussian noise is avalable for now
       
       :param batch_size: size of the batches
       
       :param training_epochs: the number of times you want your neural network to run over all your dataset
       
       :param learning_rate: the learning rate used in the optimizer
       
       :param decoder: boolean, if True returns the weight of the encoding and the decoding process.
       
    returns : E_Weights, E_Biases two dictionnary containing your weights 
    can also return E_Weights, E_Biases, D_Weights, D_Biases if you want the encoding and decoding weights
    
    to see an exemple of utilisation see '/SyncPy-master/exemples/DAE_exemple'
    to see an exemple of utilisation in case of preprocessing '/SyncPy-master/exemples/DAE_pre_processing
    
    NB: do not declare a tf.Sessoin() before or after using DAE instead use the current DAE session.
    To do so you need to enter "sess = tf.get_default_session() "
     """
     
    input_size = data.shape[1]
    Archi = np.array(Archi)
    l = Archi.size
    E_Weights = {}; E_Biases = {}
    D_Weights = {}; D_Biases = {}    
    I_P = {} ;
    cost = {} ; opt = {}
    
    """placeholders initialisation"""
    for i in range(l):
        if i == 0:
            I_P['P'+str(i)] = tf.placeholder(tf.float32, [batch_size,input_size])
        else :
            I_P['P'+str(i)] = tf.placeholder(tf.float32, [batch_size,Archi[i-1]])

    """Weights and Biases initialisation for the Encoding process"""
    for i in range(1,l+1):
        if i ==1:
            E_Weights['W'+str(i)] = tf.Variable(tf.random_normal([input_size,Archi[i-1]],0,0.1))
        else:
            E_Weights['W'+str(i)] = tf.Variable(tf.random_normal([Archi[i-2],Archi[i-1]],0,0.1))
    for i in range(1,l+1):
        E_Biases['B'+str(i)] = tf.Variable(tf.random_normal([Archi[i-1]],0,0.1))
        
    """Weights and Biases initialisation for the Decoding process"""
    for i in range(1,l+1):
        if i ==1:
            D_Weights['W'+str(i)] = tf.Variable(tf.random_normal([Archi[i-1],input_size],0,0.1))
        else:
            D_Weights['W'+str(i)] = tf.Variable(tf.random_normal([Archi[i-1],Archi[i-2]],0,0.1))
    for i in range(1,l+1):
        if i ==1:
            D_Biases['B'+str(i)] = tf.Variable(tf.random_normal([input_size],0,0.1))
        else:
             D_Biases['B'+str(i)] = tf.Variable(tf.random_normal([Archi[i-2]],0,0.1))
             
    """definition of the cost functions"""
    for i in range(l):
        E = encoding_process(I_P['P'+str(i)],E_Weights['W'+str(i+1)],E_Biases['B'+str(i+1)]) 
        D = decoding_process(E,D_Weights['W'+str(i+1)],D_Biases['B'+str(i+1)])
        cost['c' +str(i)] = tf.reduce_mean(tf.pow(I_P['P'+str(i)]-D,2))

    """definition of the optimizers"""
    for i in range(l):
        opt['o'+str(i)] = tf.train.AdamOptimizer(learning_rate).minimize(cost['c' +str(i)])
    
    
    
    """training process"""    
    init = tf.global_variables_initializer()
    sess.run(init)
    total_batch = int(data.shape[0]/batch_size)
    for i in range(l):
        print('\n')
        print("###################################")
        print("#   optimizing layer nubmer : " +str(i+1) +"   #")
        print("###################################\n")
        if i == 0:
            data = data
#seem redondant but it's important to understand the logic of the code i think
        else :
            W = E_Weights['W'+str(i)].eval()
            B = E_Biases['B'+str(i)].eval()
            data = tf.nn.sigmoid(tf.add(tf.matmul(data,W),B)).eval()
        for epochs in range(training_epochs):
            print('epochs number :'+str(epochs+1))
            for j in range(total_batch):
                U = data[j*batch_size:(j+1)*batch_size,:]
                _,c = sess.run([opt['o'+str(i)],cost['c' +str(i)]],feed_dict={I_P['P'+str(i)] : U})
                if j % disp_step == 0:
                    print("the cost is : " +str(c))
    
    """In case you want to use DAE for pre-processing, so you can initialize your variable in the same time that every thing else"""
    if pre_pross == True:
        l = []
        for key in E_Weights:
            val = E_Weights[key].eval()
            E_Weights[key] = tf.Variable(val)
            l.append(E_Weights[key])
        for key in E_Biases:
            val = E_Biases[key].eval()
            E_Biases[key] = tf.Variable(val)
            l.append(E_Biases[key])
            
        init = tf.variables_initializer(l)
        sess.run(init)


    """return """    
    if decoder == True:
        return E_Weights, E_Biases, D_Weights, D_Biases
    else:
        return E_Weights, E_Biases



    
    
    
    
    
