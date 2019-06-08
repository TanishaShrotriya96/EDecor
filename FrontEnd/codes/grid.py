#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 07:28:08 2019

@author: tanisha
"""


#============================== GRID SEARCH ======================================================    
activation =  ['relu', 'tanh', 'sigmoid', 'hard_sigmoid', 'linear'] # softmax, softplus, softsign 
momentum = [0.0, 0.2, 0.4, 0.6, 0.8, 0.9]
learn_rate = [0.001, 0.01, 0.1, 0.2, 0.3]
dropout_rate = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
weight_constraint=[1, 2, 3, 4, 5]
neurons = [1, 5, 10, 15, 20, 25, 30]
init = ['uniform', 'lecun_uniform', 'normal', 'zero', 'glorot_normal', 'glorot_uniform', 'he_normal', 'he_uniform']
optimizer = [ 'SGD', 'RMSprop', 'Adagrad', 'Adadelta', 'Adam', 'Adamax', 'Nadam']

# grid search epochs, batch size
epochs = [1, 10] # add 50, 100, 150 etc
batch_size = [1000, 5000] # add 5, 10, 20, 40, 60, 80, 100 etc
param_grid = dict(epochs=epochs, batch_size=batch_size)
##############################################################
grid = grid(estimator=model, param_grid=param_grid, n_jobs=-1)
grid_result = grid.fit(X, Y) 
##############################################################
# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

    
train_datagen=ImageDataGenerator(preprocessing_function=preprocess_input,
                                 rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True) #included in our dependencies
test_datagen = ImageDataGenerator(rescale = 1./255,preprocessing_function=preprocess_input)
train_datagen
train_generator=train_datagen.flow_from_directory('/home/tanisha/EDecor/FrontEnd/Stylizer/colors/train',
                                                 target_size=(224,224),
                                                 color_mode='rgb',
                                                 batch_size=32,
                                                 class_mode='categorical',
                                                 shuffle=True)
train_generator.samples
train_generator.batch_index
test_set = test_datagen.flow_from_directory('/home/tanisha/EDecor/FrontEnd/Stylizer/colors/test',
                                            target_size=(224,224),
                                             color_mode='rgb',
                                             batch_size=32,
                                             class_mode='categorical',
                                             shuffle=True)

step_size_train=train_generator.n//train_generator.batch_size
step_size_train

grid_result=grid.fit_generator(generator=train_generator,
               steps_per_epoch=step_size_train,
               epochs=5,
               shuffle=True,
               use_multiprocessing=True)
