from math import ceil
import random

def first_key():
    key = list()
    for i in range(16):
        character = random.randint(0,255)
        key.append(character)
    return key

def shift_left(n):
    bits = 25
    total_bit = 128
    return ((n << bits) % (1 << total_bit)) | (n >> (total_bit - bits))

def break_key(key):
    key_list = list()
    prev_key = 0
    for i in range(16):
        prev_key = (key - prev_key) % (256**(i+1))
        character = ceil(prev_key / (256**(i)))
        key_list.append(character)
        prev_key += prev_key
    key_list.reverse()
    return key_list
    
def key_decimal_value(key):
    value = 0
    for i in range(16):
        value += (key[i] * (256**(15-i)))
    return value


def create_key():
    keys = list()
    key_value = 0
    for i in range(9):
        if i == 0:
            key = first_key()
            key_value = key_decimal_value(key)
        else:
            shift_key = shift_left(key_value)
            key = break_key(shift_key)
            key_value = key_decimal_value(key)
        keys.append(key)
    encryption_key = keys.copy()
    keys.reverse()
    return {'encrypt': encryption_key, 'decrypt': keys}
    