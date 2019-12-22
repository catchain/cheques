from __future__ import print_function
import random
import hashlib

def toHex(dec):
    x = (dec % 16)
    digits = "0123456789ABCDEF"
    rest = dec / 16
    if (rest == 0):
        return digits[x]
    return toHex(rest) + digits[x]

octetsCount = int(256 / 8)
octets = [random.randint(0, 255) for i in range(octetsCount)]

print("0x" + "".join(["{0:0{1}x}".format(oct, 2) for oct in octets]))
