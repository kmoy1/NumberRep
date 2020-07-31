import math

def u_reps(n):
    """Given integer N, print all UNSIGNED representations in decimal, binary, hex.
    Binary numbers are prefixed with "0b" and hex numbers are prefixed with "0x".
    >>> u_reps(0b11110001)
    DEC: 241
    BIN: 0b11110001
    HEX: 0xf1
    >>> u_reps(100)
    DEC: 100
    BIN: 0b01100100
    HEX: 0x64
    >>> u_reps(0x2A1)
    DEC: 673
    BIN: 0b001010100001
    HEX: 0x2A1
    """
    assert n >= 0 and type(n) is int, "only unsigned (nonnegative) integer arguments."
    print("DEC:", n)
    b = padded_dtob(n)
    x = "0x" + format(n, 'X')
    print("BIN:", b)#dec -> bin
    print("HEX:", x)#dec -> hex

def tc_reps(n_str, max_digits=8):
    """Given N as a decimal integer OR in string binary/hex format, print all TWO's COMPLEMENT representations 
    in decimal, binary, hex. Binary numbers are prefixed with "0b" and hex numbers 
    are prefixed with "0x".
    that the LEADING BIT IS A 1- i.e. we only care about TC reps of negative numbers 
    (positive is the same as unsigned, with just a 0 MSB).
    >>> tc_reps("0b11111101")
    DEC: -3
    BIN: 0b11111101
    HEX: 0xFD
    >>> tc_reps(-13)
    DEC: -13
    BIN: 0b11110011
    HEX: 0xF3
    >>> tc_reps("0xC2")
    DEC: -62
    BIN: 0b11000010
    HEX: 0xC2
    """
    #Assume N is a binary value here. 
    if type(n_str) is str:
        header, num = n_str[:2], n_str[2:]
        sign_bit = num[0]
        negated = "" #negated bit string.
        if header == '0b': #Handle binary
            while len(num) % 4 != 0: #Sign extension.
                num = sign_bit + num  
            for bit in num:
                neg_bit = str(int(not int(bit)))
                negated = negated + neg_bit
            negated = bin(int(negated,2) + 1)
            if sign_bit == '1':
                d = -1 * int(negated, base=2) #negative number.
            else:
                d = int(num, base=2)#positive number.
            h = "0x" + ("%X" % int(num,2))
            b = "0b" + num
            #TODO: Handle overflow.
        elif header == '0x': #Handle hex
            conv = bin(int(num, 16))[2:]
            sign_bit = conv[0]
            for bit in conv:
                negated = negated + str(int(not int(bit)))
            negated = bin(int(negated,2) + 1) 
            if sign_bit == '1':
                d = -1 * int(negated, base=2) #negative number.
            else:
                d = int(num, base=2)#positive number.
            h = "0x" + num
            b = "0b" + conv
        print("DEC:", d)
        print("BIN:", b)
        print("HEX:", h)
    else: #Integer
        b = format(n_str, 'b')
        if b[0] == '-':
            b = b[1:]
        if n_str < 0:
            negated = ""
            for bit in b:
                neg_bit = str(int(not int(bit)))
                negated = negated + neg_bit
            while len(b) % 4 != 0:
                b = "1" + b
        else:
            while len(b) % 4 != 0:
                b = "0" + b       
        h = "0x" + ("%X" % int(b,2))
        b = "0b" + b
        d = n_str
        print("DEC:", d)
        print("BIN:", b)
        print("HEX:", h)

