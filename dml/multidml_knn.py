#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
k-Nearest Neighbors (kNN)

An interface for kNN adapted to distance metric learning algorithms.
"""

from __future__ import absolute_import
import numpy as np
from sklearn import neighbors
import pandas as pd
from sklearn.model_selection import LeaveOneOut
from .dml_algorithm import DML_Algorithm
from six.moves import xrange
import time

class MultiDML_kNN:
    def __init__(self,n_neighbors,dmls = None, verbose = False,**knn_args):
        self.nn_ = n_neighbors
        self.knn_args_ = knn_args
        self.knns_ = [neighbors.KNeighborsClassifier(n_neighbors,**knn_args)] # EUC
        self.verbose_ = verbose
        self.dmls_ = [None]
        
        if dmls is not None:
            if isinstance(dmls, list):
                for dml in dmls:
                    self.knns_.append(neighbors.KNeighborsClassifier(n_neighbors,**knn_args))
               
                self.dmls_ += dmls
            else:
                self.dmls_ = [None,dmls]
                self.knns_.append(neighbors.KNeighborsClassifier(n_neighbors,**knn_args))

    def add(self,dmls):    
        if isinstance(dmls, list):
            for dml in dmls:
                self.knns_.append(neighbors.KNeighborsClassifier(self.nn_,**self.knn_args_))
           
            self.dmls_.append(dmls)
        else:
            self.dmls_.append(dmls)
            self.knns_.append(neighbors.KNeighborsClassifier(self.nn_,**self.knn_args_))

    def fit(self,X,y):
        self.X_ = X
        self.y_ = y
        self.num_labels_ = len(set(y))
        self.elapsed_ = []

        for i,dml in enumerate(self.dmls_):
            transf = X
            if dml is not None:
                if self.verbose_:
                    print("* Training DML ",type(dml).__name__,"...")
                start = time.time()
                dml.fit(X,y)
                end = time.time()
                transf = dml.transform(X)
                self.elapsed_.append(end - start)
            else:
                self.elapsed_.append(0.0)

            self.knns_[i].fit(transf,y)

        return self
    
    def elapsed(self):
        return self.elapsed_

    def _predict(self,dml=None,knn=None,X=None):
        trans = X
        if X is None:
            trans = self.X_
            if dml is not None:
                trans = dml.transform(trans)
            return self._loo_pred(trans)
        else:
            if dml is not None:
                trans = dml.transform(trans)
            return knn.predict(trans)

    def _predict_proba(self,dml=None,knn=None,X=None):
        trans = X
        if X is None:
            trans = self.X_
            if dml is not None:
                trans = dml.transform(trans)
            return self._loo_prob(trans)
        else:
            if dml is not None:
                trans = dml.transform(trans)
            return knn.predict_proba(trans)        

    def _score(self,dml=None,knn=None,X=None,y=None):
        trans = X
        if X is None:
            trans = self.X_
            if dml is not None:
                trans = dml.transform(trans)
            return self._loo_score(trans)
        else:
            if dml is not None:
                trans = dml.transform(trans)
            return knn.score(trans,y)

    def _loo_pred(self,X):
        loo = LeaveOneOut()
        preds = np.empty([self.y_.size],dtype=self.y_.dtype)

        for train_index, test_index in loo.split(X):
            X_train, X_test = X[train_index], X[test_index]
            y_train  = self.y_[train_index]

            knnloo = neighbors.KNeighborsClassifier(self.nn_)
            knnloo.fit(X_train,y_train)

            preds[test_index]=knnloo.predict(X_test)

        return preds

    def _loo_score(self,X):
        preds = self._loo_pred(X)

        return np.mean(preds == self.y_)

    def predict_all(self,X=None):
        pred_list = []
        for i in xrange(len(self.dmls_)):
            pred_list.append(self._predict(self.dmls_[i],self.knns_[i],X))

        return pred_list

    def predict_proba_all(self,X=None):
        pred_list = []
        for i in xrange(len(self.dmls_)):
            pred_list.append(self._predict(self.dmls_[i],self.knns_[i],X))

        return pred_list

    def score_all(self,X=None,y=None):
        score_array = np.empty([len(self.dmls_)])
        
        for i in xrange(len(self.dmls_)):
            score_array[i] = self._score(self.dmls_[i],self.knns_[i],X,y)

        return score_array

    def dmls_string(self):
        strings=[]
        for dml in self.dmls_:
            if dml is None:
                strings.append("EUCLIDEAN")
            else:
                strings.append(type(dml).__name__)
        return strings