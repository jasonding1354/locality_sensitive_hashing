#coding: utf-8
import random
SCALE = 15

class BaseHash(object):

    def __init__(self, **kw):
        for key, value in kw.iteritems():
            setattr(self, key, value)


class HammingHash(BaseHash):
    """Hash function class (Hamming Distance)

    >>> from LSH.hash import HammingHash
    >>> hash = HammingHash()
    >>> hashed_array = hash.do_hashing([123, 456, 789])
    """

    def do_hashing(self,vector):
        if not isinstance(vector, (list, tuple)):
            raise TypeError("args should be an array_ref")

        if getattr(self, "d", None) is None:
            self.d = len(vector)

        if self.d != len(vector):
            raise ValueError("invalid dimention number")

        unary_code = self._unarize(vector)
        hash = []
        for i in xrange(self.L):    #the number of hash function
            sampling_bits = self.indexes[i]
            hash.append([unary_code[bit] for bit in sampling_bits])
        return hash


    @property #only read
    def indexes(self):
        if getattr(self, "_indexes", None) is None:
            self._indexes = self._create_indexes()
        return self._indexes

    def _create_indexes(self):
        indexes = []
        for i in xrange(self.L):
            sampling_bits = set()
            #A set object is an unordered collection of distinct hashable objects
            while True:
                bit = random.randint(0, self.d * SCALE - 1)
                if bit not in sampling_bits:
                    sampling_bits.add(bit)
                    if len(sampling_bits) == self.k * SCALE:
                        break
            indexes.append(sorted(sampling_bits))
        return indexes

    def _unarize(self, vector):
        n = float(SCALE) / max(vector)
        unary = []
        for x in vector:
            i = int(x * n)
            j = SCALE - i
            unary += [1] * i
            unary += [0] * j
        return unary