import mido
#import rtmidi
import threading

#print(mido.get_input_names())
#print(mido.get_output_names())


class Midi:
    instance = None
    inport = None
    outport = None
    is_connected = False
    is_listening = False
    run_listen = False


    def __new__(cls):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            
        return cls.instance
    
    
    def connect(cls):
        if cls.is_connected:
            return True
        else:
            try:
                cls.inport = mido.open_input('Command|8 0')
                cls.outport = mido.open_output('Command|8 1')
                
                cls.is_connected = True
                print('Midi Connected')
                return True
            except Exception as e:
                print(e)
                cls.is_connected = False
                return False

   

    def send_message(cls, msg):
        cls.outport.send(mido.Message.from_str(msg))

    def listen(cls):
        try:
            while cls.run_listen:
                for msg in cls.inport.iter_pending():
                    print(msg)
        except:
            print("Eror in listen")

    def start_listen(cls):
        if not cls.is_listening:
            cls.run_listen = True
            process = threading.Thread(target=cls.listen)
            process.daemon = True
            process.start()
            cls.is_listening = True
            return 'Midi Listening Started'
        else:
            return 'Midi Listening Already Started'
        
    def stop_listen(cls):
        cls.run_listen = False
        cls.is_listening = False
        cls.inport.close()
        return 'Midi Listening Stopped'


#inport = mido.open_input('Command|8 0')
#Command|8 1'
#msg = 'control_change channel=0 control=7 value=34 time=0'
# outport = mido.open_output('Command|8 1')
# outport.send(mido.Message.from_str(msg))

# for msg in inport:
#     print(msg) #, msg.type, msg.channel, msg.value)

# try:
#     # Your code that might take a long time or run indefinitely
#     for msg in inport:
#         print(msg)

# except KeyboardInterrupt:
#     print("Ctrl+C pressed. Exiting gracefully.")