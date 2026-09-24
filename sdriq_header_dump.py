"""
Author: Alex Pieken
This is a simple script to read & dump raw .sdriq header files. 
Useful for loading ADRAngel capture outputs into other programs (GNURadio, Inspectrum).
"""
import struct

infile = input("Enter the input file PATH: ")

with open(infile,'rb') as f:
    header= f.read(32)

# common SDRIQ layout: sample_rate (uint32 LE) then center_freq (uint64 LE) early in the header
sample_rate, center_freq, start_timestamp, sample_size = struct.unpack("IQQI", header)

print("sample rate:",               sample_rate)
print("file center frequency: ",    center_freq)
print("starting timestamp: ",       start_timestamp)
print("sample size: ",              sample_size)
