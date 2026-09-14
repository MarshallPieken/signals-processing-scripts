#!/bin/env python3

import numpy as np
infile = input("Enter the PATH of the file to cut: ")

x = np.fromfile(infile, dtype=np.int32, count=2_000_000)
iq = x[0::2] + 1j*x[1::2]
print("IQ length: ",len(iq))


