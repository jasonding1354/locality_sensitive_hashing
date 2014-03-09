#coding: utf-8

from lsh import LSH

lsh = LSH(L=10,k=5,d=11)
lsh.loadDataSet('training_set1.txt')
vect = [1,10,1,11,1,13,1,12,1,1,9]
knn_vects = lsh.knn(vect,3)
print knn_vects
