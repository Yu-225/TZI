from modules.MD5 import MD5 as my_md5
from math import ceil

w = 64  # bits
r = 8   # rounds
b = 32  # bytes (8, 16, 32)


class RC5:
    def __init__(self, w, r, b, key_phrase):
        self.w = w
        self.r = r
        self.b = b
        self.key_phrase = key_phrase

        self.nulbits = 0

        self.w4 = self.w // 4
        self.u = self.w // 8  # кількість байтів у слові
        self.c = ceil(max(self.b, 1) / self.u)  # довжина К в словах
        self.t = 2 * (r + 1)
        self.mod = (2 ** self.w)
        self.mask = self.mod - 1

        self.L = [0] * self.c
        self.S = [0] * self.t

        self.K = None
        self.create_sub_keys()

    def _rotate_left(self, val, n):
        n %= self.w
        return ((val << n) & self.mask) | ((val & self.mask) >> (self.w - n))

    def _rotate_right(self, val, n):
        n %= self.w
        return ((val & self.mask) >> n) | (val << (self.w - n) & self.mask)

    def _key_hash(self):
        md5 = my_md5()

        if b == 8:
            md5.update(self.key_phrase)
            key_phrase_hash = md5.digest()
            self.K = key_phrase_hash[8:]

        elif b == 16:
            md5.update(self.key_phrase)
            self.K = md5.digest()

        elif b == 32:
            md5.update(self.key_phrase)
            key_phrase_1 = md5.digest()
            md5.update(key_phrase_1)
            key_phrase_2 = md5.digest()
            self.K = key_phrase_2 + key_phrase_1

    def _L(self):
        for i in range(self.b - 1, -1, -1):
            self.L[(self.b - 1 - i) // self.u] = (self.L[(self.b - 1 - i) // self.u] << 8) + self.K[i]
        print(self.L)

    def _S(self):

        if self.w == 16:
            Pw, Qw = 0xB7E1, 0x9E37
        elif self.w == 32:
            Pw, Qw = 0xB7E15163, 0x9E3779B9
        elif self.w == 64:
            Pw, Qw = 0xB7E151628AED2A6B, 0x9E3779B97F4A7C15

        self.S[0] = Pw
        for i in range(1, self.t):
            # S[i] = S[i - 1] + Qw
            self.S[i] = (self.S[i - 1] + Qw) & ((1 << self.w) - 1)
        print(self.S)

    def _shufle(self):
        i, j, A, B = 0, 0, 0, 0
        for k in range(3 * max(self.c, self.t)):
            A = self.S[i] = self._rotate_left((self.S[i] + A + B), 3)
            B = self.L[j] = self._rotate_left((self.L[j] + A + B), A + B)
            i = (i + 1) % self.t
            j = (j + 1) % self.c
        print(self.S)

    def create_sub_keys(self):
        self._key_hash()
        self._L()
        self._S()
        self._shufle()

    def encrypt_block(self, data):
        A = int.from_bytes(data[:self.u], byteorder='little')
        B = int.from_bytes(data[self.u:], byteorder='little')

        A = (A + self.S[0]) % self.mod
        B = (B + self.S[1]) % self.mod

        for i in range(1, self.r + 1):
            A = (self._rotate_left((A ^ B), B) + self.S[2 * i]) % self.mod
            B = (self._rotate_left((A ^ B), A) + self.S[2 * i + 1]) % self.mod

        print(A)
        print(B)
        print(A.to_bytes(self.u, byteorder='little') + B.to_bytes(self.u, byteorder='little'))

        return A.to_bytes(self.u, byteorder='little') + B.to_bytes(self.u, byteorder='little')

    def decrypt_block(self, data):
        A = int.from_bytes(data[:self.u], byteorder='little')
        B = int.from_bytes(data[self.u:], byteorder='little')

        for i in range(self.r, 0, -1):
            B = self._rotate_right(B - self.S[2 * i + 1], A) ^ A
            A = self._rotate_right(A - self.S[2 * i], B) ^ B

        B = (B - self.S[1]) % self.mod
        A = (A - self.S[0]) % self.mod

        return A.to_bytes(self.u, byteorder='little') + B.to_bytes(self.u, byteorder='little')

    def encrypt_bytes(self, data):
        res, run = b'', True
        while run:
            temp = data[:self.w4]
            if len(temp) != self.w4:
                data = data.ljust(self.w4, b'\x00')
                run = False
            res += self.encrypt_block(temp)
            data = data[self.w4:]
            if not data:
                break
        return res

    def decrypt_bytes(self, data):
        res, run = b'', True
        while run:
            temp = data[:self.w4]
            if len(temp) != self.w4:
                run = False
            res += self.decrypt_block(temp)
            data = data[self.w4:]
            if not data:
                break
        return res.rstrip(b'\x00')

    def encrypt_file(self, inpFileName, outFileName):
        with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
            run = True
            while run:
                text = inp.read(self.w4)
                if not text:
                    break

                if len(text) != self.w4:
                    print('len', len(text))
                    while len(text) != self.w4:
                        text += b'\x00'
                        self.nulbits += 1
                    run = False

                text = self.encrypt_block(text)
                out.write(text)

            print(self.nulbits)

    def decrypt_file(self, inpFileName, outFileName):
        with open(inpFileName, 'rb') as inp, open(outFileName, 'wb') as out:
            while True:
                text = inp.read(self.w4)
                if not text:
                    break
                text = self.decrypt_block(text)
                out.write(text)


# rc5 = RC5(64, 8, 32, b'qwertyuiop1234567890   qwertyu12')
#
# pt = b'hello world'
# et = rc5.encryptBytes(pt)
# print('pt -', pt, ' >> rc5 >>  et -', et)
# dt = rc5.decryptBytes(et)
# print('et -', et, ' >> rc5 >>  dt -', dt)

# D:\LABS\Labs 3.1\Технології захисту інформації\main\congig.ini
# file_path = r'C:\Users\YuLap\OneDrive\Робочий стіл\4c250818f831b6fc62b59896b7739a1a.jpg'
# enc_path = r'C:\Users\YuLap\OneDrive\Робочий стіл\out_enc.jpg'
# dec_path = r'C:\Users\YuLap\OneDrive\Робочий стіл\out_dec.jpg'
#
#
# rc5.encryptFile(file_path, enc_path)
# rc5.decryptFile(enc_path, dec_path)



