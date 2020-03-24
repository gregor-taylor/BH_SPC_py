#################################
#Python wrappings for Beckr&Hickl SPC C functions
#
#Requirements:
#-Python3
#
#functions are as per documentation for SPC_DLL V4.0, April 2014
#funcs are as per doc with the leading 'SPC_' removed for easier use (with the exception of the init function)
#################################

#===============================
#IMPORTS
#===============================

import ctypes as ct
import SPC_defs as defs

#===============================
#Main Class
#===============================

class SPC():
    def __init__(self, mod_no, ini_file):
        self.SPC_lib = ct.CDLL(".dll") #Need to define dll location
        self.last_retcode = 0

        #Data structures from h file. ct.byref for ints etc, no need for string buffers
        self.errorString = ct.create_string_buffer(b"", 70)
        self.ini_file = ini_file
        self.mod_no = mod_no
        self.in_use = defs.InUseTable()
        self.mod_info = defs.SPCModInfo()
        self.SPCdata = defs.SPCData()
        self.eep_data= defs.SPCEEPData()
        self.adjpara= defs.SPCAdjustPara()
        self.mem_info= defs.SPCMemConfig()
        self.rates=defs.Rates()
        self.stream_info = defs.PhotStreamInfo()
        self.phot_info=defs.PhotInfo64() #assuming 64 bit here 

        self.SPC_value = ct.c_float()
        self.state =ct.c_short()
        self.sync_state=ct.c_short()
        self.bh_time=ct.c_float()
        self.scan_state=ct.c_short()
        self.usage_degree=ct.c_float()
        #These buffers below will likely need to be dynamically determined.
        self.buf= (ct.c_ushort*5e6)() #10Mb
        self.data_buf = (ct.c_char*1e7)() #10Mb

        self.phot_no = ct.c_int()
        self.fifo_type=ct.c_short()
        self.stream_type=ct.c_short()
        self.mt_clock=ct.c_int()
        self.spc_header=ct.c_uint()
        self.count=ct.c_ulong()
        self.buf_size = ct.c_uint()

        #Keeping track of things
        self.stream_hndl = None

        ##################



####Initialisation functions####

    def execute_func(self, retcode, func_name): #Obtains readable error strings from the error code if a func fails.
        self.last_retcode = retcode
        if retcode < 0: #Error codes are less than zero
            self.SPC_lib.SPC_get_error_string(ct.c_int(retcode), self.errorString, 70)
            print("SPC_%s error %d (%s)." % (func_name, retcode, self.errorString.value.decode("utf-8")))

    def SPC_init(self, ini_file): #inits all modules on the bus according to the .ini file
        self.execute_func(self.SPC_lib.SPC_init(ini_file), 'init')

    def get_init_status(self, mod_no): #mod_no = 0...7 module number to be checked
        self.execute_func(self.SPC_lib.SPC_get_init_status(ct.c_short(mod_no)), 'get_init_status')

    def get_module_info(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_module_info(ct.c_short(mod_no), ct.byref(self.mod_info)), 'get_module_info')

    def test_id(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_test_id(ct.c_short(mod_no)), 'test_id')

    def set_mode(self, mode, force_use=0):
        self.execute_func(self.SPC_lib.SPC_set_mode(ct.c_short(mode), ct.c_short(force_use), ct.byref(self.in_use)), 'set_mode')

    def get_mode(self):
        self.execute_func(self.SPC_lib.SPC_get_mode(), 'get_mode')

####Setup functions####

    def get_parameters(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_parameters(ct.c_short(mod_no), ct.byref(self.SPCdata)), 'get_parameters')

    def set_parameters(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_set_parameters(ct.c_short(mod_no), ct.byref(self.SPCdata)), 'set_parameters')

    def get_parameter(self, mod_no, par_id):
        self.execute_func(self.SPC_lib.SPC_get_parameter(ct.c_short(mod_no), ct.c_short(par_id), ct.byref(self.SPC_value)), 'get_parameter')

    def set_parameter(self, mod_no, par_id, value):
        self.execute_func(self.SPC_lib.SPC_set_parameter(ct.c_short(mod_no), ct.c_short(par_id), ct.c_float(self.SPC_value)), 'set_parameter')

    def get_eeprom_data(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_eeprom_data(ct.c_short(mod_no), ct.byref(self.eep_data)), 'get_eeprom_data')

    def write_eeprom_data(self, mod_no, write_enable):
        self.execute_func(self.SPC_lib.SPC_write_eeprom_data(ct.c_short(mod_no), ct.c_ushort(write_enable), ct.byref(self.eep_data)), 'write_eeprom_data')

    def get_adjust_parameters(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_adjust_parameters(ct.c_short(mod_no), ct.byref(self.adjpara)), 'get_adjust_parameters')

    def set_adjust_parameters(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_set_adjust_parameters(ct.c_short(mod_no), ct.byref(self.adjpara)), 'set_adjust_parameters')

    def read_parameters_from_inifile(self, inifile=None):
        if ini_file == None:
            ini_file=self.ini_file
        self.execute_func(self.SPC_lib.SPC_read_parameters(ct.byref(self.SPCdata), ct.c_wchar_p(inifile)), 'read_parameters_from_inifile')

    def save_parameters_to_inifile(self, dest_inifile, source_inifile, with_comments): #source_inifile can be None
        self.execute_func(self.SPC_lib.SPC_save_parameters_to_inifile(ct.byref(self.SPCdata), ct.c_wchar_p(dest_inifile), ct.c_wchar_p(source_inifile), ct.c_int(with_comments)), 'save_parameters_to_inifile')

