from __future__ import print_function
import os
import numpy as np
import keras.backend as K
from keras.models import Model
from keras.layers import Input, Dense, Masking, LSTM, TimeDistributed, Bidirectional
from keras.optimizers import RMSprop
from CES_data import load_CES_data
from calc_scores import calc_scores
from write_csv import save_features

from numpy.random import seed
from tensorflow import set_random_seed


def emotion_model(max_seq_len, num_features, learning_rate, num_units_1, num_units_2, bidirectional, dropout, num_targets):
    # Input layer
    inputs = Input(shape=(max_seq_len,num_features))
    
    # Masking zero input - shorter sequences
    net = Masking()(inputs)
    
    # 1st layer
    if bidirectional:
        net = Bidirectional(LSTM( num_units_1, return_sequences=True, dropout=dropout, recurrent_dropout=dropout))(net)
    else:
        net = LSTM(num_units_1, return_sequences=True, dropout=dropout, recurrent_dropout=dropout)(net)
    
    # 2nd layer
    if bidirectional:
        net = Bidirectional(LSTM( num_units_2, return_sequences=True, dropout=dropout, recurrent_dropout=dropout ))(net)
    else:
        net = LSTM(num_units_2, return_sequences=True, dropout=dropout, recurrent_dropout=dropout)(net)
    
    # Output layer
    outputs = []
    out1 = TimeDistributed(Dense(1))(net)  # linear activation
    outputs.append(out1)
    if num_targets>=2:
        out2 = TimeDistributed(Dense(1))(net)  # linear activation
        outputs.append(out2)
    if num_targets==3:
        out3 = TimeDistributed(Dense(1))(net)  # linear activation
        outputs.append(out3)
    
    # Create and compile model
    rmsprop = RMSprop(lr=learning_rate)
    model   = Model(inputs=inputs, outputs=outputs)
    model.compile(optimizer=rmsprop, loss=ccc_loss)  # CCC-based loss function
    return model


def main():
    ## Configuration
    path_output = 'predictions/'  # To store the predictions on the test partitions
    
    # Modalities
    use_audio      = True
    use_visual     = True
    use_linguistic = False
    
    # Neural net parameters
    batch_size    = 34       # Full-batch: 34 sequences
    learning_rate = 0.001    # default is 0.001
    num_iter      = 50       # Number of Iterations
    num_units_1   = 64       # Number of LSTM units in LSTM layer 2
    num_units_2   = 64       # Number of LSTM units in LSTM layer 2
    bidirectional = False    # True/False
    dropout       = 0.1      # Dropout
    
    # Targets
    targets       = [0,1,2]  # List of targets: 0=arousal, 1=valence, 2=liking
    shift_sec     = 2.0      # Shift of annotations for training (in seconds)
    
    ##
    target_names = {0: 'arousal', 1: 'valence', 2: 'liking'}
    inst_per_sec = 10  # 100ms hop size
    
    # Set seeds to make results reproducible 
    # (Note: Results might be different from those reported by the Organisers as seeds also training depends on hardware!)
    seed(1)
    set_random_seed(2)
    
    num_targets = len(targets)  # same for all Y
    
    shift = int(np.round(shift_sec*inst_per_sec))  
    
    # Load AVEC2018-CES data
    print('Loading data ...')
    train_x, train_y, devel_x, devel_y, test_x_DE, test_x_HU, devel_labels_original = load_CES_data(use_audio, use_visual, use_linguistic, targets)
    num_train    = train_x.shape[0]
    num_devel    = devel_x.shape[0]
    num_test_DE  = test_x_DE.shape[0]
    num_test_HU  = test_x_HU.shape[0]
    max_seq_len  = train_x.shape[1]  # same for all partitions
    num_features = train_x.shape[2]
    print(' ... done')
    
    # Shift labels to compensate annotation delay
    print('Shifting labels to the front for ' + str(shift_sec) + ' seconds ...')
    for t in range(0, num_targets):
        train_y[t] = shift_labels_to_front(train_y[t], shift)
        devel_y[t] = shift_labels_to_front(devel_y[t], shift)
    print(' ... done')
    
    # Create model
    model = emotion_model(max_seq_len, num_features, learning_rate, num_units_1, num_units_2, bidirectional, dropout, num_targets)
    print(model.summary())
    
    # Train and evaluate model
    ccc_devel_best = np.zeros(num_targets)
    pred_test_DE = []  # Store (best) test predictions
    pred_test_HU = []  # Store (best) test predictions
    for t in range(0, num_targets):  # Initalisation
        pred_test_DE_all = model.predict(test_x_DE)
        pred_test_HU_all = model.predict(test_x_HU)
        if num_targets==1:
            pred_test_DE.append( pred_test_DE_all )
            pred_test_HU.append( pred_test_HU_all )
        else:
            pred_test_DE.append( pred_test_DE_all[t] )
            pred_test_HU.append( pred_test_HU_all[t] )
    
    iteration = 1
    while iteration <= num_iter:
        print('Iteration: ' + str(iteration))
        model.fit(train_x, train_y, batch_size=batch_size, epochs=1)  # Evaluate after each epoch
        
        # Evaluate on development partition
        ccc_iter = evaluate_devel(model, devel_x, devel_labels_original, shift, targets)
        
        # Print results
        print('CCC Devel (', end='')
        for t in range(0, num_targets):
            print(target_names[targets[t]] + ',', end='')
        print('): ' + str(np.round(ccc_iter*1000)/1000))
        
        # Get predictions on test (and shift back) if CCC on Devel improved
        for t in range(0, num_targets):
            if ccc_iter[t] > ccc_devel_best[t]:
                ccc_devel_best[t] = ccc_iter[t]
                pred_test_DE_all = model.predict(test_x_DE)
                pred_test_HU_all = model.predict(test_x_HU)
                if num_targets==1:
                    pred_test_DE[t]  = shift_labels_to_back(pred_test_DE_all, shift)
                    pred_test_HU[t]  = shift_labels_to_back(pred_test_HU_all, shift)
                else:
                    pred_test_DE[t]  = shift_labels_to_back(pred_test_DE_all[t], shift)
                    pred_test_HU[t]  = shift_labels_to_back(pred_test_HU_all[t], shift)
        iteration += 1
    
    # Print best results on development partition
    print('CCC Devel best (', end='')
    for t in range(0, num_targets):
        print(target_names[targets[t]] + ',', end='')
    print('): ' + str(np.round(ccc_devel_best*1000)/1000))
    
    # Write best predictions
    print('Writing predictions on Test partitions for the best models (best CCC on the Development partition) for each dimension into folder ' + path_output)
    write_predictions(path_output, pred_test_DE, targets, target_names, prefix='Test_DE_', inst_per_sec=inst_per_sec)
    write_predictions(path_output, pred_test_HU, targets, target_names, prefix='Test_HU_', inst_per_sec=inst_per_sec)


