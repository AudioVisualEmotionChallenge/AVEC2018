import numpy as np

# Helper functions
def get_num_lines(filename, skip_header=False):
    with open(filename, 'r') as file:
        c = 0
        if skip_header:
            c = -1
        for line in file:
            c += 1
    return c

def get_num_columns(filename, delim=';', skip_header=False):
    # Returns the number of columns in a csv file
    # First two columns must be 'instance name' and 'timestamp' and are not considered in the output
    with open(filename, 'r') as file:
        if skip_header:
            next(file)
        line = next(file)
        offset1 = line.find(delim)+1
        offset2 = line[offset1:].find(delim)+1+offset1
        cols = np.fromstring(line[offset2:], dtype=float, sep=delim)
    return len(cols)

def read_csv(filename, delim=';', skip_header=False):
    # Returns the content of a csv file (delimiter delim, default: ';')
    # First two columns must be 'instance name' and 'timestamp' and are not considered in the output, header is skipped if skip_header=True
    num_lines = get_num_lines(filename, skip_header)
    data = np.empty((num_lines,get_num_columns(filename,delim,skip_header)), float)
    with open(filename, 'r') as file:
        if skip_header:
            next(file)
        c = 0
        for line in file:
            offset1 = line.find(delim)+1
            offset2 = line[offset1:].find(delim)+1+offset1
            data[c,:] = np.fromstring(line[offset2:], dtype=float, sep=delim)
            c += 1
    return data


def load_features(path_features='../audio_features_xbow/', partition='Train_DE', num_inst=34, max_seq_len=1768):
    skip_header  = False  # AVEC 2018 XBOW feature files
    num_features = get_num_columns(path_features + '/' + partition + '_01.csv', delim=';', skip_header=skip_header)  # check first 
    
    features = np.empty((num_inst, max_seq_len, num_features))
    for n in range(0, num_inst):
        F = read_csv(path_features + '/' + partition + '_' + str(n+1).zfill(2) + '.csv', delim=';', skip_header=skip_header)
        if F.shape[0]>max_seq_len:
            F = F[:max_seq_len,:]  # cropping
        features[n,:,:] = np.concatenate((F, np.zeros((max_seq_len - F.shape[0], num_features))))  # zero padding
    
    return features


def load_labels(path_labels='../labels/', partition='Train_DE', num_inst=34, max_seq_len=1768, targets=[0,1,2]):
    # targets=[0,1,2]: 0: arousal, 1: valence, 2: liking/likability
    skip_header = False  # AVEC 2018 XBOW labels files
    num_labels  = len(targets)
    
    labels_original = []
    labels_padded   = []
    
    for t in targets:
        labels_original_t = []
        labels_padded_t   = np.empty((num_inst, max_seq_len, 1))
        
        for n in range(0, num_inst):
            yn = read_csv(path_labels + partition + '_' + str(n+1).zfill(2) + '.csv', skip_header=skip_header)
            yn = yn[:,t].reshape((yn.shape[0], 1))  # select only target dimension and reshape to 2D array
            # original length
            labels_original_t.append(yn)
            # padded to maximum length
            if yn.shape[0] > max_seq_len:
                yn = yn[:max_seq_len]
            labels_padded_t[n,:,:] = np.concatenate((yn, np.zeros((max_seq_len - yn.shape[0], 1))))  # zero padding        
        labels_original.append(labels_original_t)
        labels_padded.append(labels_padded_t)
    
    return labels_original, labels_padded


def load_CES_data(use_audio=True, use_visual=True, use_linguistic=True, targets=[0,1,2]):
    num_train_DE = 34  # number of recordings
    num_devel_DE = 14
    num_test_DE = 16
    num_test_HU = 66
    
    max_seq_len = 1768  # maximum number of labels
    
    # Initialise numpy arrays
    train_DE_x = np.empty((num_train_DE, max_seq_len, 0))
    devel_DE_x = np.empty((num_devel_DE, max_seq_len, 0))
    test_DE_x  = np.empty((num_test_DE,  max_seq_len, 0))
    test_HU_x  = np.empty((num_test_HU,  max_seq_len, 0))
    
    if use_audio:
        train_DE_x = np.concatenate( (train_DE_x, load_features(path_features='../audio_features_xbow/', partition='Train_DE', num_inst=num_train_DE, max_seq_len=max_seq_len) ), axis=2)
        devel_DE_x = np.concatenate( (devel_DE_x, load_features(path_features='../audio_features_xbow/', partition='Devel_DE', num_inst=num_devel_DE, max_seq_len=max_seq_len) ), axis=2)
        test_DE_x  = np.concatenate( (test_DE_x,  load_features(path_features='../audio_features_xbow/', partition='Test_DE',  num_inst=num_test_DE,  max_seq_len=max_seq_len) ), axis=2)
        test_HU_x  = np.concatenate( (test_HU_x,  load_features(path_features='../audio_features_xbow/', partition='Test_HU',  num_inst=num_test_HU,  max_seq_len=max_seq_len) ), axis=2)
    if use_visual:
        train_DE_x = np.concatenate( (train_DE_x, load_features(path_features='../visual_features_xbow/', partition='Train_DE', num_inst=num_train_DE, max_seq_len=max_seq_len) ), axis=2)
        devel_DE_x = np.concatenate( (devel_DE_x, load_features(path_features='../visual_features_xbow/', partition='Devel_DE', num_inst=num_devel_DE, max_seq_len=max_seq_len) ), axis=2)
        test_DE_x  = np.concatenate( (test_DE_x,  load_features(path_features='../visual_features_xbow/', partition='Test_DE',  num_inst=num_test_DE,  max_seq_len=max_seq_len) ), axis=2)
        test_HU_x  = np.concatenate( (test_HU_x,  load_features(path_features='../visual_features_xbow/', partition='Test_HU',  num_inst=num_test_HU,  max_seq_len=max_seq_len) ), axis=2)
    if use_linguistic:
        train_DE_x = np.concatenate( (train_DE_x, load_features(path_features='../linguistic_features_xbow/', partition='Train_DE', num_inst=num_train_DE, max_seq_len=max_seq_len) ), axis=2)
        devel_DE_x = np.concatenate( (devel_DE_x, load_features(path_features='../linguistic_features_xbow/', partition='Devel_DE', num_inst=num_devel_DE, max_seq_len=max_seq_len) ), axis=2)
        test_DE_x  = np.concatenate( (test_DE_x,  load_features(path_features='../linguistic_features_xbow/', partition='Test_DE',  num_inst=num_test_DE,  max_seq_len=max_seq_len) ), axis=2)
        test_HU_x  = np.concatenate( (test_HU_x,  load_features(path_features='../linguistic_features_xbow/', partition='Test_HU',  num_inst=num_test_HU,  max_seq_len=max_seq_len) ), axis=2)
    
    _                       , train_DE_y = load_labels(path_labels='../labels/', partition='Train_DE', num_inst=num_train_DE, max_seq_len=max_seq_len, targets=targets)
    devel_DE_labels_original, devel_DE_y = load_labels(path_labels='../labels/', partition='Devel_DE', num_inst=num_devel_DE, max_seq_len=max_seq_len, targets=targets)
    
    return train_DE_x, train_DE_y, devel_DE_x, devel_DE_y, test_DE_x, test_HU_x, devel_DE_labels_original