####Status functions####

    def test_state(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_test_state(ct.c_short(mod_no), ct.byref(self.state)), 'test_state')

    def get_sync_state(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_sync_state(ct.c_short(mod_no), ct.byref(self.sync_state)), 'get_sync_state')

    def get_time_from_start(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_time_from_start(ct.c_short(mod_no), ct.byref(self.bh_time)), 'get_time_from_start')

    def get_break_time(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_break_time(ct.c_short(mod_no),ct.byref(self.bh_time)), 'get_break_time')

    def get_actual_coltime(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_actual_coltime(ct.c_short(mod_no), ct.byref(self.bh_time)), 'get_actual_coltime')

    def read_rates(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_read_rates(ct.c_short(mod_no), ct.byref(self.rates)), 'read_rates')

    def clear_rates(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_clear_rates(ct.c_short(mod_no)), 'clear_rates')

    def get_sequencer_state(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_sequencer_state(ct.s_short(mod_no), ct.byref(self.state)), 'get_sequencer_state')

    def read_gap_time(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_read_gap_time(ct.c_short(mod_no), ct.byref(self.bh_time)), 'read_gap_time')

    def get_scan_clk_state(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_scan_clk_state(ct.c_short(mod_no), ct.byref(self.scan_state)), 'get_scan_clk_state')

    def get_fifo_usage(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_fifo_usage(ct.c_short(mod_no), ct.byref(self.usage_degree)), 'get_fifo_usage')

####Measurement control functions####
    
    def start_measurement(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_start_measurement(ct.c_short(mod_no)), 'start_measurement')

    def pause_measurement(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_pause_measurement(ct.c_short(mod_no)), 'pause_measurement')

    def restart_measurement(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_restart_measurement(ct.c_short(mod_no)), 'restart_measurement')

    def stop_measurement(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_stop_measurement(ct.c_short(mod_no)), 'stop_measurement')

    def set_page(self, mod_no, page):
        self.execute_func(self.SPC_lib.SPC_set_page(ct.c_short(mod_no), ct.c_long(page)), 'set_page')

    def enable_sequencer(self, mod_no, enable):
        self.execute_func(self.SPC_lib.SPC_enable_sequencer(ct.c_short(mod_no), ct.c_short(enable)), 'enable_sequencer')

####Memory transfer functions####

    def configure_memory(self, mod_no, adc_resolution, no_of_routing_bits):
        self.execute_func(self.SPC_lib.SPC_configure_memory(ct.c_short(mod_no), ct.c_short(adc_resolution), ct.c_short(no_of_routing_bits), ct.byref(self.mem_info)), 'configure_memory') 

    def fill_memory(self, mod_no, block, page, fill_value):
        self.execute_func(self.SPC_lib.SPC_fill_memory(ct.c_short(mod_no), ct.c_long(block), ct.c_long(page), ct.c_ushort(fill_value)), 'fill_memory')

    def read_data_block(self, mod_no, block, page, reduction_factor, bh_from, bh_to):
        self.execute_func(self.SPC_lib.SPC_read_data_block(ct.c_short(mod_no), ct.c_long(block), ct.c_long(page), ct.c_short(reduction_factor), ct.c_short(bh_from), ct.c_short(bh_to), ct.byref(self.buf)), 'read_data_block')

    def write_data_block(self, mod_no, block, page, bh_from, bh_to):
        self.execute_func(self.SPC_lib.SPC_write_data_block(ct.c_short(mod_no), ct.c_long(block), ct.c_long(page), ct.c_short(bh_from), ct.c_short(bh_to), ct.byref(self.buf)), 'write_data_block')

    def read_fifo(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_read_fifo(ct.c_short(mod_no), ct.byref(self.count), ct.byref(self.buf)), 'read_fifo')

    def read_data_frame(self, mod_no, frame, page):
        self.execute_func(self.SPC_lib.SPC_read_data_frame(ct.c_short(mod_no), ct.c_long(frame), ct.c_long(page), ct.byref(self.buf)), 'read_data_frame')

    def read_data_page(self, mod_no, first_page, last_page):
        self.execute_func(self.SPC_lib.SPC_read_data_page(ct.c_short(mod_no), ct.c_long(first_page), ct.c_long(last_page), ct.byref(self.buf)), 'read_data_page')

    def read_block(self, mod_no, block, frame, page, bh_from, bh_to):
        self.execute_func(self.SPC_lib.SPC_read_block(ct.c_short(mod_no), ct.c_long(block), ct.c_long(frame), ct.c_long(page), ct.c_short(bh_from), ct.c_long(bh_to), ct.byref(self.buf)), 'read_block')

    def save_data_to_sdtfile(self, mod_no, data_buffer, bytes_no, sdt_file): #data_buffer is a pointer to the data you want to save
        self.execute_func(self.SPC_lib.SPC_save_data_to_sdtfile(ct.c_short(mod_no), data_buffer, ct.c_ulong(bytes_no), ct.c_wchar_p(sdt_file)), 'save_data_to_sdtfile')

