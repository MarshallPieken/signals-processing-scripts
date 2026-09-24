"""
Author: Alex Pieken
This is a simple script to read & dump raw .sdriq header files. 
Useful for loading ADRAngel capture outputs into other programs (GNURadio, Inspectrum).
"""
import numpy as np

infile = input("Enter the input file PATH: ")

with open(infile,'rb') as f:
    hdr = f.read(32)

# common SDRIQ layout: sample_rate (uint32 LE) then center_freq (uint64 LE) early in the header
header = np.frombuffer(hdr, dtype='<u4', count=4)
sample_rate = header[0]
center_freq = header[1]
start_timestamp = header[2]
sample_size = header[3]
print("sample rate:", sample_rate)
print("file center frequency: ", center_freq)
print("starting timestamp: ", start_timestamp)
print("sample size: ", sample_size)
