#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Demodulador_RFM22B
# Author: Renzo Ch.
# Generated: Thu Mar 30 15:39:43 2017
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from GFSK_Demod import GFSK_Demod  # grc-generated hier_block
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import cc1111
import math
import osmosdr
import time


class rfm22b_demod(gr.top_block):

    def __init__(self):
        gr.top_block.__init__(self, "Demodulador_RFM22B")

        ##################################################
        # Variables
        ##################################################
        self.symbole_rate = symbole_rate = 2400
        self.samp_rate = samp_rate = 2e6
        self.rat_interop = rat_interop = 8
        self.rat_decim = rat_decim = 5
        self.firdes_decim = firdes_decim = 4
        self.deviation = deviation = 36e3
        self.samp_per_sym = samp_per_sym = ((samp_rate/2/firdes_decim)*rat_interop/rat_decim)/symbole_rate
        self.modulation_index = modulation_index = float(deviation/(symbole_rate/2))
        self.frequency_tune = frequency_tune = -2e3
        self.frequency_shift = frequency_shift = 100e3
        self.frequency_center = frequency_center = 915e06
        self.firdes_transition_width = firdes_transition_width = 19000
        self.firdes_cutoff = firdes_cutoff = 38e3
        self.sensitivity = sensitivity = float((math.pi*modulation_index)/samp_per_sym)
        self.msg_sink = msg_sink = gr.msg_queue(2)
        self.frequency = frequency = frequency_center + frequency_shift + frequency_tune
        self.firdes_filter = firdes_filter = firdes.low_pass(1,samp_rate/2, firdes_cutoff, firdes_transition_width)
        self.bit_per_sym = bit_per_sym = 1

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_ccc(
                interpolation=rat_interop,
                decimation=rat_decim,
                taps=None,
                fractional_bw=None,
        )
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + "bladerf=0,buffers=64,buflen=1024,transfers=32" )
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(frequency, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(1, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(3, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(33, 0)
        self.osmosdr_source_0.set_antenna("", 0)
        self.osmosdr_source_0.set_bandwidth(2e6, 0)
          
        self.freq_xlating_fir_filter_xxx_1 = filter.freq_xlating_fir_filter_ccc(2, (1, ), 0, samp_rate)
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(firdes_decim, (firdes_filter), frequency_shift+frequency_tune, samp_rate/2)
        self.digital_correlate_access_code_bb_0_0 = digital.correlate_access_code_bb("0010110111010100", 1)
        self.cc1111_cc1111_packet_decoder_0 = cc1111.cc1111_packet_decoder(msg_sink,False, False, False, False)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.GFSK_Demod_0 = GFSK_Demod()

        ##################################################
        # Connections
        ##################################################
        self.connect((self.GFSK_Demod_0, 0), (self.digital_correlate_access_code_bb_0_0, 0))    
        self.connect((self.cc1111_cc1111_packet_decoder_0, 0), (self.blocks_null_sink_0_0, 0))    
        self.connect((self.digital_correlate_access_code_bb_0_0, 0), (self.cc1111_cc1111_packet_decoder_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.rational_resampler_xxx_0_0, 0))    
        self.connect((self.freq_xlating_fir_filter_xxx_1, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))    
        self.connect((self.osmosdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_1, 0))    
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.GFSK_Demod_0, 0))    

    def get_symbole_rate(self):
        return self.symbole_rate

    def set_symbole_rate(self, symbole_rate):
        self.symbole_rate = symbole_rate
        self.set_modulation_index(float(self.deviation/(self.symbole_rate/2)))
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim)/self.symbole_rate)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cutoff, self.firdes_transition_width))
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim)/self.symbole_rate)
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)

    def get_rat_interop(self):
        return self.rat_interop

    def set_rat_interop(self, rat_interop):
        self.rat_interop = rat_interop
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim)/self.symbole_rate)

    def get_rat_decim(self):
        return self.rat_decim

    def set_rat_decim(self, rat_decim):
        self.rat_decim = rat_decim
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim)/self.symbole_rate)

    def get_firdes_decim(self):
        return self.firdes_decim

    def set_firdes_decim(self, firdes_decim):
        self.firdes_decim = firdes_decim
        self.set_samp_per_sym(((self.samp_rate/2/self.firdes_decim)*self.rat_interop/self.rat_decim)/self.symbole_rate)

    def get_deviation(self):
        return self.deviation

    def set_deviation(self, deviation):
        self.deviation = deviation
        self.set_modulation_index(float(self.deviation/(self.symbole_rate/2)))

    def get_samp_per_sym(self):
        return self.samp_per_sym

    def set_samp_per_sym(self, samp_per_sym):
        self.samp_per_sym = samp_per_sym
        self.set_sensitivity(float((math.pi*self.modulation_index)/self.samp_per_sym))

    def get_modulation_index(self):
        return self.modulation_index

    def set_modulation_index(self, modulation_index):
        self.modulation_index = modulation_index
        self.set_sensitivity(float((math.pi*self.modulation_index)/self.samp_per_sym))

    def get_frequency_tune(self):
        return self.frequency_tune

    def set_frequency_tune(self, frequency_tune):
        self.frequency_tune = frequency_tune
        self.set_frequency(self.frequency_center + self.frequency_shift + self.frequency_tune)
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.frequency_shift+self.frequency_tune)

    def get_frequency_shift(self):
        return self.frequency_shift

    def set_frequency_shift(self, frequency_shift):
        self.frequency_shift = frequency_shift
        self.set_frequency(self.frequency_center + self.frequency_shift + self.frequency_tune)
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.frequency_shift+self.frequency_tune)

    def get_frequency_center(self):
        return self.frequency_center

    def set_frequency_center(self, frequency_center):
        self.frequency_center = frequency_center
        self.set_frequency(self.frequency_center + self.frequency_shift + self.frequency_tune)

    def get_firdes_transition_width(self):
        return self.firdes_transition_width

    def set_firdes_transition_width(self, firdes_transition_width):
        self.firdes_transition_width = firdes_transition_width
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cutoff, self.firdes_transition_width))

    def get_firdes_cutoff(self):
        return self.firdes_cutoff

    def set_firdes_cutoff(self, firdes_cutoff):
        self.firdes_cutoff = firdes_cutoff
        self.set_firdes_filter(firdes.low_pass(1,self.samp_rate/2, self.firdes_cutoff, self.firdes_transition_width))

    def get_sensitivity(self):
        return self.sensitivity

    def set_sensitivity(self, sensitivity):
        self.sensitivity = sensitivity

    def get_msg_sink(self):
        return self.msg_sink

    def set_msg_sink(self, msg_sink):
        self.msg_sink = msg_sink

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self.osmosdr_source_0.set_center_freq(self.frequency, 0)

    def get_firdes_filter(self):
        return self.firdes_filter

    def set_firdes_filter(self, firdes_filter):
        self.firdes_filter = firdes_filter
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((self.firdes_filter))

    def get_bit_per_sym(self):
        return self.bit_per_sym

    def set_bit_per_sym(self, bit_per_sym):
        self.bit_per_sym = bit_per_sym


def main(top_block_cls=rfm22b_demod, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls()
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