####Functions to manage photon streams####

    def init_phot_stream(self, fifo_type, spc_file, files_to_use, stream_type, what_to_read):
        self.execute_func(self.SPC_lib.SPC_init_phot_stream(ct.c_short(fifo_type), ct.c_wchar_p(spc_file), ct.c_short(files_to_use), ct.c_short(stream_type), ct.c_short(what_to_read)), 'init_phot_stream')
        self.stream_hndl = self.last_retcode

    def get_phot_stream_info(self, stream_hndl):
        self.execute_func(self.SPC_lib.SPC_get_phot_stream(ct.c_short(stream_hndl), ct.byref(self.stream_info)), 'get_phot_stream_info')

    def get_photon(self, stream_hndl):
        self.execute_func(self.SPC_lib.SPC_get_photon(ct.c_short(stream_hndl), ct.byref(self.phot_info)), 'get_photon')

    def close_phot_stream(self, stream_hndl):
        self.execute_func(self.SPC_lib.SPC_close_phot_stream(ct.c_short(stream_hndl)), 'close_phot_stream')
        self.stream_hndl = None

    def get_fifo_init_vars(self, mod_no):
        self.execute_func(self.SPC_lib.SPC_get_fifo_init_vars(ct.c_short(mod_no), ct.byref(self.fifo_type), ct.byref(self.stream_type), ct.byref(mt_clock), ct.byref(spc_header)), 'get_fifo_init_vars')

    def init_buf_stream(self, fifo_type, stream_type, what_to_read, mt_clock):
        self.execute_func(self.SPC_lib.SPC_init_buf_stream(ct.c_short(fifo_type), ct.c_short(stream_type), ct.c_short(what_to_read), ct.c_int(mt_clock), ct.c_uint(0)), 'init_buf_stream')
        self.stream_hndl = self.last_retcode

    def add_data_to_stream(self, photon_buffer, stream_hndl, bytes_no): #photon_buffer is pointer to buffer of data to be added
        self.execute_func(self.SPC_lib.SPC_add_data_to_stream(ct.c_short(stream_hndl), photon_buffer, ct.c_uint(bytes_no)), 'add_data_to_stream')

    def read_fifo_to_stream(self, stream_hndl, mod_no):
        self.execute_func(self.SPC_lib.SPC_read_fifo_to_stream(ct.c_short(stream_hndl), ct.c_short(mod_no), ct.byref(self.count)), 'read_fifo_to_stream')

    def get_photons_from_stream(self, stream_hndl):
        self.execute_func(self.SPC_lib.SPC_get_photons_from_stream(ct.c_short(stream_hndl), self.phot_info, ct.byref(self.phot_no)), 'get_photons_from_stream')

    def stream_start_condition(self, stream_hndl, start_time, start_OR_mask, start_AND_mask):
        self.execute_func(self.SPC_lib.SPC_stream_start_condition(ct.c_short(stream_hndl), ct.c_double(start_time), ct.c_uint(start_OR_mask), ct.c_uint(start_AND_mask)), 'stream_start_condition')

    def stream_stop_condition(self, stream_hndl, stop_time, stop_OR_mask, stop_AND_mask):
        self.execute_func(self.SPC_lib.SPC_stream_stop_condition(ct.c_short(stream_hndl), ct.c_double(stop_time), ct.c_uint(stop_OR_mask), ct.c_uint(stop_AND_mask)), 'stream_stop_condition')

    def stream_reset(self, stream_hndl):
        self.execute_func(self.SPC_lib.SPC_stream_reset(ct.c_short(stream_hndl)), 'stream_reset')

    def get_stream_buffer_size(self, stream_hndl, buf_no):
        self.execute_func(self.SPC_lib.SPC_get_stream_buffer_size(ct.c_short(stream_hndl), ct.c_ushort(buf_no), ct.byref(self.buf_size)), 'get_stream_buffer_size')

    def get_buffer_from_stream(self, stream_hndl, buf_no, free_buf):
        self.execute_func(self.SPC_lib.SPC_get_buffer_from_stream(ct.c_short(stream_hndl), ct.c_ushort(buf_no), ct.byref(self.buf_size), self.data_buf, ct.c_short(free_buf)), 'get_buffer_from_stream')

####Other functions####

    def get_error_string(self, error_id, max_length):
        self.execute_func(self.SPC_lib.SPC_get_error_string(ct.c_short(error_id), self.errorString, ct.c_short(max_length)), 'get_error_string')

    def get_detector_info(self, previous_type, det_type, fname):
        self.execute_func(self.SPC_lib.SPC_get_detector_info(ct.c_short(previous_type), ct.c_short(det_type), ct.c_wchar_p(fname)), 'get_detector_info')


