def evaluate_devel(model, devel_x, label_devel, shift, targets):
    # Evaluate performance (CCC) on the development set
    #  -shift back the predictions in time
    #  -use the original labels (without zero padding)
    num_targets = len(targets)
    CCC_devel   = np.zeros(num_targets)
    # Get predictions
    pred_devel = model.predict(devel_x)
    # In case of a single target, model.predict() does not return a list, which is required
    if num_targets==1:
        pred_devel = [pred_devel]    
    for t in range(0,num_targets):
        # Shift predictions back in time (delay)
        pred_devel[t] = shift_labels_to_back(pred_devel[t], shift)
        CCC_devel[t]  = evaluate_partition(pred_devel[t], label_devel[t])
    return CCC_devel


def evaluate_partition(pred, gold):
    # pred: np.array (num_seq, max_seq_len, 1)
    # gold: list (num_seq) - np.arrays (len_original, 1)
    pred_all = np.array([])
    gold_all = np.array([])
    for n in range(0, len(gold)):
        # padding
        len_original = len(gold[n])
        pred_n = pred[n,:len_original,0]
        # global concatenation - evaluation
        pred_all = np.append(pred_all, pred_n.flatten())
        gold_all = np.append(gold_all, gold[n].flatten())
    ccc, _, _ = calc_scores(gold_all,pred_all)
    return ccc


def write_predictions(path_output, predictions, targets, target_names, prefix='Test_HU_', inst_per_sec=10):
    for t in range(0, len(targets)):
        dimension = target_names[targets[t]]
        out_dir = path_output + dimension + '/'
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        for n in range(0, predictions[t].shape[0]):
            pred_inst = predictions[t][n,:,:]
            # add time stamp
            seq_len    = pred_inst.shape[0]
            time_stamp = np.linspace(0., (seq_len-1)/float(inst_per_sec), seq_len).reshape(-1,1)
            pred_inst  = np.concatenate( (time_stamp, pred_inst), axis=1 )
            instname   = prefix + str(n+1).zfill(2)
            filename   = out_dir + instname + '.csv'
            save_features(filename, pred_inst, append=False, instname=instname, precision=6)


def shift_labels_to_front(labels, shift=0):
    labels = np.concatenate((labels[:,shift:,:], np.zeros((labels.shape[0],shift,labels.shape[2]))), axis=1)
    return labels


def shift_labels_to_back(labels, shift=0):
    labels = np.concatenate((np.zeros((labels.shape[0],shift,labels.shape[2])), labels[:,:labels.shape[1]-shift,:]), axis=1)
    return labels


def ccc_loss(gold, pred):  # Concordance correlation coefficient (CCC)-based loss function - using non-inductive statistics
    # input (num_batches, seq_len, 1)
    gold       = K.squeeze(gold, axis=-1)
    pred       = K.squeeze(pred, axis=-1)
    gold_mean  = K.mean(gold, axis=-1, keepdims=True)
    pred_mean  = K.mean(pred, axis=-1, keepdims=True)
    covariance = (gold-gold_mean)*(pred-pred_mean)
    gold_var   = K.mean(K.square(gold-gold_mean), axis=-1, keepdims=True)
    pred_var   = K.mean(K.square(pred-pred_mean), axis=-1, keepdims=True)
    ccc        = K.constant(2.) * covariance / (gold_var + pred_var + K.square(gold_mean - pred_mean) + K.common.epsilon())
    ccc_loss   = K.constant(1.) - ccc
    return ccc_loss


if __name__ == '__main__':
    main()

