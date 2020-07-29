# Beckr-Hickl_SPC_for_Python
Wrappings of the SPC DLLs for Beckr and Hickl SPC cards.</br>

Code is organised into three files:</br>
- SPC_lib.py is the wrapping of all of the Becker and Hickl C functions into python using ctypes. Convention is the leading 'SPC_' is removed form the function name (with the exception of the init function) but other than that they follow as per the documentation available [here](https://www.becker-hickl.com/wp-content/uploads/2018/12/opm-SPCM-DLL.pdf).</br>
- SPC_defs.py is the definition file for all of the memory structures, error codes and general definitions. Mostly taken from the Spcm_def.h file.</br>
- SPC_funcs.py is where all of the functionality will be built. Here the functions in SPC_lib.py are grouped and formatted to carry out the operations needed for single photon counting applciations. These will be documented seperately.</br>
