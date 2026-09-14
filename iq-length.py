#!/bin/env python3
"""
This script simply converts the incoming int 32 file into a flat stream of complex numbers.
"""
import numpy as np
infile = input("Enter the PATH of the file: ")

x = np.fromfile(infile, dtype=np.int32, count=2_000_000)
iq = x[0::2] + 1j*x[1::2]
print("IQ length: ",len(iq))


