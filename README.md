# Benchmark Test

## Overview
Benchmark Test Block is a benchmarking module that can evaluate the performance of wireless communication systems over the air using the GNU Radio Companion (GRC). This block can be used to obtain the following performance metrics in a realistic communication channel: Packet Error Rate (PER), Packet Loss Rate (PLR), Signal-to-Noise Ratio (SNR), and Throughput. In addition, it provides information about the transmission duration, the correctly/incorrectly received packets, and the total received data size. The output data is displayed in the GRC console window and stored in an external CSV file with more details. A GRC flowgraph example of how to use this block is demonstrated below.

**Important Notes:**

•	This block can work with any communication system that uses the cyclic redundancy check (CRC) at the transmitter. Therefore, the CRC should be appended to the transmitted packets before transmission.

•	The user should use this block at the receiver and should first run the receiver before starting data transmission by the transmitter. 

•	The data transmission process should be for a specific period (i.e., the transmitter should stop transmission after some time). 

•	The benchmark block will output performance metrics after approximately 5 seconds of completing the transmission process by the transmitter. 

## Installation
### make sure you have swig installed
