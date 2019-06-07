# -*- coding: utf-8 -*-
"""
Created on Tue May 14 23:52:43 2019



Examples:
>>> com = '//dev//ttyUSB0' 
>>> iga = IGA6(com)
>>> iga._query('sn')
'01406'
>>> iga._query('la1')
'ok'



TODO:
* don't hard code device_address variable - find better solution
* calling ser.read(1) without an output present at pyrometer causes 
command line to freeze
* change write() to _query()
* implement verbose in query()
* implement port_settings dictionary ...
* read back string seems to have a different structure on linux than
on windows. Example: sending '00sn\r\n' on windows -> '01406\r';
on linux -> '00sn\r\n01406\r'
need to fix that
* get_temperature returns 'no' if underrange. not so nice. maybe change that
* finish implementation of PORT_SETTINGS as class variable dictionary. (not complete)
* implement possibility to set values to in setter functions (e.g. set emissivity)
* _get_short_cmd() function does not work properly!!
	example: when entering 'measuring value' it returns 'measuring value' this 
	is because 'measuring value'[2:] is in IGA6_CMD_TABLE.values()
* implement safetz warning when temperature is readout too early after turning on


"""
__version__ = "0.0.1"
__author__ = "kha"



import serial
import time
import sys




IGA6_CMD_TABLE = {
    'analog output':        'as',
    'reference number':     'bn',
    'baudrate':             'br',
    'emissivity':           'em',
    'transmittance':        'et',
    'response time':        'ez',
    'temp display':         'fh',
    'device address':       'ga',
    'internal temperature':  'gt',
    'laser':                'la',
    'software sim':         'lx',
    'clear peak memory':    'lz',
    'basic range':          'mb',
    'sub range read':       'me',
    'sub range 1':          'm1',
    'sub range 2':          'm2',
    'measuring value':      'ms',
    'device type':          'na',
    'read parameter':       'pa',
    'serial number':        'sn',
    'device type':          've',
    'communication module': 'vc',
    'sw version in detail': 'vs'
}


class IGA6Exception(Exception):
    """ """
    pass


class IGA6(object):
    """ """

    PORT_SETTINGS = {
        'baudrate':     19200,
        'bytesize':     serial.EIGHTBITS,
        'parity':       serial.PARITY_EVEN,
        'stopbits':     serial.STOPBITS_ONE,
        'timeout':      None,
        'rtscts':       False,
        'dsrdtr':       False
    }
    
    BAUDRATE = 19200
    BYTESIZE = serial.EIGHTBITS
    STOPBITS = serial.STOPBITS_ONE
    PARITY = serial.PARITY_EVEN
    
    WRITE_RESPONSE_TIME   = 0.005     # [s]
    READ_RESPONSE_TIME    = 0.0015    # [s]

    CR = "\r\n"
    RTN_BYTE = b'\r'

    DEFAULT_DEVICE_ADDRESS = '00'

    def __init__(self, port= None, device_address = None):
        
        self.ser = serial.Serial()
        self.ser.baudrate = IGA6.BAUDRATE
        self.ser.bytesize = IGA6.BYTESIZE
        self.ser.stopbits = IGA6.STOPBITS
        self.ser.parity = IGA6.PARITY
        self.ser.rtscts = 0
        
        self.cr = IGA6.CR
        self.rtn_byte = IGA6.RTN_BYTE
        self.write_resp_time = IGA6.WRITE_RESPONSE_TIME
        self.read_resp_time = IGA6.READ_RESPONSE_TIME

        if device_address is None:
            device_address = IGA6.DEFAULT_DEVICE_ADDRESS
        self.device_address = device_address
        self.cmd_table = IGA6_CMD_TABLE

        if port is not None:
            self.ser.port = port
            self._open()
    
    
    def _open(self):
        if not self.ser.isOpen():
            self.ser.open()
            if not self.ser.isOpen():
                raise IGA6Exception('Failed to open port')
        else:  
            raise IGA6Exception('Port already open')
            
    def _close(self):
        if self.ser.isOpen():
            self.ser.close()
        else:
            raise IGA6Excpetion('Port already closed')

    def is_open(self):
        """returns True if serial port is open"""
        return self.isOpen()
            
    def _write(self, cmd, verbose=False):
        """cmd must be two-character command letter"""
        cmd = ''.join([self.device_address,cmd,self.cr])
        if verbose:
            print('write...\n' + repr('    cmd: {}'.format(cmd)))
        self.ser.write(cmd.encode('utf-8'))
        time.sleep(self.write_resp_time)
        return
        
    def _read(self, verbose=False):
        """ 

        Needed to include additional while-loop because read back on linux
        seems to be different than on windows.

        """
        if verbose: print('read...')
        rtn = ''
        msg = []
        cmd = []

        if sys.platform == 'linux':
            while rtn != self.rtn_byte:
                rtn = self.ser.read(1)
                cmd.append(rtn.decode('utf-8'))
            rtn = self.ser.read(1)
            cmd.append(rtn.decode('utf-8'))
            if verbose: print(repr('    cmd: {}'.format(''.join(cmd))))

        rtn = ''
        while rtn != self.rtn_byte:
            rtn = self.ser.read(1)
            msg.append(rtn.decode('utf-8'))
        if verbose: print(repr('    msg: {}'.format(''.join(msg))))
        time.sleep(self.read_resp_time)
        return ''.join(msg[:-1])
        
    def _check_cmd(self, cmd):
        """raises error if cmd is not a valid command"""
        if cmd not in self.cmd_table.keys():
            raise IGA6Exception('{} is not a valid command'.format(cmd))
        return
        
    def _get_short_cmd(self, cmd):
        """checks if cmd is valid command and returns two-character command"""
        if cmd[:2] not in self.cmd_table.values():
            if cmd not in self.cmd_table.keys():
               raise IGA6Exception('{} is not a valid command'.format(cmd))
            else:
                cmd = self.cmd_table[cmd]
        return cmd
        
    def _query(self, cmd):
        """ """
        cmd = self._get_short_cmd(cmd)
        self._write(cmd)
        return self._read()

    def get_temperature(self):
        temp = self._query('ms')
#        if temp == 'no': temp = 0
        return int(temp)/10.

    def laser_on(self):
        self._query('la1')

    def laser_off(self):
        self._query('la0')





#iga = IGA6('com16')
#iga._query('sn')        # returns device serial number
#iga._query('la1')       # switches laser on
#iga._query('la')        # returns laser on/off status
#iga._query('la0')       # switches laser off
   
        
