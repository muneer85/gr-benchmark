# Benchmark Test

## Overview
Benchmark Test Block is a benchmarking module that can evaluate the performance of wireless communication systems over the air using the GNU Radio Companion (GRC). This block can be used to obtain the following performance metrics in a realistic communication channel: Packet Error Rate (PER), Packet Loss Rate (PLR), Signal-to-Noise Ratio (SNR), and Throughput. In addition, it provides information about the transmission duration, the correctly/incorrectly received packets, and the total received data size. The output data is displayed in the GRC console window and stored in an external CSV file with more details. A GRC flowgraph example of how to use this block is demonstrated below.

**Important Notes**

•	This block can work with any communication system that uses the cyclic redundancy check (CRC) at the transmitter. Therefore, the CRC should be appended to the transmitted packets before transmission.

•	The user should use this block at the receiver and should first run the receiver before starting data transmission by the transmitter. 

•	The data transmission process should be for a specific period (i.e., the transmitter should stop transmission after some time). 

•	The benchmark block will output performance metrics after approximately 5 seconds of completing the transmission process by the transmitter. 

## Installation
Use the fellowing code to build and install the Benchmark Test block to GNU Radio:
```
git clone https://github.com/muneer85/gr-benchmark.git
cd gr-benchmark
mkdir build
cd build
cmake ..
make
make install  # may need sudo make install
ldconfig      # may need sudo ldconfig

```
The new block can be found in the block list under the "Benchmark Test" category.

**Requirements**
• GNU Radio (3.10+)
• Python (3.10+)
• CMake (3.1.0+)
• swig 

## Parameters & Input/Output Signals
### Parameters
-	***Output file***:  Path and file name to store the resulting measurement data. If the file already exists, new measurements will be appended to this file in a new row.
-	***Time zone***: The time zone to be used for getting the date/time in the area where the measurement is conducted. The date/time will be stored in the output file with the corresponding measured data. The time zone can be obtained from the IANA time zone database or the attached TimeZones.txt file. 
-	***Test mode***: This option can be used to make the block work in over-the-air mode or simulation mode. This block supports only over-the-air mode while the simulation mode will be added in the future version. 
-	***Modulation order***: It is a parameter M that determines the number of the different symbols that can be transmitted. For example, M=2 for BPSK and M=4 for QPSK. 
-	***Number of sent packets***: Total number of packets transmitted by the transmitter. It can be determined by dividing the total transmitted data size by packet length.
-	***Packet length***: The size of the transmitted packet (payload) in bytes.
-	***FFT vector length***: This parameter determines the number of samples (bins) used in the FFT calculation, which also determines how many points are in the output.
-	***No. of FFT iterations***: The number of iterations used to average the magnitude of the FFT samples (bins). This average process is used in the SNR calculation process and to average the FFT samples at the block output. It is not a critical parameter but can help in getting more accurate and reliable results. 
-	***Channel BW***: The range of frequencies (channel bandwidth) occupied by the transmitted signal in Hz.
-	***Center frequency***: The frequency in hertz used by the transmitter.
-	***Sample rate***: The number of samples per second. This parameter determines the indices of the FFT bins used in the power calculation process. 
-	***TX power***: The transmit power or gain used by the transmitter in dBm or dB. This parameter is only used as a remark added to the measured data in the output file. It is not used in the performance evaluation process. 
-	***Ant. gain***: The antenna gain in dBi or dBd. This parameter is only used as a remark added to the measured data in the output file. It is not used in the performance evaluation process. 
-	***No. of discarded packets***: Number of packets you want to exclude from the error rate calculation for any reason.
-	***Note***: The comment or note you want to add to the measured data stored in the output file. For example, you can add the GPS coordinates or address of the receiver.

  ## Input:
-	***in_sig***: The input port for the FFT samples of the received signal before demodulation. The FFT samples can be generated using the FFT block in GNU Radio with a size defined using the parameter “FFT vector length”. The FFT block output should be directly connected to the “in_sig” input port. However, the input data stream to the FFT block should be first converted to a vector of size “FFT vector length” using the “Stream to Vector” block. 

-	***msg_in_ok & msg_in_fail***: These input message ports are used to receive the status of the CRC-checked packets which can be either correct (ok) or incorrect (fail). These input ports should be connected to the corresponding output ports of the “CRC Check” block in GNU Radio. The data stream entering the “CRC Check” block should be first converted to PDU messages using the “Tagged Stream to PDU” block which is connected to the last point in the receiver GRC flowgraph just before performing the CRC check. 

## Output:
-	***out_sig***: This port can be used to visualize the frequency spectrum of the received signal averaged over multiple readings defined using the parameter “No. of FFT iterations”. It can be connected to the “GUI vector Sink” block to plot the output vectors of data after adjusting the “Vector Size” parameter to “FFT vector length”.

## Example Flowgraph 

### GFSK Transmitter Flowgraph 

### GFSK Receiver Flowgraph 

### Connection of The Benchmark Test Block and the Receiver 






##
