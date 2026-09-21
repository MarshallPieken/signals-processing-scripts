"""
Author: Alex Pieken

This is for plotting symbols from a QPSK signal & extracting thrit bits. 
It started as a general PSK mod identifier but it turned out I was looking at an Iridium QPSK-modded transmission, so I tailored it.
There is also no phase ramping correction here, as the sample rate I was working on luckily produced completely flat phase-derived plots.

Purpose: Determining that the symbols being captured are in fact accurate to their phases.

this file:
- Finds the symbol rate of a cs32 signal file
- turns its data into raw I/Q
- Plots the phase-derived graph for user verification
- Plots the signal constellation for user verification
"""

import matplotlib.pyplot as plt
import numpy as np

def convert(infile):
    """Convert data from input file into int32 for processing
    params:
    - infile: input file
    returns:
    - data: int32 data processed from the file.
    """
    data = np.fromfile(infile, dtype=np.int32)
    return data

def split_stream(data):
    """split the raw extracted data into in-phase (cos(theta)) and quadrature (sin(theta))
    params:
    - data: Data stream to be split
    returns:
    - I: In-phase data (cosine of theta)
    - Q: Quadrature data (sine of theta)"""
    I = data[0::2]
    Q = data[1::2]
    return I, Q

def complexify(I, Q):
    """make a complex array for plotting """
    complex_signal = I + 1j * Q
    complex_signal /= np.iinfo(np.int32).max # restrict to machine limit
    return complex_signal

def plot_basic(data, title):
    """create and show phase plot to the user.
    params:
    - data: raw vector of data to plot.
    - title: title of the graph.
    retuns:
    - plot: The basic plot. 
    """
    plt.figure()
    plt.plot(data)
    plt.grid(True)
    plt.title(title)

def plot_complex(I, Q, title):
    """ This plots both the in-phase and quadrature data streams against one another.
    params:
    - I: in-phase datapoints
    - Q: quadrature datapoints
    returns:
    - plot: the complex plot.
    """
    plt.figure()
    plt.plot(I)
    plt.plot(Q)
    plt.title(title)

def plot_constellation(complex_signal, title):
    """create and show constellation plot to the user"""
    plt.figure()
    plt.plot(np.real(complex_signal), np.imag(complex_signal), '.')
    plt.grid(True); plt.axis("equal")
    plt.axhline(0); plt.axvline(0)
    plt.title(title)

def decode_qpsk(complex_signal, mode="both"):
    """
    Decodes QPSK by acquiring the plotted bitstreams from the constellation, and:
    - determine by magnitude if a symbol is real (e.g., > peak magnitude/2)
    - normalize each sample to sit at a predictable scale (unit avg power)
    - allocates for both absolute and differential QPSK.

    params:
        bits: the streams of bits which are to be decoded.
        
    returns:
        bin: 
    
    I need to learn how the plotted data is structured.
        - what bits map to what quadrant:
                             Q
                            |   
                   [01]  X  |  X  [11]
                            |
                      ------+------ I
                            |
                   [00]  X  |  X  [10]
                            |            
        
        - So, for example, if I > 1 && Q > 1, that symbol is 11 in binary.

    Then, I can transform it by maping it to bits.
        - I need to know what order it's also received in as well, to order the bits in.
        
    Sources:
    - https://tomroelandts.com/articles/mapping-bits-to-a-constellation
    """
    #determining the symbol magnitude
    magnitude = np.abs(complex_signal)
    
    # determine if the symbol is real
    symbol = complex_signal[magnitude > 0.5 * magnitude.max()]
    symbol /= np.sqrt(np.mean(np.abs(symbol)**2))

    # Declare the quadrant; keep positive I and Q; map them to ints from bool, and add. 
    quadrant = (symbol.real < 0).astype(int)*2 + (symbol.imag < 0).astype(int)

    # Diagnostic:
    print("============= QPSK Decode Diagnostics ============")
    print("Symbols kept: ", len(symbol))
    print("quadrant sequence (first 150 symbols):")
    print(''.join(map(str, quadrant[:150])))

    bitstream = {}

    # absolute means between changes in phase
    if mode in ("absolute", "both"):
        b0 = (symbol.real < 0).astype(int)
        b1 = (symbol.imag < 0).astype(int)
        bitstream["absolute"] = np.column_stack([b0, b1]).ravel()
    
    # differential is based off the changes in phase
    if mode in ("differential", "both"):
        d = symbol[:1] * np.conj(symbol[:-1])
        q = np.round(np.mod(np.angle(d), 2*np.pi)/(np.pi/2)).astype(int) % 4
        table = {0:(0,0), 1:(0,1), 2:(1,1), 3:(1,0)} # assign the points
        bitstream["differential"] = np.array([b for x in q for b in table[x]], dtype=int)

    return bitstream 

def main():
    infile = input("Enter the raw .cs32 signal file: ")
    data = convert(infile)
    plot_basic(data, "Raw Phase Data")
    
    I, Q = split_stream(data)
    plot_complex(I, Q, "I/Q Data Streams")
      
    data = complexify(I, Q)
    plot_constellation(data, "Data constellation")
    print("length: ", len(data), "max average: ", np.abs(data).max())
    print("First 8 complex: ", data[:8])    


    # bitstream data for analysis
    bitstream = decode_qpsk(data, "both")
    print("=================== RAW BITS =========================")
    print("ABSOLUTE QPSK:")
    absolute_stream = bitstream["absolute"]
    print("".join(absolute_stream.astype(str)))
    print("DIFFERENTIAL QPSK")
    differential_stream = bitstream["differential"]
    print("".join(differential_stream.astype(str)))

    plt.show() # spit out those plots

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\r\nKeyboard Interrupt.")
