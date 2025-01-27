from devices.colors import Colors

#(Name, Display, Feature Type )
class FeatureList():
    FEATURE_LIST = (
        ('RGB','RGB'),
        ('DIMM', 'Dimmer'),
        ('COLORWHL', 'Color Wheel'),
        ('GOBOWHL', 'Gobo Wheel'),
        ('SELECT', 'Selector')
    )

    def __iter__(self):
        return iter(self.FEATURE_LIST)
    
class ChannelType():
    CHANNEL_TYPE_LIST = (
        ('DIMM', 'Dimmer'),
        ('RGB-R','RGB Red'),
        ('RGB-G','RGB Green'),
        ('RGB-B','RGB Blue'),
        ('SELECT','Selector'),
        ('PAN', 'Pan'),
        ('TILT', 'Tilt'),
        ('PAN-F','Pan-Fine'),
        ('TILT-F','Pan-Tilt'),
        ('MOTION', 'Motion'),
        ('MOTION-F', 'Motion-Fine'),
        ('SPEED','Speed'),
        ('SPEED-F','Speed-Fine'),
    )

    def __iter__(self):
        return iter(self.CHANNEL_TYPE_LIST)



class RGB():
    #Adds the  R, G, and B Items to a list.  Can be used for display or to create records in the DeviceFeatureItems Model  
    def append_item_list(self, item_list=[]):
        pass
        #item_dict = 
        #item_list.append('value': '0')
        #channel_list.append()
    