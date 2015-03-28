from Crypto.Cipher import AES


class Cipher():
    def __init__(self, alg, key, iv, op):
        assert alg == 'aes_256_cbc' and op == 0
        self._iv=iv
        self._key=key

    def unpad(self, s):
        return s[0:-ord(s[-1])]

    def update(self, ciphertext):
        cipher = AES.new(self._key, AES.MODE_CBC, self._iv)
        return self.unpad(cipher.decrypt(ciphertext))

    def final(self):
        return ''

