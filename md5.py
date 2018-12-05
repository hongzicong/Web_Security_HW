# -*- coding: utf-8 -*-
import math

# IV
A = '0x67452301'
B = '0xefcdab89'
C = '0x98badcfe'
D = '0x10325476'

# generate function
F = lambda x, y, z: ((x & y) | ((~x) & z))
G = lambda x, y, z: ((x & z) | (y & (~z)))
H = lambda x, y, z: (x ^ y ^ z)
I = lambda x, y, z: (y ^ (x | (~z)))

# used to rotate left shift
RLS = lambda x, n: (((x << n) | (x >> (32 - n))) & 0xffffffff)

s_1 = (7, 12, 17, 22) * 4
s_2 = (5, 9, 14, 20) * 4
s_3 = (4, 11, 16, 23) * 4
s_4 = (6, 10, 15, 21) * 4

m_1 = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
m_2 = (1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12)
m_3 = (5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2)
m_4 = (0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9)


def T(i):
    return (int((1 << 32) * abs(math.sin(i)))) & 0xffffffff


def hex_str2arr(data_str):
    result = []
    for i in range(0, len(data_str), 2):
        result.append(data_str[i: i + 2])
    return result


def reverse_hex_str(data_str):
    # abort '0x'
    result = hex_str2arr(data_str)[1:]
    result.reverse()
    result = '0x' + ''.join(result)
    return result


def generateX(order, Y):
    # each X is 4 chars
    X = [0] * 16
    for i in range(16):
        X[i] = '0x' + ''.join((Y[4 * order[i]] + Y[4 * order[i] + 1] + Y[4 * order[i] + 2]
                               + Y[4 * order[i] + 3]).split('0x'))
    for i in range(16):
        X[i] = reverse_hex_str(X[i])
    return X


def fun(a, b, c, d, f, X, s):
    global T_i
    for i in range(16):
        a = (int(a, 16) + f(int(b, 16), int(c, 16), int(d, 16)) + int(X[i], 16) + T(T_i)) & 0xffffffff
        a = RLS(a, s[i])
        a = hex((int(b, 16) + a) & 0xffffffff)
        a, b, c, d = d, a, b, c
        T_i += 1
    return a, b, c, d


# CV is a array including 4 hex strings
# Y is a array including 64 chars (512 bits)
def H_MD5(CV, Y):

    a, b, c, d = CV

    X_1 = generateX(m_1, Y)
    X_2 = generateX(m_2, Y)
    X_3 = generateX(m_3, Y)
    X_4 = generateX(m_4, Y)

    # four loops
    aa, bb, cc, dd = fun(a, b, c, d, F, X_1, s_1)
    aa, bb, cc, dd = fun(aa, bb, cc, dd, G, X_2, s_2)
    aa, bb, cc, dd = fun(aa, bb, cc, dd, H, X_3, s_3)
    aa, bb, cc, dd = fun(aa, bb, cc, dd, I, X_4, s_4)

    output_a = hex((int(a, 16) + int(aa, 16)) & 0xffffffff)
    output_b = hex((int(b, 16) + int(bb, 16)) & 0xffffffff)
    output_c = hex((int(c, 16) + int(cc, 16)) & 0xffffffff)
    output_d = hex((int(d, 16) + int(dd, 16)) & 0xffffffff)

    return output_a, output_b, output_c, output_d


def show_result(data_list):
    result = ''
    for data_str in data_list:
        result += reverse_hex_str(data_str)[2:]
    return result


if __name__ == "__main__":
    while True:
        data = input("Input string <<< ")

        data = list(map(hex, map(ord, data)))
        # every char is 8 bits
        K = len(data) * 8
        print("length of input (bits): %d" % K)

        # padding
        padding_data = data[:]
        padding_data.append('0x80')
        while (len(padding_data) * 8 + 64) % 512 != 0:
            padding_data.append('0x00')

        # make hex value of K greater than or equal to 64 bits('0' is 4 bits in hex)
        K_hex_str = hex(K)[2:].rjust(16, '0')
        # make hex value of K be 64 bits and add '0x'
        K_hex_str = '0x' + K_hex_str[-64:]
        # reverse it and then abort '0x'
        K_hex_str = reverse_hex_str(K_hex_str)[2:]
        K_hex_arr = []
        for i in range(0, len(K_hex_str), 2):
            K_hex_arr.append('0x' + K_hex_str[i:i + 2])
        padding_data.extend(K_hex_arr)

        # little endian
        IV = [A, B, C, D]
        T_i = 1
        CV = IV
        # take every 512 bits
        for i in range(0, len(padding_data) // 64):
            T_i = 1
            CV = H_MD5(CV, padding_data[64 * i: 64 * (i + 1)])
            print("md5 >>> " + show_result(CV))
