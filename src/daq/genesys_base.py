# -*- coding: utf-8 -*-
"""
Base class representation of the TDK-Lambda Genesys 750W / 1500W power supply. 

Commanication commands and procedure implemented in this code is based on the description given in the 
Genesys USER MANUAL. 

The user manual can be found under this link:
https://www.us.tdk-lambda.com/hp/product_html/genesys1u.htm



"""

__version__ = "0.0.1"
__author__ = "kha"



import serial
import time


# ============================================================================
# Commands
# ============================================================================


_INIT_CMD = {
    'address':                  'ADR',
    'clear_status':             'CLS',
    'reset':                    'RST',
    'remote_mode':              'RMT',
    'multi-drop_option':        'MDAV',
    'master-slave':             'MS'
}

_ID_CMD = {
    'identification':           'IDN',
    'software_version':         'REV',
    'serial_number':            'SN',
    'date_of_last_test':        'DATE'
}

_OUTPUT_CMD = {
    'set_voltage':              'PV',
    'voltage':                  'MV',
    'set_current':              'PC',
    'current':                  'MC',
    'operation_mode':           'MODE',
    'display_V_n_C':            'DVC',
    'power_supply_status':      'STT',
    'adc_filter':               'FILTER',
    'output_mode':              'OUT',
    'foldback_protection':      'FLD',
    'foldback_delay':           'FLB',
    'reset_foldback_delay':     'RSTFLB',
    'over_voltage_protection':  'OVP',
    'ovp_maximum':              'OVM',
    'under_voltage_limit':      'UVL',
    'auto_restart_mode':        'AST',
    'save_settings':            'SAV',
    'recall_last_settings':     'RCL'
}

OUTPUT_MODE = ['0', '1']


# ============================================================================
# Exception Calss
# ============================================================================
class GenesysBaseException(Exception):
    """ """
    pass


# ============================================================================
# Genesys base class
# ============================================================================
class GenesysBase(object):
    """ """

    PORT_SETTINGS = {
        'baudrate':     9600,
        'bytesize':     serial.EIGHTBITS,
        'parity':       serial.PARITY_NONE,
        'stopbits':     serial.STOPBITS_ONE,
        'timeout':      None,
        'rtscts':       False,
        'dsrdtr':       False
    }
    
    PROTOCOL_SETTINGS = {
        'cr':                       "\r",
        'rtn_byte':                 b'\r',
        'default_device_address':   6,
        'write_resp_time':          0.050,      # [s]
        'read_resp_time':           0.050       # [s]
    }
    

    # WRITE_RESPONSE_TIME   = 0.005     # [s]
    # READ_RESPONSE_TIME    = 0.0015    # [s]


    def __init__(self, port= None, device_address = None):
        
        self.ser = self._init_ser()
        
        for key, value in self.PROTOCOL_SETTINGS.items():
            setattr(self, key, value)
        
#        self.cmd_table = self._compile_cmd_table()
        
        if device_address is None:
            device_address = self.default_device_address
        self.device_address = device_address

        if port is not None:
            self.ser.port = port
            self._open()
        
        self.device_is_initialized = False
        if self.is_open() and not self.device_is_initialized:
            self._init_device()   

    def __enter__(self):
        """ """
        if not self.device_is_initialized:
            self._init_device()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """ """
        if self.ser.isOpen():
            self._close()
    
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, traceback)
        return True

    def _init_ser(self):
        """initializes pyserial.Serial object with PORT_SETTINGS"""
        ser = serial.Serial()
        for key, value in self.PORT_SETTINGS.items():
            setattr(ser, key, value)
        return ser

    def _init_device(self):
        """ """
        self.send_address()
        self.device_is_initialized = True
        self.set_output_on()
        return 
    
#    def _compile_cmd_table(self):
#        """defines which commands are part of returned command table"""
#        return {**_INIT_CMD, **_ID_CMD, **_OUTPUT_CMD}



# === serial communication ====================================================
    
    def _open(self):
        if not self.ser.isOpen():
            self.ser.open()
            if not self.ser.isOpen():
                raise GenesysBaseException('Failed to open port')
        else:  
            raise GenesysBaseException('Port already open')
    
    def _close(self):
        if self.ser.isOpen():
            self.ser.close()
            
        else:
            raise GenesysBaseExcpetion('Port already closed')
       
    def is_open(self):
        """returns True if serial port is open"""
        return self.ser.isOpen()
            
    def _write(self, cmd, verbose=False):
        """sends cmd to hardware
        
        cmd needs to be in a shape which can be understand by the hardware. 
        
        """
        if cmd[-len(self.cr):] is not self.cr:
            cmd = ''.join([cmd,self.cr])    
        
        if verbose:
            print('write...\n' + repr('    cmd: {}'.format(cmd)))
        rtn = self.ser.write(cmd.encode('utf-8'))
        time.sleep(self.write_resp_time)
        return rtn    

    def _read(self, verbose=False):
        """reads back string from device"""
        if verbose: print('read...')
        rtn = ''
        msg = []

        while rtn != self.rtn_byte:
            rtn = self.ser.read(1)
            msg.append(rtn.decode('utf-8'))
        if verbose: print(repr('    msg: {}'.format(''.join(msg))))
        time.sleep(self.read_resp_time)
        return ''.join(msg[:-1])

    def _query(self, cmd, verbose=False):
        """ """
        # cmd = self._get_short_cmd(cmd)
        self._write(cmd, verbose=verbose)
        return self._read(verbose=verbose)
    
    def set_value(self, cmd_str, val, **kwargs):
        """specifies syntax for set commands"""
        cmd = ''.join([cmd_str, ' ', str(val)])
        self._query(cmd, **kwargs)
        
    def get_value(self, cmd_str, **kwargs):
        """specifies syntax for get commands"""
        cmd = ''.join([cmd_str, '?'])
        return self._query(cmd, **kwargs)


# === high-level commands ====================================================
    
    def send_address(self):
        self.set_value('ADR', self.device_address)

    def get_set_point_voltage(self):
        return self.get_value('PV')
    
    def get_set_point_current(self):
        return self.get_value('PC')
 
    def get_current(self):
        return self.get_value('MC')
    
    def get_voltage(self):
        return self.get_value('MV')
    
    def set_voltage(self, voltage):
        self.set_value('PV', voltage)
    
    def set_current(self, current):
        self.set_value('CV', current)
    
    def set_output_mode(self, output_mode):
        self.set_value('OUT', output_mode)

    def set_output_on(self):
        self.set_output_mode(1)
        
    def set_output_off(self):
        self.set_output_mode(0)
    
    def get_output_mode(self):
        return self.get_value('OUT')
    
    def set_over_voltage_protection(self, voltage):
        self.set_value('OVP', voltage)
        
    def get_over_voltage_protection(self):
        return self.get_value('OVP')
    
    def get_model_id(self):
        return self.get_value('IDN')
    
    def get_software_version(self):
        return self.get_value('REV')
    
    def get_serial_number(self):
        return self.get_value('SN')
    
    def get_last_test_date(self):
        return self.get_value('DATE')
    
    

# ============================================================================
# Genesys Models
# ============================================================================
class Genesys_20_75(GenesysBase):
    """ """ 
    MAX_VOLTAGE = 20    # [V]
    MAX_CURRENT = 75    # [A]




