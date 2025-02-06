
from .constants import SystemType, Interfaces, ChannelType, FeatureList
from devices.models import LibraryDevice, DeviceFeature, LibraryChannel, ChannelParameter, Color




class Feature():
    def __init__(self):
        self.feature_class = ''

    def get_feature_class(self, class_name):
        if class_name == 'DMX_RGB':
            return DMX_RGB()
        elif class_name == 'DMX_DIMM':
            return DMX_DIMM()
        elif class_name == 'DMX_SELECT':
            return DMX_SELECT()
        elif class_name == 'DMX_COLORWHL':
            return DMX_COLORWHL()
        elif class_name == 'DMX_PANTILT':
            return DMX_PANTILT()

    def add_feature(self, feature, name, hide, devicelib_id):
        devicelib_qs = LibraryDevice.objects.get(pk=devicelib_id)
        feature_qs = DeviceFeature.objects.filter(library_device=devicelib_qs).order_by('-sort_order')
        
        feature_class = self.get_feature_class(feature)
        channel_list = feature_class.get_channel_list()

        if feature_qs:
            feature_sort_order = feature_qs[0].sort_order + 1
        else:
            feature_sort_order = 1

        new_feature = DeviceFeature()
        new_feature.name = name
        new_feature.feature_class = feature
        new_feature.library_device = devicelib_qs
        new_feature.sort_order = feature_sort_order
        new_feature.hide = False
        new_feature.save()
        print('Feature:', new_feature)
        channel_sort_order = 1
        for channel in channel_list:
            print('Channel:', channel)
            new_channel = LibraryChannel()
            new_channel.name = channel
            new_channel.channel_type = channel
            new_channel.device_feature = new_feature
            new_channel.sort_order = channel_sort_order
            new_channel.startup_int = 0
            new_channel.save()
            channel_sort_order += 1

    def delete_feature(self, feature_id):
        feature_del_qs = DeviceFeature.objects.get(pk=feature_id)
        lib_dev = feature_del_qs.library_device
        feature_del_qs.delete()
        feature_qs = DeviceFeature.objects.filter(library_device=lib_dev).order_by('sort_order')
        sort_order = 1
        for feature in feature_qs:
            feature.sort_order = sort_order
            feature.save()
            sort_order += 1

    
    def move_feature(self, feature_id, direction):
        feature_qs = DeviceFeature.objects.get(pk=feature_id)
        lib_dev = feature_qs.library_device
        feature_list = DeviceFeature.objects.filter(library_device=lib_dev).order_by('sort_order')
        feature_sort_order = feature_qs.sort_order
        if direction == 'up':
            if feature_sort_order == 1:
                return False
            new_sort = feature_sort_order - 1
        else:
            new_sort = feature_sort_order + 1
            if new_sort > len(feature_list):
                return False
        switch_feature = DeviceFeature.objects.get(library_device=lib_dev, sort_order=new_sort)
        feature_qs.sort_order = new_sort
        switch_feature.sort_order = feature_sort_order    
        switch_feature.save()
        feature_qs.save()
        
        return True
    
    def has_parameters(self, feature):
        feature_class = self.get_feature_class(feature)
        return feature_class.has_parameters()
    
    def get_parameter_fields(self, feature):
        feature_class = self.get_feature_class(feature)
        return feature_class.get_parameter_fields()
    
    def get_parameter_field_display(self, pararmeter_field):
            if pararmeter_field == 'int_min':
                return 'Min'
            elif pararmeter_field == 'int_max':
                return 'Max'
            elif pararmeter_field == 'str_value':
                return 'Value'
            elif pararmeter_field == 'allow_fading':
                return 'Allow Fading'
            elif pararmeter_field == 'color':
                return 'Color'
            else:
                return False

