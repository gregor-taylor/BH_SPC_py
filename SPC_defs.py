import ctypes as ct

#Constant Definitions
Module_States={0x1:'SPC_OVERFL', 0x2:'SPC_OVERFLOW', 0x4:'SPC_TIME_OVER', 0x8:'SPC_COLTIM_OVER', 0x10:'SPC_CMD_STOP',
               0x80:'SPC_ARMED', 0x20:'SPC_REPTIM_OVER', 0x100:'SPC_COLTIM_2OVER', 0x200:'SPC_REPTIM_2OVER', 0x40:'SPC_MEASURE',
               0x400:'SPC_FOVFL OR SPC_SCRDY',0x800:'SPC_FEMPTY OR SPC_FBRDY', 0x1000:'SPC_WAIT_TRIG', 0x8000:'SPC_HFILL_NRDY',
               0x4000:'SPC_SEQ_STOP', 0x2000:'SPC_SEQ_GAP150 OR SPC_WAIT_FR'}

Sequencer_States={0x1:'SPC_SEQ_ENABLE',0x2:'SPC_SEQ_RUNNING',0x4:'SPC_SEQ_GAP_BANK'}

Init_Error_Codes={0:'INIT_SPC_OK', -1:'INIT_SPC_NOT_DONE', -2:'INIT_SPC_WRONG_EEP_CHKSUM', -3:'INIT_SPC_WRONG_MOD_ID', -4:'INIT_SPC_HARD_TEST_ERR',
                  -5:'INIT_SPC_CANT_OPEN_PCI_CARD', -6:'INIT_SPC_MOD_IN_USE', -7:'INIT_SPC_WINDRVR_VER', -8:'INIT_SPC_WRONG_LICENSE', -9:'INIT_SPC_FIRMWARE_VER',
                  -10:'INIT_SPC_NO_LICENSE', -11:'INIT_SPC_LICENSE_NOT_VALID', -12:'INIT_SPC_LICENSE_DATE_EXP', -100:'INIT_SPC_XILINX_ERR'}

Modes={0:'ROUT_IN', 1:'ROUT_OUT', 2:'SCAN_IN', 3:'SCAN_OUT', 5:'FIFO_32M', }

Sync_States={0:'NO SYNC', 1:'SYNC OK', 2:'SYNC OVERLOAD', 3:'SYNC_OVERLOAD'}

Scan_Clk_States={1:'EXTERNAL PIXEL CLOCK PRESENT', 2:'LINE CLOCK PRESENT', 3:'PIXEL/LINE CLOCK PRESENT', 4:'FRAME CLOCK PRESENT', 5:'FRAME/PIXEL CLOCK PRESENT',
                 6:'FRAME/LINE CLOCK PRESENT', 7:'FRAME/LINE/PIXEL CLOCK PRESENT'}

