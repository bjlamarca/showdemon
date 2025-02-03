from django.dispatch import Signal, receiver
import json
from devices.interfaces import DMXInterface



device_update = Signal()




dmx_signal = Signal()
@receiver(dmx_signal)
def handle_device_signal(sender, **kwargs):
    dmx_interface = DMXInterface()
    data = kwargs.get('data_dict') 
    #print('Sender', sender, 'Signal:', data)
    if sender != 'DMX-INTERFACE':
        channel = data['channel']
        value = data['value']
        dmx_interface.set_channel_value(channel, value)
        data['requester'] = sender
        dmx_signal.send(sender='DMX-INTERFACE', data_dict=data)
        
    
    
    #     
    # if data['type'] == 'update':
    #     channel_num = str(data['channel_num'])
    #     channel_value = str(data['channel_value'])
    #     send_dict = json.dumps({'type': 'update', 'channel_num': channel_num, 'channel_value': channel_value, 'sender': sender})
        

    

