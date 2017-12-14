# -*- coding: utf-8 -*-

from SimpleConstantObfuscator import SCO
import numpy

sco8 = SCO.SCO(8)       # 8-bit instance of the Constant Obfuscator
sco32 = SCO.SCO(32)     # 32-bit instance
print "Demonstration of the obfuscation. The 'operator.pyc' library is a compiled version of 'op.py'"

n = numpy.random.randint(256)
print "ORIGINAL NUMBER:", n
print ""

code1 = sco8.GetObfuscatedCode("c1", n, comment="At first start, the obfuscator calls the import directives which are needed for execution")
code1_32 = sco32.GetObfuscatedCode("c1_32", n)
print "OBFUSCATED CODE: (generated from an 8-bit obfuscator):"
print ""
print code1, "\n"

# the method generates a working Python code as a string, which can be executed.
print "EXECUTING CODE - 8-bit obfuscator"
exec(code1)
print "8-bit encoding returns:", c1
print ""
print "EXECUTING CODE - 32-bit obfuscator"
exec(code1_32)
print "32-bit encoding returns:", c1_32
