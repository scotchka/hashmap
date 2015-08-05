class Hashmap(object):
    def __init__(self, size=8):
        self.num_filled = 0
        self.keys = [None] * size
        self.values = [None] * size
        self.size = size

    @staticmethod
    def _hash(x):
        return hash(x)

    def put(self, key, value):
        if key is None:
            raise TypeError('key cannot be None')
        index = self._hash(key) % self.size

        step = 0
        while self.keys[index] is not None and self.keys[index] != key and step < self.size - 1:
            # print 'step'
            step += 1
            index = (index + 1) % self.size

        if step == self.size - 1:
            raise Exception('all spaces occupied')

        if self.keys[index] is None:
            self.num_filled += 1

        self.keys[index] = key
        self.values[index] = value

        if self.num_filled > self.size * 0.67:
            self.expand()

    def get(self, key):
        index = self._hash(key) % self.size

        step = 0
        while self.keys[index] != key and step < self.size - 1:
            # print 'step'
            step += 1
            index = (index + 1) % self.size
        if step == self.size - 1:
            raise Exception('key not found')

        return self.values[index]

    def __len__(self):
        return self.num_filled

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __contains__(self, key):
        if self.get(key):
            return True
        else:
            return False

    def __repr__(self):
        non_empty = [(k, v) for k, v in zip(self.keys, self.values) if k is not None]
        string_list = []
        for k, v in non_empty:
            string_list.append(repr(k) + ': ' + repr(v))
        return '{ ' + ', '.join(string_list) + ' }'

    def expand(self):
        old_keys, old_values = self.keys, self.values
        self.__init__(size=self.size * 2)
        for k, v in zip(old_keys, old_values):
            if k is not None:
                self.put(k, v)

if __name__ == '__main__':
    import timeit

    setup = '''
import random, string
from hashmap import Hashmap

hashmap = Hashmap()

def random_string(length=10):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(length))

keys, values = map(random_string, [10] * 10), map(random_string, [5] * 10)

for k, v in zip(keys, values):
    hashmap[k] = v
    assert hashmap[k] == v
'''

    print '10 keys: ', timeit.timeit("hashmap[random.choice(keys)]",  setup=setup)

    setup = '''
import random, string
from hashmap import Hashmap

hashmap = Hashmap()

def random_string(length=10):
    return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase) for _ in range(length))

keys, values = map(random_string, [10] * 1000), map(random_string, [5] * 1000)

for k, v in zip(keys, values):
    hashmap[k] = v
    assert hashmap[k] == v
'''

    print '1000 keys: ', timeit.timeit("hashmap[random.choice(keys)]",  setup=setup)
