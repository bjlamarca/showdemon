
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
