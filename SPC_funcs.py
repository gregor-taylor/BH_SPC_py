#Will define other functions here that are not in the main DLL documentation
#If we define all custom funcs here and leave the main SPC_lib.py as per the B&H docs (almost).

#Collection of command-line functions to be proceeded with 'show_', i.e 'show_rates' to quickly print counting rates or other params. As we get more complex with GUIs etc we
#can move away from these but they're always useful for sanity check.

###Imports###
import SPC_lib as BH
import SPC_defs as defs
import numpy as np
import matplotlib.pyplot as plt
import h5py
#######

###Main Class###
class SPC_module(BH.SPC):
    def __init__(self, mod_no, ini_file='C:\Program Files (x86)\BH\SPCM\spcm.ini'):
        super().__init__(mod_no, ini_file)
        #Intialises measurement parameters from ini file to the module
        self.SPC_init(self.ini_file)
        self.get_init_status(self.mod_no)#Checks the init is OK
        if self.last_retcode == 0: #all ok
            mod_name = 'mod_'+str(mod_no)
            setattr(self.in_use, mod_name, ct.c_int(1))#Update in_use table to 1 for initialised ones.
            self.get_parameters(self.mod_no) #reads the parameters back to the 'SPCdata' structure
        else:
            print(defs.Init_Error_Codes[self.last_retcode]) #stop as init failed so check errors

###########################################
#######General Helper funcs################
###########################################

    def modify_parameters(self, parameters_to_update):
        #Takes a list of tuples of the parameter names to update (from SPCData). Use if more than a few paramters but if updating the
        #whole lot better to use set_parameters with a whole new structure of type SPCData. You need to provide the values as the correct c type.
        #parameters_to_update of the form [('tac_range', ct.c_float(50)), ...etc...]
        for i in parameters_to_update:
            setattr(self.SPCdata, i[0], i[1])
        #Then run set_and_check
        self.set_and_check_parameters()

    def set_and_check_parameters(self, mod_no=None):
        if mod_no == None:
            mod_no=self.mod_no
        self.set_parameters(mod_no) #sets the parameters to the SPCData data
        self.get_parameters(mod_no) #reads them back 
        #Add comparison of old data and new?

    def get_parameter_id(self, parameter_name): #Gets the id value of the parameter, can pass to other funcs for setting/getting individual params
    	return defs.Parameter_IDs[parameter_name]

    def set_and_check_parameter(self, par_id, value, mod_no=None): #for single parameter updates
        if mod_no == None:
            mod_no=self.mod_no
        self.set_parameter(mod_no, par_id, value) #set a particular parameter
        self.get_parameter(mod_no, par_id) #Checks the value
        if self.SPC_value.value != value:
            print("%f out of range! Value set to %f"(value, self.SPC_value.value)) 

###########################################
####show functions for command line use####
###########################################

    def print_values(self, ctype_struct): #helper func to print the keys and values of the ctypes structures.
        for field in ctype_struct._fields_:
            print(field[0], getattr(ctype_struct, field[0]))

    def show_module_info(self):
        self.get_module_info(self.mod_no)
        self.print_values(self.mod_info)

    def show_parameters(self):
        self.get_parameters(self.mod_no)
        self.print_values(self.SPCdata)

    def show_eeprom_data(self):
        self.get_eeprom_data(self.mod_no)
        self.print_values(self.eep_data)

    def show_adjust_parameters(self):
        self.get_adjust_parameters(self.mod_no)
        print_values(self.adjpara)

    def show_sync_state(self):
        self.get_sync_state(self.mod_no)
        print(defs.Sync_States[self.sync_state.value])

    def show_break_time(self):
        self.get_break_time(self.mod_no)
        print(self.bh_time.value)

    def show_rates(self):
        self.read_rates(self.mod_no)
        self.print_values(self.rates)

    def show_sequencer_state(self):
        self.get_sequencer_state(self.mod_no)
        print(defs.Sequencer_States[self.state.value])

    def show_gap_time(self):
        self.read_gap_time(self.mod_no)
        print(self.bh_time.value)
    
    def show_scan_clk_state(self):
        self.get_scan_clk_state(self.mod_no)
        print(defs.Scan_Clk_States[self.scan_state.value])

    def show_fifo_usage_degree(self):
        self.get_fifo_usage(self.mod_no)
        print(str(self.usage_degree.value*100)+'%')

    def show_phot_stream_info(self):
        if self.stream_hndl == None:
            print('No stream!')
        else:
            self.get_phot_stream_info(self.stream_hndl)
            self.print_values(self.stream_info)

    def show_photon(self): #Not sure it's wise to use this one as you might end up printing a lot of photon data! Will only print one and then you can loop through.
        if self.stream_hndl == None:
            print('No stream!')
        else:
            self.get_photon(self.stream_hndl)
            self.print_values(self.phot_info)

    def show_fifo_init_vars(self):
        self.get_fifo_init_vars(self.mod_no)
        print(self.fifo_type.value, self.stream_type.value, self.mt_clock.value, self.spc_header.value)

    def show_stream_buffer_size(self, buf_no):
        if self.stream_hndl == None:
            print('No stream!')
        else:
            self.get_stream_buffer_size(self.stream_hndl, buf_no)
            print(self.buf_size.value)

