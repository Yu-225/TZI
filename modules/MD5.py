import binascii
import struct
from enum import Enum
from math import (
    floor,
    sin,
)

from bitarray import bitarray
from bitarray.util import bits2bytes


class MD5Buffer(Enum):
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476


class MD5:
    def __init__(self):
        self._string = b''
        self._buffers = {
            MD5Buffer.A: MD5Buffer.A.value,
            MD5Buffer.B: MD5Buffer.B.value,
            MD5Buffer.C: MD5Buffer.C.value,
            MD5Buffer.D: MD5Buffer.D.value,
        }

    def hash(self, string):
        if isinstance(string, str):
            self._string = string.encode('utf-8')

        preprocessed_bit_array = self._step_2(self._step_1())
        self._step_3()
        self._step_4(preprocessed_bit_array)
        return self._step_5()

    def update(self, chunk):
        if isinstance(chunk, str):
            chunk = chunk.encode('utf-8')

        # Ensure that self._string is in bytes format
        if isinstance(self._string, str):
            self._string = self._string.encode('utf-8')

        # Append the new chunk directly to the existing bytes
        self._string += chunk

        # Calculate the hash based on the updated string
        return self.hash(self._string)

    def hexdigest(self):
        return self._step_5()

    def digest(self):
        # Convert the buffers to little-endian bytes
        A = struct.pack("<I", self._buffers[MD5Buffer.A])
        B = struct.pack("<I", self._buffers[MD5Buffer.B])
        C = struct.pack("<I", self._buffers[MD5Buffer.C])
        D = struct.pack("<I", self._buffers[MD5Buffer.D])

        # Concatenate the bytes to form the digest
        digest_bytes = A + B + C + D

        return digest_bytes

    def _step_1(self):
        bit_array = bitarray(endian="big")
        bit_array.frombytes(self._string)

        # Pad the string with a 1 bit and as many 0 bits required such that
        # the length of the bit array becomes congruent to 448 modulo 512.
        # Note that padding is always performed, even if the string's bit
        # length is already conguent to 448 modulo 512, which leads to a
        # new 512-bit message block.
        bit_array.append(1)
        while len(bit_array) % 512 != 448:
            bit_array.append(0)

        # For the remainder of the MD5 algorithm, all values are in
        # little endian, so transform the bit array to little endian.
        b = bitarray(bit_array, 'little')
        b.bytereverse()
        if len(bit_array) % 8:
            # copy last few bits directly
            p = 8 * (bits2bytes(len(bit_array)) - 1)
            b[p:] = bit_array[p:]
        return b

    def _step_2(self, step_1_result):
        # Extend the result from step 1 with a 64-bit little endian
        # representation of the original message length (modulo 2^64).
        length = (len(self._string) * 8) % pow(2, 64)
        length_bit_array = bitarray(endian="little")
        length_bit_array.frombytes(struct.pack("<Q", length))

        result = step_1_result.copy()
        result.extend(length_bit_array)
        return result

    def _step_3(self):
        # Initialize the buffers to their default values.
        for buffer_type in self._buffers.keys():
            self._buffers[buffer_type] = buffer_type.value

    def _step_4(self, step_2_result):
        # Define the four auxiliary functions that produce one 32-bit word.
        F = lambda x, y, z: (x & y) | (~x & z)
        G = lambda x, y, z: (x & z) | (y & ~z)
        H = lambda x, y, z: x ^ y ^ z
        I = lambda x, y, z: y ^ (x | ~z)

        # Define the left rotation function, which rotates `x` left `n` bits.
        rotate_left = lambda x, n: (x << n) | (x >> (32 - n))

        # Define a function for modular addition.
        modular_add = lambda a, b: (a + b) % pow(2, 32)

        # Compute the T table from the sine function. Note that the
        # RFC starts at index 1, but we start at index 0.
        T = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]

        # The total number of 32-bit words to process, N, is always a
        # multiple of 16.
        N = len(step_2_result) // 32

        # Process chunks of 512 bits.
        for chunk_index in range(N // 16):
            # Break the chunk into 16 words of 32 bits in list X.
            start = chunk_index * 512
            X = [step_2_result[start + (x * 32): start + (x * 32) + 32] for x in range(16)]

            # Convert the `bitarray` objects to integers.
            X = [int.from_bytes(word.tobytes(), byteorder="little") for word in X]

            # Make shorthands for the buffers A, B, C and D.
            A = self._buffers[MD5Buffer.A]
            B = self._buffers[MD5Buffer.B]
            C = self._buffers[MD5Buffer.C]
            D = self._buffers[MD5Buffer.D]

            # Execute the four rounds with 16 operations each.
            for i in range(4 * 16):
                if 0 <= i <= 15:
                    k = i
                    s = [7, 12, 17, 22]
                    temp = F(B, C, D)
                elif 16 <= i <= 31:
                    k = ((5 * i) + 1) % 16
                    s = [5, 9, 14, 20]
                    temp = G(B, C, D)
                elif 32 <= i <= 47:
                    k = ((3 * i) + 5) % 16
                    s = [4, 11, 16, 23]
                    temp = H(B, C, D)
                elif 48 <= i <= 63:
                    k = (7 * i) % 16
                    s = [6, 10, 15, 21]
                    temp = I(B, C, D)

                # The MD5 algorithm uses modular addition. Note that we need a
                # temporary variable here. If we would put the result in `A`, then
                # the expression `A = D` below would overwrite it. We also cannot
                # move `A = D` lower because the original `D` would already have
                # been overwritten by the `D = C` expression.
                temp = modular_add(temp, X[k])
                temp = modular_add(temp, T[i])
                temp = modular_add(temp, A)
                temp = rotate_left(temp, s[i % 4])
                temp = modular_add(temp, B)

                # Swap the registers for the next operation.
                A = D
                D = C
                C = B
                B = temp

            # Update the buffers with the results from this chunk.
            self._buffers[MD5Buffer.A] = modular_add(self._buffers[MD5Buffer.A], A)
            self._buffers[MD5Buffer.B] = modular_add(self._buffers[MD5Buffer.B], B)
            self._buffers[MD5Buffer.C] = modular_add(self._buffers[MD5Buffer.C], C)
            self._buffers[MD5Buffer.D] = modular_add(self._buffers[MD5Buffer.D], D)

    def _step_5(self):
        # Convert the buffers to little-endian.
        A = struct.unpack("<I", struct.pack(">I", self._buffers[MD5Buffer.A]))[0]
        B = struct.unpack("<I", struct.pack(">I", self._buffers[MD5Buffer.B]))[0]
        C = struct.unpack("<I", struct.pack(">I", self._buffers[MD5Buffer.C]))[0]
        D = struct.unpack("<I", struct.pack(">I", self._buffers[MD5Buffer.D]))[0]

        self._string = self.digest()

        # Output the buffers in upper-case hexadecimal format.
        return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}".upper()