class DMX_RGB():
    #Adds the  R, G, and B Items to a list.  Can be used for display or to create records in the DeviceFeatureItems Model  
    def __init__(self):
        self.class_has_parameters = False
        self.feature_class = 'DMX_RGB'
        self.feature_list = ['RGB-R', 'RGB-G', 'RGB-B']

    def get_channel_list(self):
        return self.feature_list
    
    def has_parameters(self):
        return self.class_has_parameters

    def get_control_widget(self, channel_id):
        pass
    
class DMX_DIMM():
    def __init__(self):
        self.class_has_parameters = False
        self.feature_class = 'DMX_DIMM'
        self.feature_list = ['DIMM']

    def get_channel_list(self):
        return self.feature_list
    
    def has_parameters(self):
        return self.class_has_parameters
    
class DMX_COLORWHL():
    def __init__(self):
        self.class_has_parameters = True
        self.parameter_fields = ['int_min', 'int_max', 'allow_fading', 'color']
        self.feature_class = 'DMX_COLORWHL'
        self.feature_list = ['SELECT']
    
    def get_channel_list(self):
        return self.feature_list
    
    def has_parameters(self):
        return self.class_has_parameters

    def get_parameter_fields(self):
        return self.parameter_fields

    def add_parameter(self, channel_id, value_dict):
        result_dict = {}
        channel_qs = LibraryChannel.objects.get(pk=channel_id)
        try:
            int_min = int(value_dict['int_min'])
        except:
            result_dict['result'] = False
            result_dict['message'] = 'Invalid Min Value'
            return result_dict
        else:
            if int_min < 0 or int_min > 255:
                result_dict['result'] = False
                result_dict['message'] = 'Min must be between 0 and 255'
                return result_dict
        try:
            int_max = int(value_dict['int_max'])
        except:
            result_dict['result'] = False
            result_dict['message'] = 'Invalid Max Value'
            return result_dict
        else:
            if int_max < 0 or int_max > 255:
                result_dict['result'] = False
                result_dict['message'] = 'Max must be between 0 and 255'
                return result_dict
        allow_fading = value_dict['allow_fading']
       
        if value_dict['name'] == '':
            result_dict['result'] = False
            result_dict['message'] = 'Name is required'
            return result_dict
        else:
            name = value_dict['name']
        
        color_id = int(value_dict['color'])
        if color_id != 0:
            color_obj = Color.objects.get(pk=color_id)
        else:
            color_obj = None

        new_parameter = ChannelParameter()
        new_parameter.name = name
        new_parameter.library_channel = channel_qs
        new_parameter.int_min = int_min
        new_parameter.int_max = int_max
        new_parameter.allow_fading = allow_fading
        new_parameter.color = color_obj
        new_parameter.save() 

        result_dict['result'] = True
        result_dict['message'] = 'Parameter Added'
        return result_dict
    
    def edit_parameter(self, parameter_id, value_dict):
        result_dict = {}
        parameter_qs = ChannelParameter.objects.get(pk=parameter_id)
        try:
            int_min = int(value_dict['int_min'])
        except:
            result_dict['result'] = False
            result_dict['message'] = 'Invalid Min Value'
            return result_dict
        else:
            if int_min < 0 or int_min > 255:
                result_dict['result'] = False
                result_dict['message'] = 'Min must be between 0 and 255'
                return result_dict
        try:
            int_max = int(value_dict['int_max'])
        except:
            result_dict['result'] = False
            result_dict['message'] = 'Invalid Max Value'
            return result_dict
        else:
            if int_max < 0 or int_max > 255:
                result_dict['result'] = False
                result_dict['message'] = 'Max must be between 0 and 255'
                return result_dict
        allow_fading = value_dict['allow_fading']
       
        if value_dict['name'] == '':
            result_dict['result'] = False
            result_dict['message'] = 'Name is required'
            return result_dict
        else:
            name = value_dict['name']

        color_id = int(value_dict['color'])
        if color_id != 0:
            color_obj = Color.objects.get(pk=color_id)
        else:
            color_obj = None

        parameter_qs.name = name
        parameter_qs.int_min = int_min
        parameter_qs.int_max = int_max
        parameter_qs.allow_fading = allow_fading
        parameter_qs.color = color_obj
        parameter_qs.save()
        result_dict['result'] = True
        result_dict['message'] = 'Parameter Updated'
        return result_dict

