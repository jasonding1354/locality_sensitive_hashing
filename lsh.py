#coding: utf-8

"""
DESCRIPTION
===========
This module is a Python implementation of Locality Sensitive Hashing,
which is a alpha version.

AUTHOR
===========
Jason Ding(ding1354@gmail.com)

LICENCE
===========
This module is free software that you can use it or modify it.
"""
#encoding:utf-8

import math
import numpy as np
from hamminghash import HammingHash
from buckets import LshBucket

from bitarray import bitarray
"""
try:
    from bitarray import bitarray
expect ImportError:
    bitarray = None
"""

class LSHBase(object):
    """
    Base class for LSH
    """

    def __init__(self, **kw):
        for key, value in kw.iteritems():
            setattr(self, key, value)

    def _check_parameters(self):
        for param in ('d', 'L', 'k'):
            if not hasattr(self, param):
                raise TypeError("parameter 'param' is necessary")
        if self.k > self.d:
            raise ValueError("parameter 'k' must be smaller than parameter 'd'")


class LSH(LSHBase):
    """
     >>> from LSH import LSH

    >>> lsh = LSH(
    ...     L=L,   # number of hash functions
    ...     k=k,   # number of reductions
    ...     d=d,   # number of dimentions
    ... )
    """

    def __init__(self, L, k, d, **kw):
        super(LSH, self).__init__(L=L, k=k, d=d, **kw)
        self._check_parameters()

        self.hash = HammingHash(L=L, k=k, d=d)
        self.bucket = LshBucket(L=L, k=k, d=d)

    """
    def file2vector(filename):
        fr = open(filename)
        arrayOfLines = fr.readlines()
        numOfLines = len(arrayOfLines)
        retMatrix = np.zeros((numOfLines,11))

    def loadDataSet(self, fileName, delim=','):
        dataMat = np.loadtxt(fileName, delimiter=delim)
        return np.mat(dataMat)
    """

    def loadDataSet(self,filename,delim=','):
        fr = open(filename)
        arrayOfLines = fr.readlines()
        #numOfLines = len(arrayOfLines)
        for line in arrayOfLines:
            line = line.strip()
            arrayFromLine = line.split(delim)
            vectFromLine = [int(x) for x in arrayFromLine]#transform the string type to integer
            self.insert(vectFromLine)

    def insert(self, vector):
        """insert a vector data to buckets"""
        hashed_array = self.hash.do_hashing(vector)
        self.bucket.insert(vector, hashed_array)

    def nn(self, vector, without_itself=False):#nearest_neighbours
        neighbours = self._neighbours(vector,without_itself)
        nearest_vector = self._nearest(vector,neighbours)
        return nearest_vector

    def knn(self,vector,kk,without_itself=False):
        neighbours = self._neighbours(vector,without_itself)
        knn_vectors = self._k_nearest(vector,kk,neighbours)
        return knn_vectors

    def _neighbours(self, vector, without_itself=False):
        """this function extracts some vectors as neighbours with query vector"""
        hashed_array = self.hash.do_hashing(vector)
        neighbours = self.bucket.select(vector, hashed_array, without_itself)
        return neighbours

    def _k_nearest(self, vector, kk, neighbours):
        knn_list = []
        for n_vector in neighbours:
            dist = self._euclidean_dist(vector,n_vector)
            if len(knn_list) < kk:
                knn_list.append({'distance':dist,'vector':n_vector})
                continue

            knn_list.sort()#sort from small to large
            maximum_dist = knn_list[2]['distance']
            if dist < maximum_dist:
                knn_list[2] = {'distance':dict,'vector':n_vector}
        return knn_list

    def _nearest(self, vector, neighbours):
        """pick up the nearest vector from neighbours"""
        nearest = {}
        for n_vector in neighbours:
            dist = self._euclidean_dist(vector,n_vector)
            if "distance" not in nearest or dist < nearest["distance"]:
                """
                'distance' is the key of dictionary(nearest)
                'distance' is not in the dict,then build it
                dist is shorter,then update
                """
                nearest.update(vector = n_vector,distance = dist)
        return nearest

    def _hamming_dist(self, hashval1, hashval2):
        xor_result = bitarray(hashval1) ^ bitarray(hashval2)
        return xor_result.count()

    def _euclidean_dist(self, vector1, vector2):
        sum = 0
        for x1, x2 in zip(vector1, vector2):
            d = (x1 - x2) ** 2
            sum += d
        return math.sqrt(sum)


if __name__ == '__main__':
    lsh = LSH(L=10,k=5,d=11)
    lsh.loadDataSet('training_set1.txt')
    vect = [1,10,1,11,1,13,1,12,1,1,9]
    knn_vects = lsh.knn(vect,3)
    print knn_vects
