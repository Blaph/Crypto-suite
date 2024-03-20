import random
import copy

# Executes XOR between a bit of a certain key and a bit of a given (plain or cyphered) text
def _xor_letters(key, letter):
    # Convert letters into integers using ord()
    # Then, convert them in binary using 'bin()', and trim their prefix '0b' using [2:]
    # Finally, fill with 0 to the left until length of the string is 8 characters using 'zfill(8)'
    bin_letter1 = bin(key)[2:].zfill(8)
    bin_letter2 = bin(ord(letter))[2:].zfill(8)

    # bitwise XOR
    result = ''.join(str(int(bit1) ^ int(bit2)) for bit1, bit2 in zip(bin_letter1, bin_letter2))

    # Convert the binary in char using 'chr()'
    return chr(int(result, 2))


# Implementation of the Caesar Cypher
def caesar(plaintext: str, op_mode="enc"):
    '''
        It's a simple transposition cypher where each letter of the plaintext is trasposed with the letter in the 3 positions in the alphabet

        Parameters
        ----------
            plaintext (str): the plaintext you want to cypher
            op_mode (str): the operation mode of the cypher: 'enc' is for encryption; 'dec' is for decryption. Default is 'enc'

        Returns
        -------
            cyp (str): the ciphered/deciphered text
    '''

    plaintext = plaintext.lower()

    alphabet = "abcdefghijklmnopqrstuvwxyz"  # mod 26

    assert op_mode == "enc" or op_mode == "dec", "op_mode should be 'enc' for encryption or 'dec' for decryption"

    cyp = ""

    if op_mode == "enc":
        for ch in plaintext:
            i_cyp = (alphabet.index(ch) + 3) % 26

            cyp += alphabet[i_cyp]
    else:
        for ch in plaintext:
            i_cyp = (alphabet.index(ch) - 3) % 26

            cyp += alphabet[i_cyp]
        

    return cyp
    

# Implementation of the Blum Blum Shub algorithm
def bbs(p, q, s, l=20):
    '''
    Parameters
    ----------
        p (int): one of the two n factors. Toy example default value is 383
        q (int): the second of the two n factors. Toy example default value is 503
        s (int): the seed of the generator. Toy example default value is 101355
        l (int): length of the generated sequence. Default is 20
    
    Returns
    -------
        Bn (list): the generated sequence of bits
    '''

    # Initialize the sequence
    Bn = []

    # Generate n
    n = p * q
    print("p is ", p)
    print("q is ", q)
    print("n is ", n)

    # Generate first element of the sequence = x0
    xi = (s**2) % n
    print("X0 is ", xi)

    for i in range(l):
        xi = (xi**2) % n
        Bi = xi % 2
        Bn.append(Bi)
    
    return Bn


# Linear congruential generator
def linear_congruential_generator(X0: int, m = 2147483647, a = 16807, c = 0):
    '''
        Parameters
        ----------
            m (int): the modulus. Must be > 0. Default is 2.147.483.647
            a (int): the multiplier. Must be 0 < a < m. Default is 16807
            c (int): the increment. Must be 0 <= c < m. Default is 0
            X0 (int): the starting value, i.e.: the seed. Must be 0 <= X0 < m.

        Returns
        -------
            Xn (set): a sequence of generated numbers
    '''

    # Initialize the generator
    Xn = []
    Xi = X0

    # Keep repeating until a number is not already in the set
    while True:

        # Compute next number in the sequence
        Xi = (a * Xi + c) % m
        
        # If number is not in the set, add it
        if Xi not in Xn:
            Xn.append(Xi)
            print(Xi)

        # If number is already in the set, stop the generator and return the list    
        else:
            break

    return Xn


# Runs an instance of the RC4 cypher
import random
import copy

def rc4(stream, key_index=None):

    '''
        RC4 is a stream cypher widely used for its semplicity and efficiency. It uses a variable length key.

        Parameters
        ----------
            stream (str): the first stream of plaintext RC4 will cypher/decipher
            key_index (int): the key used for ciphering/deciphering the input stream. If none, a new key will be generated. Default is 'None'

        Returns
        -------
            op_stream (str): the corresponding ciphered/deciphered stream 
    '''

    MOD = 256

    # Initialization step
    S = []

    for i in range(MOD):
        S.append(i)

    T = copy.deepcopy(S)

    # Generate a new key
    if key_index is None:
        # Choose a random key K from vector state S
        key_index = random.randint(0, MOD)
    
    print("K is", key_index)

    for i in range(MOD):
        T[i] = S[i % key_index]

    # Swap elements according to T
    j = 0
    for i in range(MOD):
        j = (j + S[i] + T[i]) % MOD
        aux = S[i]
        S[i] = S[j]
        S[j] = aux

    # Stream generation
    # Swap elements according to S
    op_stream = []    

    for stream_bit in range(len(stream)):
        i = (stream_bit + 1) % MOD
        j = (j + S[i]) % MOD

        aux = S[i]
        S[i] = S[j]
        S[j] = aux

        t = (S[i] + S[j]) % MOD
        k = S[t]

        x_cyph = _xor_letters(k, stream[stream_bit])

        op_stream.append(x_cyph)

    message = str()

    for x in op_stream:
        message += x

    return message, key_index