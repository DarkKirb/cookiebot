import random
import hashlib

from warnings import warn as _warn
from types import MethodType as _MethodType, BuiltinMethodType as _BuiltinMethodType
from math import log as _log, exp as _exp, pi as _pi, e as _e, ceil as _ceil
from math import sqrt as _sqrt, acos as _acos, cos as _cos, sin as _sin
from os import urandom as _urandom
#from _collections_abc import Set as _Set, Sequence as _Sequence
from hashlib import sha512 as _sha512
import itertools as _itertools
import bisect as _bisect
sha512c=0
randc=0
def sha512(string):
#    print("sha512(%s)"%string)
    global sha512c
    sha512c=sha512c+1
    return hashlib.sha512(string.encode('UTF-8')).hexdigest()
def sha512i(string):
#    print("sha512i(%s)"%string)
    global sha512c
    sha512c=sha512c+1
    return int.from_bytes(hashlib.sha512(string.encode('UTF-8')).digest(),'little')

class SHARandom(random.Random):
    def __init__(self, seed=0):
        self.sed=seed
    def seed(self, seed):
        self.sed=seed
    def getstate(self):
        return self.sed
    def setstate(self, state):
        self.sed=state
    def random(self):
        global randc
        randc=randc+1
        a,b = sha512i(self.sed)%2**256,sha512i(self.sed)//2**256
        ratio=0.0
        if a<b:
            ratio=a/b
        else:
            ratio=b/a
        self.sed=sha512(repr(ratio))
        return ratio
    def getrandbits(self, i):
        global randc
        randc=randc+1
        a = sha512i(self.sed)%2**i
        self.sed=sha512(self.sed)
        return a
    #backport to not desync on older versions
    def randrange(self,start,stop=None, step=1, _int=int):
        istart = _int(start)
        if istart != start:
            raise ValueError("non-integer arg 1 for randrange()")
        if stop is None:
            if istart > 0:
                return self._randbelow(istart)
            raise ValueError("empty range for randrange()")

        #stop argument supplied
        istop = _int(stop)
        if istop != stop:
            raise ValueError("non-integer stop for randrange()")
        width = istop - istart
        if step == 1 and width > 0:
            return istart + self._randbelow(width)
        if step == 1:
            raise ValueError("empty range for randrange() (%d,%d, %d)" % (istart, istop, width))

        #Non-unit step argument supplied.
        istep = _int(step)
        if istep != step:
            raise ValueError("non-integer step for randrange()")
        if istep > 0:
            n = (width + istep -1) // istep
        elif istep < 0:
            n = (width + istep +1) // istep
        else:
            raise ValueError("zero step for randrange()")
        
        if n <= 0:
            raise ValueError("empty range for randrange()")

        return istart + istep *self._randbelow(n)

    def randint(self,a,b):
        return self.randrange(a, b+1)

    def _randbelow(self, n, int=int, maxsize=1<<53, type=type, Method=_MethodType, BuiltinMethod=_BuiltinMethodType):
       
        if not n:
            raise ValueError("can't choose a random number below 0")
        random = self.random
        getrandbits = self.getrandbits
        # Only call self.getrandbits if the original random() builtin method
        # has not been overridden or if a new getrandbits() was supplied.
        #Overridden.
        #return int(random()*n)
        k = n.bit_length()
        r = getrandbits(k)
        while r >= n:
            r = getrandbits(k)
        return r

    def choice(self, seq):
        try:
            i = self._randbelow(len(seq))
        except ValueError:
            raise IndexError('Cannot choose from an empty sequence')
        return seq[i]

    def shuffle(self, x, random=None):
        randbelow = self._randbelow
        for i in reversed(range(1, len(x))):
            j = randbelow(i+1)
            x[i], x[j] = x[j], x[i]
