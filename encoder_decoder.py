# This is the most efficient (in terms of chars per digit) encoder and decoder you can find on scratch.
# There is simply no better way of encoding / decoding both theoretically nor practically.
# Instead of doing substitution encoding (like what most people do) this script teats characters as numbers in their own base.
# So in the end you convert base-n to base-10 and vice versa.

# Note encoding is computationally expensive for larger strings, which is why it's best to use the encoder on the server side, and the decoder on the client side (faster)

# Here is the client version of this script: https://scratch.mit.edu/projects/1202684524/

# If you decide to use this, please feel free to do so with credit.

def decode(n, codec="0123456789 etaoinshrdlcumwfgypbvkjxqz,.;:\"'!?&*-=_+@~#|/\\<>(){}[]�"):
    base = len(codec)
    if n == 0: return codec[0]
    s = ''
    while n > 0:
        n, r = divmod(n - 1, base)
        s = codec[r] + s
    return s

def encode(s, codec="0123456789 etaoinshrdlcumwfgypbvkjxqz,.;:\"'!?&*-=_+@~#|/\\<>(){}[]�"):
    base = len(codec)
    val = 0
    for c in s.lower():
        val = val * base + (codec.index(c) + 1)
    return val
