"""
This cipher is scheizer. If you use it, you deserve to be hacked.
"""
import math


def phi(n):
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
        i += 1
    if n > 1:
        result -= result // n
    return result


def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    r = int(n ** 0.5)
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f + 2) == 0: return False
        f += 6
    return True


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modular_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


class PrivateKey(object):
    def __init__(self, p, q, e):
        self.block_size = 8

        self.p = p  # prime 1
        self.q = q  # prime 2
        self.n = self.p * self.q

        # totient as φ(n) = (p − 1)(q − 1)
        self.t = (self.p - 1) * (self.q - 1)

        # prime number between 1 and φ(n)
        self.e = e
        assert 1 < self.e < self.t

        self.d = modular_inverse(self.e, self.t)
        assert self.d * self.e % self.t == 1

        # maximum message length defined as φ(n) - 1
        self.max_length = self.t - 1
        self.max_bits = math.floor(math.log(self.max_length, 2))
        self.max_bytes = self.max_bits // 8

    def import_key(self, key):
        pass

    def get_public_key(self):
        return PublicKey(self.e, self.n)

    def decrypt(self, cipher):
        # if hasattr(cipher, "__len__"):
        #     msg = []
        #     for byte in cipher:
        #         msg.append(chr(pow(byte, self.d, self.n)))
        #     return msg

        return pow(cipher, self.d, self.n)

    def sign(self, msg):
        return self.decrypt(msg)


class PublicKey(object):
    def __init__(self, e, n):
        self.e = e
        self.n = n

    def encrypt(self, msg):
        # if hasattr(msg, "__len__"):
        #     cipher = []
        #     for char in msg:
        #         cipher.append(pow(ord(char), self.e, self.n))
        #     return cipher
        return pow(msg, self.e, self.n)

    def verify(self, sign):
        return self.encrypt(sign)
