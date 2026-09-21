#!/usr/bin/env python3
"""
This is simply to see what the average extracted symbol # is.
The closer to zero, the more likely the extraction was accurate.

This also spits out a phase-domain diagram and the symbols in rough binary ( symbol < 0 and symbol > 0) for basic heuristics.
"""
import math
import numpy as np
import matplotlib.pyplot as plt

# Store data for averaging; This is some pull off Inspectrum
SYMBOLS = [0.305614, -0.710449, 0.265014, -0.744802, 0.26131, -0.744031, 0.271389, 0.2812, -0.700352, 0.275097, -0.747799, -0.775862, 0.233837, -0.756326, -0.786403, -0.760584, 0.245077, -0.788677, 0.204225, 0.176769, -0.795532, -0.793733, -0.803806, -0.816203, 0.201775, 0.18994, -0.785006, -0.794165, -0.798572, 0.227273, 0.206197, 0.229929, -0.758877, 0.219552, -0.797148, 0.187009, -0.805079, -0.83128, -0.812291, 0.169932, -0.822564, -0.835403, -0.843569, 0.171416, 0.143549, -0.844829, -0.846119, 0.150038, -0.8455, -0.849982, -0.868564, -0.859626, 0.127434, -0.862864, -0.866312, -0.856036, -0.870834, -0.879081, 0.141733, 0.110228, 0.104072, -0.893281, -0.883739, 0.130357, -0.875569, 0.108871, -0.891484, -0.927604, 0.0966385, 0.0633139, -0.903885, -0.916816, 0.0888971, 0.0660374, 0.0578767, 0.0601923, 0.0702131, 0.0699786, -0.918057, -0.918894, 0.068985, -0.926189, -0.96306, 0.0595179, 0.0875975, -0.942307, 0.0350639, -0.953007, -0.962989, -0.964803, 0.0700449, 0.0695729, 0.0526751, 0.0807553, -0.918431, 0.0553136, -0.950342, -0.970787, -0.971748, -0.974384, -0.980649, -0.972645, -0.990816, -0.969174, 0.0382124, -0.981019, 0.0114309, -0.992595, 0.990847, 0.9754, 0.962247, -0.0088633, -0.00452754, 0.00429254, -0.0290454, -0.0256578, 0.960155, -0.0304036, -0.0481242, 0.991992, 0.975686, 0.997945, -0.0163479, 0.970992, 0.964581, -0.054229, 0.953263, 0.946007, 0.950859, 0.949719]

avg = np.mean(SYMBOLS)
time_array= np.linspace(start=0, stop=len(SYMBOLS), num=len(SYMBOLS))

#Extract binary
binary_extract = []
for i in SYMBOLS:
    if i < 0:
        binary_extract.append('0')
    else:    
        binary_extract.append('1')

#Print the stuff to stdout as well
print("Symbol Average: ", avg)
bin_extract_str = ''.join(binary_extract)
print("Binary Extract: ", bin_extract_str) 

# make hex nibbled out of binary
# for every 4 bits, assign its hex nibble transcription
hextract = hex(int(bin_extract_str))
print("Hex conversion: ", hextract)

#plot the array
plt.figure()
plt.plot(time_array, SYMBOLS, marker='o')
#add a dotted line at y=0
plt.axhline(0, label="y=0")
plt.figtext(0.5, 0.95, f"Average: {avg}", ha="center", fontsize=10)
# plot the raw data
plt.xlabel("Time")
plt.ylabel("Symbol Spacing")
plt.title("Symbols Extracted from Derived plot")
plt.grid(True)

#plot extracted binary
plt.figure()
plt.figtext(0, 0.95, f"Bin dump: {bin_extract_str}", wrap=True)
#plt.figtext(0, 1, f"Bin average: {}", wrap=True)
plt.plot(time_array, binary_extract, marker='o' )
plt.xlabel("time")
plt.ylabel("binary")
plt.title("Binary from Extracted Symbols")
plt.grid(True)

#show the mean
plt.show()
