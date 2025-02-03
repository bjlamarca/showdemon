from .models import Device, Channel, LibraryDevice, DeviceFeature, LibraryChannel

class DMX:
    def __init__(self):
        self.channel_list = [str(i) for i in range(1, 513)]
        
    def get_channel_list(self):
        channel_list_qs = Channel.objects.all(library_channel__device_feature__system='DMX')
        
        return self.channel_list
    
    def get_lib_dev_channel_count(self, lib_dev_id):
        chnl_count = 0
        lib_dev = LibraryDevice.objects.get(pk=int(lib_dev_id))
        lib_dev_features_qs = DeviceFeature.objects.filter(library_device=lib_dev)
        for feature in lib_dev_features_qs:
            chnl_count += LibraryChannel.objects.filter(device_feature=feature).count()       
        
        return chnl_count
    
    def next_start_channel(self, chnl_count):
        channel_qs = Channel.objects.filter(library_channel__device_feature__library_device__system='DMX').order_by('channel_number')
        if channel_qs:
            chnl_range = range(1, 512)
            for chnl in chnl_range:
                if not channel_qs.filter(system_channel=chnl):
                    chnl_ok = True
                    for i in range(chnl, chnl + chnl_count):
                        if channel_qs.filter(system_channel=i):
                            chnl_ok = False
                            break
                    if chnl_ok:
                        return chnl 
            
        else:
            return 1
    #edit assumes the current device channesls will be deleted and new ones created
    def check_start_channel(self, start_channel, chnl_count, edit=False, device_id=None):
        if edit==True:
            device= Device.objects.get(pk=device_id)
            channel_qs = Channel.objects.filter(library_channel__device_feature__library_device__system='DMX').exclude(device=device).order_by('channel_number')
        else:
            channel_qs = Channel.objects.filter(library_channel__device_feature__library_device__system='DMX').order_by('channel_number')
        if channel_qs:
            chnl_range = range(start_channel, start_channel + chnl_count)
            for chnl in chnl_range:
                if channel_qs.filter(system_channel=chnl):
                    return False
            return True
        else:
            return True
        
    def get_start_channel(self, device_id):
        device = Device.objects.get(pk=device_id)
        channel_qs = Channel.objects.filter(device=device).order_by('system_channel').first()
        return channel_qs.system_channel
        
    def add_device(self, dev_lib_id, name, start_channel):
        result_dict = {}
        chnl_count = self.get_lib_dev_channel_count(dev_lib_id)
        if not self.check_start_channel(start_channel, chnl_count):
            result_dict['result'] = False
            result_dict['message'] = 'Invalid Start Channel'
            return result_dict
        lib_dev = LibraryDevice.objects.get(pk=dev_lib_id)
        dev = Device()
        dev.name = name
        dev.device_library = lib_dev
        dev.save()
        feature_list_qs = DeviceFeature.objects.filter(library_device=lib_dev).order_by('sort_order')
        channel_num = 1
        system_channel = start_channel
        for feature in feature_list_qs:
            lib_channel_qs = LibraryChannel.objects.filter(device_feature=feature).order_by('sort_order')
            for lib_chnl in lib_channel_qs:
                new_chnl = Channel()
                new_chnl.device = dev
                new_chnl.library_channel = lib_chnl
                new_chnl.channel_number = channel_num
                new_chnl.system_channel = system_channel
                new_chnl.int_value = 0
                new_chnl.save()
                channel_num += 1
                system_channel += 1
        result_dict['result'] = True
        result_dict['message'] = 'Device Added'
        return result_dict
    
    def delete_device(self, dev_id):
        result_dict = {}
        try:
            dev = Device.objects.get(pk=dev_id)
            dev.delete()
        except Exception as e:
            if type(e).__name__ == 'ProtectedError':
                result_dict['result'] = False
                result_dict['message'] = 'IDevice is in use and cannot be deleted'
                return result_dict
            else:
                result_dict['result'] = False
                result_dict['message'] = 'Error Deleting Device'
                return result_dict
        else:
            result_dict['result'] = True
            result_dict['message'] = 'Device Deleted'
            return result_dict

    def edit_device(self, dev_id, name, start_channel):
        result_dict = {}
        device = Device.objects.get(pk=dev_id)
        dev_lib_id = device.device_library.pk
        if not self.check_start_channel(start_channel, self.get_lib_dev_channel_count(dev_lib_id), edit=True, device_id=dev_id):
            result_dict['result'] = False
            result_dict['message'] = 'Invalid Start Channel'
            return result_dict
        device.name = name
        device.save()
        channel_qs = Channel.objects.filter(device=device).order_by('system_channel')
        for channel in channel_qs:
            channel.system_channel = start_channel
            channel.save()
            start_channel += 1
        result_dict['result'] = True
        result_dict['message'] = 'Device Edited'
        return result_dict
