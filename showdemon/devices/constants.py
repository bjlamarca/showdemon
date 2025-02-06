
class SystemType():
    SYSTEM_CHOICES = (
        ('DMX', 'DMX'),
        ('PICOM', 'PiCom')
    )
    
    def get_display(self, system):
        for choice in self.SYSTEM_CHOICES:
            if choice[0] == system:
                return choice[1]
        return None

    def __iter__(self):
        return iter(self.SYSTEM_CHOICES)

class Interfaces():
    INTERFACE_CHOICES = (
        ('DMX1', 'DMX 1'),
    )
    
    def __iter__(self):
        return iter(self.INTERFACE_CHOICES)


#(Name, Display , Feature Type )
class FeatureList():
    FEATURE_LIST = (
        ('DMX_RGB','DMX RGB'),
        ('DMX_DIMM', 'DMX Dimmer'),
        ('DMX_COLORWHL', 'DMX Color Wheel'),
        ('DMX_PANTILT', 'DMX Pan Tilt'),
        ('DMX_SELECT', 'DMX Selector')
    )

    def __iter__(self):
        return iter(self.FEATURE_LIST)
    def get_display(self, feature):
        for choice in self.FEATURE_LIST:
            if choice[0] == feature:
                return choice[1]
        return None
    
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
    def get_display(self, channel):
        for choice in self.CHANNEL_TYPE_LIST:
            if choice[0] == channel:
                return choice[1]
        return None
