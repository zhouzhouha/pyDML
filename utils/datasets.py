#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 12:28:34 2018

@author: jlsuarezdiaz
"""

import numpy as np
import pandas as pd
from sklearn.datasets import load_iris, load_digits
from six.moves import xrange
from .arff_reader import read_ARFF
import os.path

def iris():
    data=load_iris()  # IRIS
    X=data['data']
    y=data['target']

    return X,y  

def simetria_hor(A):
    nrow, ncol= A.shape
    A = np.abs(A-A[:,::-1]) # Diferencia con la imagen simétrica
    return np.mean(A)                  # Media de las diferencias (grado de simetría)

def simetria_ver(A):
    nrow, ncol= A.shape
    A = np.abs(A-A[::-1,:]) # Diferencia con la imagen simétrica
    return np.mean(A)                  # Media de las diferencias (grado de simetría)


def digits(numbers=None):
    data=load_digits()     # DIGITS
    X=data['data']
    y=data['target']
    
    if numbers is None:
        numbers=[0,1,2,3,4,5,6,7,8,9]
        
    selected = np.where(np.isin(y,numbers))[0]
    return X[selected,:], y[selected]

    return X,y

def digits_reduced():
    data=load_digits()
    XX = data['data']
    y = data['target']
    nn,dd = XX.shape
    XX = XX.reshape([nn,8,8])

    X = np.empty([nn,3])
    for i in xrange(nn):
        X[i,0] = simetria_hor(XX[i,:,:])
        X[i,1] = simetria_ver(XX[i,:,:])
        X[i,2] = np.mean(XX[i,:])
    
    return X,y

### ARFF dataframes ###
def sonar():
    X,y,m = read_ARFF("./data/sonar.arff",-1)          # SONAR

    return X,y

def wdbc():
    X,y,m = read_ARFF("./data/wdbc.arff",0)            # WDBC

    return X,y

def spambase():
    X,y,m = read_ARFF("./data/spambase-460.arff",-1)   # SPAMBASE-460

    return X,y


### CSV dataframes ###
def wine():
    data = pd.read_csv("./data/wine.data",header=None)              # WINE
    X = data.iloc[:,1:].values        
    y=data.iloc[:,0].values

    return X,y

def letters(letters=None):
    if letters is None:
        letters = [chr(i) for i in range(ord('A'),ord('Z')+1)]
        
    data = pd.read_csv("./data/letter-recognition.data",header=None)
    X = data.iloc[:,1:].values
    y = data.iloc[:,0].values
    selected = np.where(np.isin(y,letters))[0]
    return X[selected,:], y[selected]

def isolet(subset = "train"):
    if subset == "train":
        data = pd.read_csv("./data/isolet_train.data",header=None)
    elif subset == "test":
        data = pd.read_csv("./data/isolet_test.data",header=None)
    else:
        raise ValueError("which argument must be 'train' or 'test'")
    X = data.iloc[:,:-1].values
    y = data.iloc[:,-1].values
    
    return X, y

def balance():
    data = pd.read_csv("./data/balance-scale.data",header=None)
    X = data.iloc[:,1:].values
    y = data.iloc[:,0].values
    return X, y
    


