# -*- coding: utf-8 -*-
import numpy as np
import numpy.random as r
import op

class SCO:
"""
a Simple Constant Obfuscator

"""

    def __init__(self, n_bit):
        self.first_start = True
        self.bit = n_bit


    def decode(self, k, verbose=False):
        """
        Decodes and returns the obfuscated constant

        """

        operator = op.Operator(self.bit)

        zero = k["zero"]
        one = k["one"]
        set_ones = operator.binary(k["set1"])
        set_zeros = operator.binary(k["set0"])

        binRandom = r.randint(2, size=self.bit)
        binConstant = operator.binary(0)

        for i in range(self.bit):
            if (binRandom[i] == 0):
                z_i = zero[i]
                xor = operator.binary(z_i)
            else:
                o_i = one[i]
                xor = operator.binary(o_i)

            if (verbose):
                print binConstant, xor, "\n"

            # applying xor to the bits of the constant to be decoded
            for b in range(self.bit):
                binConstant[b] = operator.lxor([binConstant[b], xor[b]])

        if (verbose):
            print binConstant, "\n\n"

        for i in range(self.bit):
            binConstant[i] = binConstant[i] or set_ones[i]

        if (verbose):
            print binConstant, "\n"

        for i in range(self.bit):
            binConstant[i] = binConstant[i] and set_zeros[i]

        if (verbose):
            print binConstant, "\n"


        return operator.decimal(binConstant)

    def encode(self, const):
        """
        Obfuscates the "const" integer by dividing bit indexes in two groups (I and II);
        it obscures the constant and returns a dictionary containing:
            "zero" : the zero[] list as seen in decode()
            "one"  : the one[] list as seen in decode()
            "set0" : the value which defines the bits of group II which need to be set to 0
            "set1" : the value which defines the bits of group II which need to be set to 1

        """
        operator = op.Operator(self.bit)
        indexes = range(self.bit)
        r.shuffle(indexes)

        # dividing "indexes" in 2 groups:
        positive_offset = r.randint(self.bit / 8)
        negative_offset = r.randint(self.bit / 8)

        m = self.bit / 2 + positive_offset - negative_offset
        m = min(self.bit, max(0, m))        # check that m is not out of bound
        I = indexes[:m]
        II = indexes[m:]

        bconst = operator.binary(const)

        zero = []
        one = []

        for i in range(self.bit):
            #initialize zero and one to random values
            z_i = r.randint(2 ** self.bit, dtype=np.int64)
            z_i = operator.binary(z_i)
            zero.insert(i, z_i)
            o_i = r.randint(2 ** self.bit, dtype=np.int64)
            o_i = operator.binary(o_i)
            one.insert(i, o_i)

        for b in I:
            # consider the b-th bit of every element in z:
            sequence = []
            for k in range(self.bit):
                sequence.append(zero[k][b])

            # the 'xor' of all those bits must be equal to bconst[b];
            # the following code calculates the 'xor' of all elements
            #  in sequence except the last one:
            all_except_one = operator.lxor(sequence[:len(sequence) - 1])
            # ...then adjust the last bit accordingly:
            if bconst[b] == 0:
                zero[self.bit - 1][b] = all_except_one
            else:
                zero[self.bit - 1][b] = int( not all_except_one )

        # copy values of bits which are in group I from zero to one:
        for i in range(self.bit):
            for b in I:
                one[i][b] = zero[i][b]

        # turn zero and one back to decimal
        for i in range(self.bit):

            zero[i] = operator.decimal(zero[i])
            one[i] = operator.decimal(one[i])

        # now fixing 0s and 1s of group II
        set0 = []
        set1 = []

        for i in range(self.bit):
            set0.append(1)
            set1.append(0)

        for b in II:
            if bconst[b] == 0:
                set0[b] = 0
            if bconst[b] == 1:
                set1[b] = 1

        set0 = operator.decimal(set0)
        set1 = operator.decimal(set1)

        return {"zero": zero, "one": one, "set0":set0, "set1":set1}

    def GetObfuscatedCode(self, const_name, const_value, indentation=0, headers=False, comment=""):
        """
        Returns a string containing the offuscated code to write
        'const_name = const_value' as an opaque constant.

        """

        operator = op.Operator(self.bit)

        def indent(times=0):
            tabs = ""
            for i in range(indentation + times):
                tabs += "\t"
            return tabs

        if comment != "":
            comment = "# " + comment + "\n"
        else:
            comment = "\n"

        if self.first_start or headers:
            # added only on first code generated, or when requested with "headers=True"
            imports = "from SimpleConstantObfuscator import operator\n" + indent() + "import numpy\n" + indent() + "import numpy.random\n"
            header = imports
        else:
            header = ""

        self.first_start = False

        k = self.encode(const_value)

        zero_str = "zero = " + str(k["zero"]) + "\n"
        one_str = "one = " + str(k["one"]) + "\n"
        set1_str = "set_ones = " + str(operator.binary(k["set1"])) + "\n"
        set0_str = "set_zeros = " + str(operator.binary(k["set0"])) + "\n"
        init_str = "operator = operator.Operator(" + str(self.bit) + ")\n" + indent() + "binRandom = numpy.random.randint(2, size=" + str(self.bit) + ")\n" + indent() + const_name + " = operator.binary(0)\n"

        init_block = zero_str + indent() + one_str + indent() + set1_str + indent() + set0_str + indent() + indent() + comment + init_str


        for_clause = "for i in range("+ str(self.bit) + "):\n"
        if_0 = "if (binRandom[i] == 0):\n" + indent(times=2) + "z_i = zero[i]\n" + indent(times=2) + "xor = operator.binary(z_i)\n"
        if_1 = "else:\n" + indent(times=2) + "o_i = one[i]\n" + indent(times=2) + "xor = operator.binary(o_i)\n"
        xor_str = "for b in range(" + str(self.bit) + "):\n" + indent(times=2) + const_name + "[b] =operator.lxor([" + const_name + "[b], xor[b]])\n"

        for_block = for_clause + indent(times=1) + if_0 + indent(times=1) + if_1 + indent(times=1) + xor_str + "\n"


        or_str = "for i in range(" + str(self.bit) + "):\n" + indent(times=1) + const_name + "[i] = " + const_name + "[i] or set_ones[i]\n"
        and_str = "for i in range(" + str(self.bit) + "):\n" + indent(times=1) + const_name + "[i] = " + const_name + "[i] and set_zeros[i]\n"

        end_block = or_str + indent() + and_str + indent() + const_name + "= operator.decimal(" + const_name + ")\n"


        full_code = indent() + header + indent() + init_block + indent() + for_block + indent() + end_block

        return full_code