def sam_reps(n):
    """Given integer N, print sall SIGN & MAGNITUDE representations in decimal, binary, hex.
    Binary numbers are prefixed with "0b" and hex numbers are prefixed with "0x".
    >>> sam_reps("0b00110101")
    DEC: 53
    BIN: 0b00110101
    HEX: 0x35
    Sign: +
    Magnitude: 53 (0110101)
    >>> sam_reps("0b11101101")
    DEC: -109
    BIN: 0b11101101
    HEX: 0xED
    Sign: -
    Magnitude: 109 (1101101)
    >>> sam_reps(-3)
    DEC: -3
    BIN: 0b1011
    HEX: 0xB
    Sign: -
    Magnitude: 3 (011)
    """
    pm = ""
    if type(n) is str:
        #Implement "0bXXXX" logic
        header, digits = n[:2], n[2:]
        if header == "0b":
            sign_bit, mag = digits[0], digits[1:] #Binary string (unsigned rn)
            if sign_bit == '0':
                d = int(mag, base=2)
                sign = "+"
            else:
                d = -1 * int(mag, base=2)
                sign = "-"
            b = "0b" + digits
            h = "0x" + format(int(digits,base=2), 'X')
        elif header == "0x":
            bs = bin(int(digits,base=16))[2:] #hex -> bitstring
            sign_bit, mag = bs[0], bs[1:]
            if sign_bit == '0':
                d = int(mag, base=2)
                sign = "+"
            else:
                d = -1 * int(mag, base=2)
                sign = "-"
            b = "0b" + digits
            h = "0x" + format(int(n,base=2),'X')
            #convert hex -> bin.
        pm = mag
    else: #Implement decimal logic.
        if n < 0:
            mag = bin(n)[3:]
            padded_mag = mag
            while len(padded_mag) % 3 != 0:
                padded_mag = '0' + padded_mag
            b = "0b1" + padded_mag
            sign = "-"
        else:
            mag = bin(n)[2:]
            padded_mag = mag
            while len(padded_mag) % 3 != 0:
                padded_mag = '0' + padded_mag
            b = "0b0" + padded_mag
            sign = "+"
        pm = padded_mag
        h = "0x" + format(int(b,2), 'X')
        d = n
    print("DEC:", d)
    print("BIN:", b)
    print("HEX:", h)
    print("Sign:", sign)
    print("Magnitude:", str(int(mag,2)) + " (" + str(pm) + ")" )

def bias_reps(n, bias=0):
    """Given unsigned integer N and bias B (default 0, or unsigned) print all SIGN & MAGNITUDE representations 
    in decimal, binary, hex. We subtract BIAS from N.
    Binary numbers are prefixed with "0b" and hex numbers are prefixed with "0x".
    >>> bias_reps(10, 5)
    DEC: 5
    BIN: 0b1010

    """
    if type(n) is str:
        #Implement "0bXXXX" logic
        b = bin(n)[2:] #Binary string (unsigned rn)
        sign_bit = b[0]
        print("DEC:", d)
        print("BIN:", b)
        print("HEX:", h)
    else: #Implement decimal logic.
        d = n-bias
        b = bin(n)
        h = "0x" + ("%X" % int(b,2))

def opt_bias(upper):
    """Returns optimal bias for [0, UPPER], s.t. we
    represent an equal number of positive and negative numbers."""
    return None


#####HELPER FUNCS#####

def twos_comp(val, bits):
    """Convert decimal to 2's complement"""
    if (val & (1 << (bits - 1))) != 0: 
        val = val - (1 << bits)
    return val

def btod(s):
    """Helper func that converts binary string S to unsigned decimal.
    >>> btod("0b11010")
    26
    >>> btod("10101")
    21  
    """
    if s[0:2] == "0b":
        s = s[2:]    
    return int(s, 2)


def padded_dtob(x):
    """Given integer x, return a binary string padded so bit width is
    a multiple of 4."""
    padded_bw = roundup(len(bin(x)) - 2)
    true_bw = len(bin(x))-2
    dtob = bin(x)[2:]
    while len(dtob) < padded_bw:
        dtob = '0' + dtob
    dtob = '0b' + dtob
    return dtob

def roundup(x, base=4):
    """Helper func that rounds X UP to nearest multiple
    of 4."""
    return base * math.ceil(x/base)

def test_func(f):
    """Run f's doctests."""
    import doctest
    doctest.run_docstring_examples(f, globals())

test_func(tc_reps)