class DMX_PANTILT():
    def __init__(self):
        self.class_has_parameters = False
        self.feature_class = 'DMX_PANTILT'
        self.feature_list = ['PAN', 'TILT']

    def get_channel_list(self):
        return self.feature_list
    
    def has_parameters(self):
        return self.class_has_parameters

class DMX_SELECT():
    def __init__(self):
        self.class_has_parameters = True
        self.parameter_fields = ['int_min', 'int_max', 'allow_fading']
        self.feature_class = 'DMX_SELECT'
        self.feature_list = ['SELECT']
    
    def get_channel_list(self):
        return self.feature_list
    
    def has_parameters(self):
        return self.class_has_parameters

    def get_parameter_fields(self):
        return self.parameter_fields

    def add_parameter(self, channel_id, value_dict):
        result_dict = {}
        channel_qs = LibraryChannel.objects.get(pk=channel_id)
        try:
            int_min = int(value_dict['int_min'])
        except:
            result_dict['result'] = False
            result_dict['message'] = 'Invalid Min Value'
            return result_dict
        else:
            if int_min < 0 or int_min > 255:
                result_dict['result'] = False
                result_dict['message'] = 'Min must be between 0 and 255'
                return result_dict
        try:
            int_max = int(value_dict['int_max'])
        except:
            result_dict['result'] = False
            result_dict['message'] = 'Invalid Max Value'
            return result_dict
        else:
            if int_max < 0 or int_max > 255:
                result_dict['result'] = False
                result_dict['message'] = 'Max must be between 0 and 255'
                return result_dict
        allow_fading = value_dict['allow_fading']
       
        if value_dict['name'] == '':
            result_dict['result'] = False
            result_dict['message'] = 'Name is required'
            return result_dict
        else:
            name = value_dict['name']
        
        

        new_parameter = ChannelParameter()
        new_parameter.name = name
        new_parameter.library_channel = channel_qs
        new_parameter.int_min = int_min
        new_parameter.int_max = int_max
        new_parameter.allow_fading = allow_fading
        new_parameter.save() 

        result_dict['result'] = True
        result_dict['message'] = 'Parameter Added'
        return result_dict
    
    def edit_parameter(self, parameter_id, value_dict):
        result_dict = {}
        parameter_qs = ChannelParameter.objects.get(pk=parameter_id)
        try:
            int_min = int(value_dict['int_min'])
        except:
            result_dict['result'] = False
            result_dict['message'] = 'Invalid Min Value'
            return result_dict
        else:
            if int_min < 0 or int_min > 255:
                result_dict['result'] = False
                result_dict['message'] = 'Min must be between 0 and 255'
                return result_dict
        try:
            int_max = int(value_dict['int_max'])
        except:
            result_dict['result'] = False
            result_dict['message'] = 'Invalid Max Value'
            return result_dict
        else:
            if int_max < 0 or int_max > 255:
                result_dict['result'] = False
                result_dict['message'] = 'Max must be between 0 and 255'
                return result_dict
        allow_fading = value_dict['allow_fading']
       
        if value_dict['name'] == '':
            result_dict['result'] = False
            result_dict['message'] = 'Name is required'
            return result_dict
        else:
            name = value_dict['name']

        parameter_qs.name = name
        parameter_qs.int_min = int_min
        parameter_qs.int_max = int_max
        parameter_qs.allow_fading = allow_fading
        parameter_qs.save()
        result_dict['result'] = True
        result_dict['message'] = 'Parameter Updated'
        return result_dict