Parameter_IDs={'CFD_LIMIT_LOW':0, 'CFD_LIMIT_HIGH':1, 'CFD_ZC_LEVEL':2, 'CFD_HOLDOFF':3, 'SYNC_ZC_LEVEL':4, 'SYNC_FREQ_DIV':5, 'SYNC_HOLDOFF':6, 'SYNC_THRESHOLD':7, 'TAC_RANGE':8,
               'TAC_GAIN':9, 'TAC_OFFSET':10, 'TAC_LIMIT_LOW':11, 'TAC_LIMIT_HIGH':12, 'ADC_RESOLUTION':13, 'EXT_LATCH_DELAY':14, 'COLLECT_TIME':15, 'DISPLAY_TIME':16,
               'REPEAT_TIME':17, 'STOP_ON_TIME':18, 'STOP_ON_OVFL':19, 'DITHER_RANGE':20, 'COUNT_INCR':21, 'MEM_BANK':22, 'DEAD_TIME_COMP':23, 'SCAN_CONTROL':24, 'ROUTING_MODE':25,
               'TAC_ENABLE_HOLD':26, 'MODE':27, 'SCAN_SIZE_X':28, 'SCAN_SIZE_Y':29, 'SCAN_ROUT_X':30, 'SCAN_ROUT_Y':31, 'SCAN_POLARITY':32, 'SCAN_FLYBACK':33, 'SCAN_BORDERS':34,
               'PIXEL_TIME':35, 'PIXEL_CLOCK':36, 'LINE_COMPRESSION':37, 'TRIGGER':38, 'EXT_PIXCLK_DIV':39, 'RATE_COUNT_TIME':40, 'MACRO_TIME_CLK':41, 'ADD_SELECT':42,
               'ADC_ZOOM':43, 'XY_GAIN':44, 'IMG_SIZE_X':45, 'IMG_SIZE_Y':46, 'IMG_ROUT_X':47, 'IMG_ROUT_Y':48, 'MASTER_CLOCK':49, 'ADC_SAMPLE_DELAY':50, 'DETECTOR_TYPE':51,
               'X_AXIS_TYPE':52, 'CHAN_ENABLE':53, 'CHAN_SLOPE':54, 'CHAN_SPEC_NO':55}
             
#Error code here?

#Data Structures
class SPCData(ct.Structure):
        _fields_ = [('base_adr', ct.c_ushort), ('init', ct.c_short), ('cfd_limit_low', ct.c_float), 
                    ('cfd_limit_high', ct.c_float), ('cfd_zc_level', ct.c_float), ('cfd_holdoff', ct.c_float),
                    ('sync_zc_level', ct.c_float), ('sync_holdoff', ct.c_float), ('sync_threshold', ct.c_float),
                    ('tac_range', ct.c_float), ('sync_freq_div', ct.c_short), ('tac_gain', ct.c_short),
                    ('tac_offset', ct.c_float), ('tac_limit_low', ct.c_float), ('tac_limit_high', ct.c_float), 
                    ('adc_resolution', ct.c_short), ('ext_latch_delay', ct.c_short), ('collect_time', ct.c_float),
                    ('display_time', ct.c_float), ('repeat_time', ct.c_float), ('stop_on_time', ct.c_short), 
                    ('stop_on_ovfl', ct.c_short), ('dither_range', ct.c_short), ('count_incr', ct.c_short),
                    ('mem_bank', ct.c_short), ('dead_time_comp', ct.c_short), ('scan_control', ct.c_ushort),
                    ('routing_mode', ct.c_short), ('tac_enable_hold', ct.c_float), ('pci_card_no', ct.c_short),
                    ('mode', ct.c_ushort), ('scan_size_x', ct.c_ulong), ('scan_size_y', ct.c_ulong),
                    ('scan_rout_x', ct.c_ulong), ('scan_rout_y', ct.c_ulong), ('scan_flyback', ct.c_ulong),
                    ('scan_borders', ct.c_ulong), ('scan_polarity', ct.c_ushort), ('pixel_clock', ct.c_ushort),
                    ('line_compression', ct.c_ushort), ('trigger', ct.c_ushort), ('pixel_time', ct.c_float),
                    ('ext_pixclk_div', ct.c_ulong), ('rate_count_time', ct.c_float), ('macro_time_clk', ct.c_short),
                    ('add_select', ct.c_short), ('test_eep', ct.c_short), ('adc_zoom', ct.c_short),
                    ('img_size_x', ct.c_ulong), ('img_size_y', ct.c_ulong), ('img_rout_x', ct.c_ulong),
                    ('img_rout_y', ct.c_ulong), ('xy_gain', ct.c_short), ('master_clock', ct.c_short),
                    ('adc_sample_delay', ct.c_short), ('detector_type', ct.c_short), ('chan_enable', ct.c_ulong),
                    ('chan_slope', ct.c_ulong), ('chan_spec_no', ct.c_ulong), ('x_axis_type', ct.c_short)]