###########################################
###       Measurement functions        ####
###########################################

#Basic measurement sequence as defined in the SPCM_DLL documentation:
# - SPC_init (This is done upon _init_ of the object so OK)
# - SPC_configure_memory >Configures the ADC and routing bits
# - SPC_set_page >where the data will be recorded to
# - SPC_fill_memory >Clears the memory
# - SPC_start_measurement >Starts the measurement loop
# - SPC_test_state is repeatedly called until it returns an SPC_armed=0 indicating the meas is stopped. The stop condition is defined in the measurement params.
# - SPC_read_data_block >read the data.

    def perform_measurement(self, adc_res, no_of_routing_bits, page):
        self.configure_memory(self.mod_no, adc_res, no_of_routing_bits)
        self.set_page(self.mod_no, page) 
        self.fill_memory(self.mod_no, -1, page, 0) #block=-1 clears all blocks
        #Check the clearing is successful
        if self.last_retcode == 0:
            self.start_measurement(self.mod_no)
            self.test_state(self.mod_no)
            while self.state.value == 0x80:
                self.test_state(self.mod_no) #keeps checking
            #Once we exit this loop the reason for exit (success/overflow etc) can be read from self.state with the dict Module_States in SPC_defs.py
            #Read the data out after with read_data_block
        else:
            pass

    def read_data_block_to_np_arr(self, blocks, page, from_point=0, to_point=None, reduction_factor=1 ):
    	#Blocks is a list of block numbers.
    	#Page is the data page (one page is a frame in imaging modes).
    	#reduction_factor is the data reduction factor - averages a given number of points, must be power of 2.
    	#from and to are the first and last point numbers within the block (curve).
    	#Must have called configure_memory before trying to read data so that we have access to the parameters in mem_info.
    	no_of_points=self.mem_info.block_length/reduction_factor
    	if to_point == None:
    		to_point = no_of_points-1
    	curves=np.ndarray(len(blocks), dtype='object') #to hold all of the curves
    	curve_id=0
    	for block in blocks:
    	    self.read_data_block(self.mod_no, block, page, reduction_factor, from_point, to_point) #reads the data to the buffer, self.buf
    	    np_data = np.ctypeslib.asarray(self.buf) #then takes that to an np arr
    	    curves[curve_id]=np_data
    	    curve_id+=1
    	return curves
    	#curves is a numpy array of the returned curves.

    def disp_realtime_curves(self, number_of_curves, save_data=False):
    	#Little test func, take a number of curves and display them as we go
    	#Set the measurements up first.
    	#Setup the canvas
    	plt.ion()
    	fig=plt.figure()
    	ax=fig.add_subplot(111)
    	ax.set_autoscale(True)
    	ax.autoscale_view(True,True,True)
    	line1, =plt.plot([],[],'r-') #blank data
    	plt.xlabel('Bin')
    	plt.ylabel('Counts')

    	if save_data==True:
    		saveFile=h5py.File("TestOutputFile.hdf5", 'w')
    	for m in range(number_of_curves):
    		#get data
    		self.perform_measurement(0, 0, 0)
    		#read data
    		curves=self.read_data_block_to_np_arr([0],0)
    		#plt data
    		lin1.set_ydata(curves[0])
    		axes.relim()
    		ax.autoscale_view(True,True,True)
    		plt.draw()
    		#save data if req
    		if save_data==True:
    			saveFile.create_dataset('curve_{}'.format(m), data=curves[0])

































 
