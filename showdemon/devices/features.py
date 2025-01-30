from devices.colors import Colors
from .constants import SystemType, Interfaces, ChannelType, FeatureList
from devices.models import LibraryDevice, DeviceFeature, LibraryChannel


class Feature():
    def __init__(self):
        self.feature_class = ''

    #FCL has two lists, the first is the feature list of dicts, the second is the channel list of dicts
    def feature_channel_list_add(self, feature_channel_list, feature, name ):
        print('Feature:', feature_channel_list, feature, name)  
        feature_type = FeatureList()
        if feature == 'DMX_RGB':
            dmx_rgb = DMX_RGB()
            channel = dmx_rgb.get_channel_list()
            display = feature_type.get_display(feature)
        elif feature == 'DMX_DIMM':
            dmx_dimm = DMX_DIMM()
            channel = dmx_dimm.get_channel_list()
            display = feature_type.get_display(feature)

        feature_sort_order = 1
        channel_sort_order_start = 1
        if  feature_channel_list == []:
            feature_list = []
            channel_list = []
        else:
            feature_list = feature_channel_list[0]
            channel_list = feature_channel_list[1]
            feature_sort_order = 1
            for feature_dict in feature_list:
                if feature_dict['sort_order'] >= feature_sort_order:
                    feature_sort_order = feature_dict['sort_order'] + 1
           
        feature_dict = {
            'feature': feature,
            'display': display,
            'name': name,
            'sort_order': feature_sort_order,
            'feature_id': 0,
            'channel_count': len(channel),
        }
        feature_list.append(feature_dict)
        feature_channel_list.append(feature_list)

        channel_type = ChannelType()
        
        for item in channel:
            print('Item:', item)
            channel_number = channel_sort_order_start + channel.index(item)
            feature_dict = {
                'channel_type': item,
                'display': channel_type.get_display(item),
                'name': item,
                'parent_sort_order': feature_sort_order,
                'sort_order': channel_number,
                'channel_id': 0,
            }
            channel_list.append(feature_dict)

        feature_channel_list.append(channel_list)
        return feature_channel_list

    def add_feature(self, feature, name, devicelib_id):
        devicelib_qs = LibraryDevice.objects.get(pk=devicelib_id)
        feature_qs = DeviceFeature.objects.filter(library_device=devicelib_qs).order_by('-sort_order')
        
        if feature == 'DMX_RGB':
            dmx_rgb = DMX_RGB()
            channel_list = dmx_rgb.get_channel_list()
        elif feature == 'DMX_DIMM':
            dmx_dimm = DMX_DIMM()
            channel_list = dmx_dimm.get_channel_list()
            
        if feature_qs:
            feature_sort_order = feature_qs[0].sort_order + 1
        else:
            feature_sort_order = 1

        new_feature = DeviceFeature()
        new_feature.name = name
        new_feature.feature_class = feature
        new_feature.library_device = devicelib_qs
        new_feature.sort_order = feature_sort_order
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


            


class DMX_RGB():
    #Adds the  R, G, and B Items to a list.  Can be used for display or to create records in the DeviceFeatureItems Model  
    def __init__(self):
        self.feature_class = 'DMX_RGB'
        self.feature_list = ['RGB-R', 'RGB-G', 'RGB-B']

    def get_channel_list(self):
        return self.feature_list
    
class DMX_DIMM():
    def __init__(self):
        self.feature_class = 'DMX_DIMM'
        self.feature_list = ['DIMM']

    def get_channel_list(self):
        return self.feature_list