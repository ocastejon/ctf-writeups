import hashlib

def crack_hash(type, value):
    '''Given a hash type and a hash value, it bruteforces it with all strings of length 3'''
    hash_function = get_hash_function(type)
    for i in range(32,127):
        for j in range(32,127):
            for k in range(32,127):
                s = "{}{}{}".format(chr(i), chr(j), chr(k))
                if hash_function(s).hexdigest() == value:
                    return s
    # We should never get here
    return None

def get_hash_function(type):
    '''Returns the corresponding hash function indicated by type'''
    if type == 'md5':
        return hashlib.md5
    if type == 'sha1':
        return hashlib.sha1
    if type == 'sha256':
        return hashlib.sha256
    return None

# We could use all the hashes found, but it would take longer. Instead we will use only 4 elements
# hashes = [
#     {'type': 'md5', 'value': 'cb2877f6063e950be80bdd9cf63cccad', 'positions': [7, 1, 4]},
#     {'type': 'sha1', 'value': '8ae43fbad3aa2e57f0ab4206a3710d8dee05b8ca', 'positions': [7, 5, 6]},
#     {'type': 'sha1', 'value': 'c7cab1a05e1e0c1d51a6a219d96577a16b7abf9d', 'positions': [2, 1, 2]},
#     {'type': 'sha1', 'value': 'f135388c435baf1644480f9dd1d9b53e2c9d23a0', 'positions': [9, 8, 6]},
#     {'type': 'sha1', 'value': '32815afa46f395cb82cf25512d4ca51964afb2e2', 'positions': [1, 9, 4]},
#     {'type': 'sha1', 'value': '8ba7b7562df3de9fa0641b2783e71d738eb44fe2', 'positions': [3, 5, 5]},
#     {'type': 'sha1', 'value': '17d656cc432054e57167d58a148d6aec9c80261c', 'positions': [0, 3, 6]},
#     {'type': 'sha256', 'value': 'afaedac802835591860b7e61e1486a8f7ce34cfb8bbf447e01783046da1b0a60', 'positions': [2, 3, 9]},
#     {'type': 'sha1', 'value': '64791691a6ec96929c9c99d98c9ea5623d3936ba', 'positions': [4, 0, 8]},
#     {'type': 'sha1', 'value': 'b803ea6cf07a51add8f1eca30e8df5c66eb7f70a', 'positions': [8, 7, 0]}
# ]

# Note that all positions from 0 to 9 are covered with only these 4 elements
hashes = [
    {'type': 'md5', 'value': 'cb2877f6063e950be80bdd9cf63cccad', 'positions': [7, 1, 4]},
    {'type': 'sha1', 'value': '8ae43fbad3aa2e57f0ab4206a3710d8dee05b8ca', 'positions': [7, 5, 6]},
    {'type': 'sha256', 'value': 'afaedac802835591860b7e61e1486a8f7ce34cfb8bbf447e01783046da1b0a60', 'positions': [2, 3, 9]},
    {'type': 'sha1', 'value': '64791691a6ec96929c9c99d98c9ea5623d3936ba', 'positions': [4, 0, 8]}
]

# We know flag has length 10
flag = [''] * 10

# Start cracking the hashes
for hash_data in hashes:
    s = crack_hash(hash_data['type'], hash_data['value'])
    for i, position in enumerate(hash_data['positions']):
        flag[position] = s[i]

# Print flag
print "Flag: {}".format("".join(flag))
