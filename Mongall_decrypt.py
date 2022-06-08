#!/usr/bin/env python3
import codecs
import base64
import argparse

MOD = 256

def KSA(key):
    key_length = len(key)
    S = list(range(MOD))  # [0,1,2, ... , 255]
    j = 0
    for i in range(MOD):
        j = (j + S[i] + key[i % key_length]) % MOD
        S[i], S[j] = S[j], S[i]  # swap values

    return S


def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % MOD
        j = (j + S[i]) % MOD

        S[i], S[j] = S[j], S[i]  # swap values
        K = S[(S[i] + S[j]) % MOD]
        yield K


def get_keystream(key):
    S = KSA(key)
    return PRGA(S)

def decrypt(ciphertext, key):
    ciphertext = codecs.decode(ciphertext, 'hex_codec')
    res = encrypt_logic(key, ciphertext)
    return codecs.decode(res, 'hex_codec').decode('utf-8')    

def encrypt_logic(key, text):
    # For plaintext key, use this
    key = [ord(c) for c in key]
    # If key is in hex:
    # key = codecs.decode(key, 'hex_codec')
    # key = [c for c in key]
    keystream = get_keystream(key)

    res = []
    for c in text:
        val = ("%02X" % (c ^ next(keystream)))  # XOR and taking hex
        res.append(val)
    return ''.join(res)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(usage='%(prog)s -s strings -t type')
    parser.add_argument('--strings', '-s', dest='strin', help='strings to nuke')
    parser.add_argument('--types', '-t', dest='typein', help='strings to nuke')
    args = parser.parse_args()
    arg_1 = args.strin
    arg_2 = args.typein
    key = 'C++RuntimeLibrary'
    chipertext_1 = arg_1[1::2]

    if arg_2 == '1':
        print(decrypt(chipertext_1, key))
    elif arg_2 == '2':
        print(base64.b64decode(chipertext_1))
    elif arg_2 == '3':
        print(base64.b64decode(arg_1))