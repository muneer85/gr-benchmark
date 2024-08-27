#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2024 MUNEER ALZUBI.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr
import pmt
import time
from datetime import datetime
from csv import writer
import csv
import io
import os
import math
import pytz

class Benchmark(gr.sync_block):
    """
    docstring for block Benchmark
    """
    def __init__(self, file_out, time_zone, test_mode, Num_sent_Packets, packet_length, vector_size, iter_avg, ch_bw, freq_center, sample_rate, tx_power, Ant_gain, N_disc_packtet, Note, mod_order):
    
        gr.sync_block.__init__(self, name="Benchmark", in_sig=[(np.complex64,vector_size)], out_sig=[(np.float32,vector_size)])
        
        """ define parameters from input"""
        self.Num_sent_Packets     = int(Num_sent_Packets)
        self.packet_length        = int(packet_length)           # Payload length (packet length=payload+header)
        self.N_disc_packtet       = int(N_disc_packtet)    
        self.sample_rate          = int(sample_rate)
        self.iter_avg             = int(iter_avg)
        self.vector_size          = int(vector_size)
        self.ch_bw                = ch_bw
        self.freq_center          = freq_center
        self.test_mode            = test_mode
        self.time_zone            = time_zone
        self.file_out             = file_out
        self.tx_power             = tx_power
        self.Ant_gain             = Ant_gain        
        self.fft_bin_start        = int((self.vector_size/self.sample_rate)*(self.ch_bw/2))
        self.fft_bin_end          = int(self.fft_bin_start * 3)
        self.Note                 = Note
        self.mod_order            = int(mod_order) 
        
        """ define parameters in current class"""
        self.ok_counter    	  = 0
        self.fail_counter         = 0
        self.start_rx             = 0
        self.start1               = time.time()
        self.end1                 = 0

        self.start2               = time.time()
        self.end2                 = 0
        self.packet_counter       = 0
        self.byte_counter         = 0

        self.counter   		  = 0
        self.mag2_sum             = 0
        self.state                = 0
        self.P_n                  = 0
        self.P_s                  = 0
        self.P_avg_bw             = 0
        
        """ define input msg port 1"""
        self.message_port_register_in(pmt.intern('msg_in_ok')) # register/create input port for msg
        self.set_msg_handler(pmt.intern('msg_in_ok'), self.handle_msg_1) # connect msg input port with msg handle function
        
        """ define input msg port 2"""
        self.message_port_register_in(pmt.intern('msg_in_fail')) # register/create input port for msg
        self.set_msg_handler(pmt.intern('msg_in_fail'), self.handle_msg_2) # connect msg input port with msg handle function

        """ define output msg port"""
        #self.message_port_register_out(pmt.intern('msg_out'))# register/create output port for msg


        print("Waiting for packets to be sent...")
        		
    """ msg handler is called when msg arraive at port"""
    def handle_msg_1(self, msg):

        if(self.start_rx==0):
            self.start1   = time.time()
            self.start_rx = 1

        self.ok_counter     = self.ok_counter + 1
        self.start2         = time.time()
        self.end1           = time.time()
        self.P_s            = self.P_avg_bw
        
        print(self.ok_counter+self.fail_counter, " : correct packet...")

    def handle_msg_2(self, msg):
        
        if(self.start_rx==0):
            self.start1 = time.time()
            self.start_rx = 1
            
        self.fail_counter = self.fail_counter + 1
        self.start2       = time.time()
        self.end1         = time.time()
        self.P_s          = self.P_avg_bw      
        
        print(self.ok_counter+self.fail_counter, " : incorrect packet...")
        
    """ Main Function"""
    def work(self, input_items, output_items):
    
        in_sig              = input_items[0]
        out_sig             = output_items[0]

        self.counter        = self.counter + 1                     # counter for ftt vector average
        fft_scale           = in_sig*1/(self.vector_size)          # mutiplay by 1/(fft vector_size)
        fft_mag2            = abs(fft_scale)**2                    # magnitude-squared of complex fft bin        
        self.mag2_sum       = self.mag2_sum + np.sum(fft_mag2, axis=0) # sum of many received ftt vectors in order to be averaged

        if(self.counter == self.iter_avg):
            fft_avg         = self.mag2_sum/self.iter_avg     # power in watt in each FFT bin (vector of size "Vector_Size") which averaged over a number of reading (iter_avg)
            fft_avg_dB      = 10*np.log10(fft_avg)
            
            fft_avg_bw      = fft_avg[self.fft_bin_start:self.fft_bin_end] # power in ftt bins within ch bandwidth only
            self.P_avg_bw   = sum(fft_avg_bw)                 # average power in watt over FFT bins of size (Vector_Size)
            P_avg_bw_dB     = 10*np.log10(self.P_avg_bw)      # average power dB over all FFT bins of size (Vector_Size) 
                
            out_sig[:]      = fft_avg_dB

            self.counter    = 0 
            self.mag2_sum   = 0


         #=====================================================
        self.end2             = time.time()
        Time_lapse_end_sent   = self.end2 - self.start2       # time after no packet arraived at rx
        
        #if(self.start_rx==1 and int(Time_lapse_end_sent)>5):
        if(self.start_rx==1 and self.P_avg_bw<(self.P_s/2) and int(Time_lapse_end_sent)>5):

            self.P_n          = self.P_avg_bw

            correct_packets   = self.ok_counter 
            incorrect_packets = self.fail_counter - self.N_disc_packtet
            received_packets  = correct_packets + incorrect_packets
            
            Time_lapse        = self.end1 - self.start1

            if(Time_lapse>0):
                Throughput    = (correct_packets*self.packet_length*8)/Time_lapse /1000
                
                Packet_Durtion= (Time_lapse / received_packets) *1000
                #Symb_Duration = (Packet_Durtion / (self.packet_length * 8))* (math.log2(self.mod_order))
            else:
                Throughput    = "NA"
                Packet_Durtion= "NA"
                #Symb_Duration = "NA"
                            
            DataBytes         = correct_packets*self.packet_length / 1000



            if(received_packets>0):
                PER           = (incorrect_packets-self.N_disc_packtet) / (self.Num_sent_Packets-self.N_disc_packtet)
            else:
                PER           = "NA"
            
            PLR               = ((self.Num_sent_Packets - self.N_disc_packtet) - received_packets) / (self.Num_sent_Packets- self.N_disc_packtet)

            if(abs(self.P_n)>0 and abs(self.P_s)>0):
                SNR_dB        = 10*np.log10((self.P_s-self.P_n)/self.P_n)
            else:
                SNR_dB        = "NA"
            
            print("################")
            print("Please see the collected data below (full ") 
            print("details stored in the output CSV file):   ") 
            print("                                          ")   
            print("Total Duration (s)  : ", Time_lapse)
            print("Latency (ms)        : ", Packet_Durtion)
            print("Throughput (Kbps)   : ", Throughput)
            print("Received Data (KB)  : ", DataBytes)
            print("PER                 : ", PER)
            print("PLR                 : ", PLR)
            print("SNR (dB)            : ", SNR_dB)
            print("                                          ")   
            print("################")
                        
            #========================
            # Add data to CSV file
            #========================
            date_time = str(datetime.now(pytz.timezone(self.time_zone)))

            file_data = self.file_out

            file_exists = os.path.isfile(file_data)
            if not file_exists:
                # add header
                columns = ["Date_Time", "Duration (s)", "Throughput (Kbps)", "Rx Bytes (KB)", "PER", "PLR", "SNR (dB)", "Rx Correct Packets", "Rx InCorrect Packets", "Latency (ms)" ,"Tx Packets", "Packet(Payload) Length (Bytes)", "Frequency (KHz)" , "Channel BW (KHz)", "Sample Rate (Ksps)", "Transmit Power (dBm)", "Antenna Gain (dBi)", "Note"]
                with open(file_data, mode='w', newline='') as csv_file:
                    csv_writer = csv.DictWriter(csv_file, fieldnames=columns)
                    csv_writer.writeheader()
                    
            data    = [date_time, Time_lapse, Throughput, DataBytes, PER, PLR, SNR_dB, correct_packets, incorrect_packets, Packet_Durtion, self.Num_sent_Packets, self.packet_length, self.freq_center/1e3, self.ch_bw/1e3, self.sample_rate/1e3, self.tx_power, self.Ant_gain, self.Note]

            # writing to csv file
            with open(file_data, 'a', newline='') as f_object:
                # Pass this file object to csv.writer() and get a writer object
                writer_object = writer(f_object)
                # Pass the list as an argument into the writerow()
                writer_object.writerow(data)
                # Close the file object
                f_object.close()
            #========================
            #========================

            self.start_rx     = 0
            self.ok_counter   = 0
            self.fail_counter = 0

            print("Measurement Completed!")
            print("")   
            print("Waiting for packets to be sent...")

        return len(output_items[0])
