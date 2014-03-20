#coding: utf-8
from storage import PickleStorage

class LshBucket(object):
    """Data bucket class

    >>> from buckets import LshBucket
    >>> bucket = LshBucket()
    >>> bucket.insert(vector, hashed_array)
    >>> bucket.select(vector, hashed_array)
    """

    def __init__(self, **kw):
        self.L = 0

        for key, value in kw.iteritems():
            setattr(self, key, value)

        self.data = [{} for i in xrange(self.L)]#包含L个哈希表，表中存有哈希值及其对应的向量
        self.index = [[] for i in xrange(self.L)]#包含L个列表，每个列表里包含对应哈希表中的哈希值
        self.storage = PickleStorage()


    def insert(self, vector, hashed_array ):
        assert len(self.data) == self.L
        assert len(self.index) == self.L
        assert len(hashed_array) == self.L
        #assert <test> , <data>
        #if <test> is false, raise error

        L = self.L

        for i in xrange(L):
            self._putInBucket(i,vector,hashed_array[i])

    def store_buckets(self):
        fw1 = open("buckets.data",'wb')
        self.storage.save(self.data,fw1)
        fw1.close()

        fw2 = open("buckets_index.data",'wb')
        self.storage.save(self.index,fw2)
        fw2.close()

    def load_buckets(self):
        fr1 = open('buckets.data')
        self.data = self.storage.load(fr1)
        fr1.close()

        fr2 = open('buckets_index.data')
        self.index = self.storage.load(fr2)
        fr2.close()

    def select(self,query_vector,hashed_array,without_itself=False):
        assert len(self.data) == self.L
        assert len(hashed_array) == self.L

        query_vector_tuple = tuple(query_vector)
        L = self.L
        result = []
        seen = {}

        for i in xrange(L):
            hashed = "".join(map(str,hashed_array[i]))
            data = self.data[i]
            vectors = data.get(hashed,[])#return the list of vectors pointed to hashed

            for vector in vectors:
                key = tuple(vector)
                if key in seen:
                    continue
                if key == query_vector_tuple and without_itself:#是否忽略完全一样的
                    continue

                seen[key] = True
                result.append(vector)

            if len(result) >= L*2:
                break

        return result#a list that composed of vectors


    def _putInBucket(self,i,vector,hashed_array):
        """
        this func build the relationship of (data[hashed] = vector)
        and build the index of hashed_array
        """
        index = self.index[i]
        hashed_array = "".join(map(str, hashed_array))
        #"".join() return an object of string type
        #map() Apply function to every item of iterable and return a list of the results.
        self.index[i] = sorted(set(index + [hashed_array]))
        data = self.data[i]
        if hashed_array not in data:
            data[hashed_array] = []
        data[hashed_array].append(vector)
