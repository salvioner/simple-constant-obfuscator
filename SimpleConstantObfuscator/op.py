class Operator:

    def __init__(self, n_bit):
        self.bit = n_bit

    def binary(self, x):
        """
        Turns a base-10 number 'x' into a list of bits

        """
        error = "Overflow - please insert a number between 0 and " + str(2**self.bit - 1) + " or raise the number of bits of the SCO."
        bx = bin(x)
        bx = bx[2:]

        if len(bx) > self.bit:
            raise ValueError(error)
            return []
        else:

            n = []

            for i in range(len(bx)):
                n.append( int(bx[i]) )

            while len(n) < self.bit:
                n.insert(0, 0)

            return n

    def decimal(self, b):
        """
        Turns a list of bits - formatted as the output of self.binary() - as a base-10 integer

        """
        d = 0;
        for i in range(self.bit):
            d += b[self.bit - 1 - i] * (2 ** i)
        return d

    def lxor(self, l):
        """
        Computes the 'xor' value for every pair of nearby elements in 'l'

        """
        value = l[0];
        for b in l[1:]:
            value = int( value != b )
        return value
