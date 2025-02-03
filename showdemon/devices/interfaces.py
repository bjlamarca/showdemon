import time
import random
import threading, multiprocessing
from pyftdi.ftdi import Ftdi
from showdemon.threads import ThreadTracker
from devices.models import Channel

import uuid




class DMXInterface:
    _instance = None
    url='ftdi://ftdi:232:AQ01UKYW/1'
    is_connected = False
    is_running = False
    send_to_interface = True
    port = None
    process_data_list = []
    process_data_list_id = 0
    data = None
    run_loop = False


    

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        
        return cls._instance

    def __init__(cls):
        cls.uuid = uuid.uuid4()
        #thread_tracker = ThreadTracker()
        #thread_tracker.start_thread(cls.loop_process_updates, 'DMX_PROCESS_UPDATES')
        



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
    
    def set_channel_value(cls, channel, value):
        if cls.is_running and cls.send_to_interface:
            cls.data[channel] = value
            print("Set Channel Value", channel, value)
        cls.process_data_list_id += 1
        cls.process_data_list.append([cls.process_data_list_id, channel, value])
                
    #a thread, after updating the interface, update the db, and send a signal 
    def loop_process_updates(cls):
        while True:
            process_list = cls.process_data_list
            for process in process_list:
                channel_qs = Channel.objects.filter(library_channel__device_feature__library_device__system='DMX', system_channel=process[1])
                if channel_qs:
                    channel = channel_qs[0]
                    channel.int_value = process[2]
                    channel.save()
                cls.process_data_list.remove(process)
                



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

        print("Start DMX")
        if not cls.is_connected:
            if cls.connect():
                pass
                #return 'DMX Connected'
            else:
                return 'DMX Connection Failed'
            
        if not cls.is_running:
            cls.run_loop = True    
            print("Start DMX")
            thread_tracker = ThreadTracker()
            thread_tracker.start_thread(cls.loop_dmx, 'DMX_INTERFACE')
            
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
        

    def start_process_lookup(cls):
        thread_tracker = ThreadTracker()
        thread_tracker.start_thread(cls.loop_process_updates, 'DMX_PROCESS_UPDATES')
        