class SPCMemConfig(ct.Structure):
     _fields_ = [('max_block_no', ct.c_long), ('blocks_per_frame', ct.c_long), ('frames_per_page', ct.c_long), ('maxpage', ct.c_long), ('block_length', ct.c_long)]

class SPCModInfo(ct.Structure):
     _fields_ = [('module_type', ct.c_short), ('bus_number', ct.c_short), ('slot_number', ct.c_short), ('in_use', ct.c_short), ('init', ct.c_short), ('base_adr', ct.c_ushort)]

class SPCAdjustPara(ct.Structure):
     _fields_ = [('vrt1', ct.c_short), ('vrt2', ct.c_short), ('vrt3', ct.c_short), ('dith_g', ct.c_short), ('gain_1', ct.c_float), ('gain_2', ct.c_float),
                 ('gain_4', ct.c_float), ('gain_8', ct.c_float), ('tac_r0', ct.c_float), ('tac_r1', ct.c_float), ('tac_r2', ct.c_float), ('tac_r4', ct.c_float),
                 ('tac_r8', ct.c_float), ('sync_div', ct.c_short)]

class SPCEEPData(ct.Structure):
     _fields_ = [('module_type', ct.c_char*16), ('serial_no', ct.c_char*16), ('date', ct.c_char*16)]

class PhotStreamInfo(ct.Structure):
     _fields_ = [('fifo_type', ct.c_short), ('stream_type', ct.c_short), ('mt_clock', ct.c_int), ('rout_chan', ct.c_short), ('what_to_read', ct.c_short),
                 ('no_of_files', ct.c_short), ('no_of_ready_files', ct.c_short), ('base_name', ct.c_char*264), ('cur_name', ct.c_char*264), ('first_no', ct.c_short),
                 ('cur_no', ct.c_short), ('fifo_overruns', ct.c_int), ('stream_size', ct.c_uint64), ('cur_stream_offs', ct.c_uint64), ('cur_file_offs', ct.c_uint64),
                 ('invalid_phot', ct.c_uint64), ('read_photons', ct.c_uint64), ('read_0_mark', ct.c_uint64), ('read_1_mark', ct.c_uint64), ('read_2_mark', ct.c_uint64),
                 ('read_3_mark', ct.c_uint64), ('start01_offs', ct.c_uint), ('no_of_buf', ct.c_short), ('no_of_ready_buf', ct.c_short), ('cur_buf_offs', ct.c_uint), 
                 ('start_OR_mask', ct.c_uint), ('start_AND_mask', ct.c_uint), ('stop_OR_mask', ct.c_uint), ('stop_AND_mask', ct.c_uint), ('start_found', ct.c_short),
                 ('stop_reached', ct.c_short), ('start_time', ct.c_double), ('stop_time', ct.c_double), ('curr_time', ct.c_double), ('start_found_chan', ct.c_uint),
                 ('stop_found_chan', ct.c_uint)]

class PhotInfo(ct.Structure):
     _fields_ = [('mtime_lo', ct.c_ulong), ('mtime_hi', ct.c_ulong), ('micro_time', ct.c_ushort), ('rout_chan', ct.c_ushort), ('flags', ct.c_ushort)]

class PhotInfo64(ct.Structure):
     _fields_ = [('mtime', ct.c_uint64), ('micro_time', ct.c_ushort), ('rout_chan', ct.c_ushort), ('flags', ct.c_ushort)]

class InUseTable(ct.Structure):
     _fields_=[('mod_0', ct.c_int), ('mod_1', ct.c_int), ('mod_2', ct.c_int),('mod_3', ct.c_int), ('mod_4', ct.c_int), ('mod_5', ct.c_int),
              ('mod_6', ct.c_int), ('mod_7', ct.c_int)]

class Rates(ct.Structure):
     _fields_ = [('sync_rate', ct.c_float), ('cfd_rate', ct.c_float),
                 ('tac_rate', ct.c_float), ('adc_rate', ct.c_float)]

