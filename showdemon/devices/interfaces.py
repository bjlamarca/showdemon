import time
import random
import threading, multiprocessing
from pyftdi.ftdi import Ftdi




class DMXInterface:
    _instance = None
    url='ftdi://ftdi:232:AQ01UKYW/1'
    is_connected = False
    is_running = False
    port = None
    data = None
    run_loop = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        
        return cls._instance


    def connect(cls):
        if cls.is_connected:
            return True
        else:
            try:
                cls.port = Ftdi.create_from_url(cls.url)
                cls.port.reset()
                cls.port.set_baudrate(baudrate=250000)
                cls.port.set_line_property(bits=8, stopbit=2, parity='N', break_=False)
                # The 0th byte must be 0 (start code)
                # 513 bytes are sent in total
                cls.data = bytearray(513 * [0])
                cls.is_connected = True
                return True
            except Exception as e:
                print("Error in connect", e)
                cls.is_connected = False
                if cls.port:
                    cls.port.close()
                cls.port = None
                return False

        #self.devices = []
    
    def disconnect(cls):
        if cls.is_connected:
            if cls.port:
                cls.port.close()
            cls.port = None
            cls.is_connected = False

    def __del__(cls):
        print("Close DMX")
        if cls.port:
            cls.port.close()

    def update(cls, channel, value):
        cls.data[channel] = value
        
    def loop_dmx(cls):
        try:
            while cls.run_loop:
                cls.port.set_break(True)
                cls.port.set_break(False)
                cls.port.write_data(cls.data)
                time.sleep(8/1000.0)
        except:
            print("Error in loop")
            cls.run_loop = False
            cls.is_running == False
            if cls.port:
                cls.port.close()
            cls.port = None
            cls.is_connected = False        
        

    def start_dmx(cls):
        if not cls.is_connected:
            if cls.connect():
                return 'DMX Connected'
            else:
                return 'DMX Connection Failed'
            
        if not cls.is_running:
            cls.run_loop = True    
            print("Start DMX")
            process = threading.Thread(target=cls.loop_dmx)
            process.daemon = True
            process.start()
            cls.is_running = True
            return 'DMX Started'
        else:
            return 'DMX Already Started'

    def stop_dmx(cls):
        if cls.is_running:
            cls.run_loop = False
            cls.is_running = False
            cls.disconnect()
            return 'DMX Stopped'
        else:
            return 'DMX Already Stopped'
        



