from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from devices.constants import SystemType, Interfaces, ChannelType, FeatureList



class Manufacture(models.Model):
    name = models.CharField(max_length=150)
    comments = models.TextField(
        verbose_name='comments',
        blank=True, 
        null=True
    )
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("devices:manufacture", kwargs={"pk": self.pk})


#Templates that become parents for Devices. Should not be modified once a child device is created.  
class LibraryDevice(models.Model):
    name = models.CharField(max_length=150)
    system = models.CharField(
        max_length=10,
        choices=SystemType
    )
    manufacture = models.ForeignKey(
        to=Manufacture,
        on_delete=models.PROTECT
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
        )

    class Meta:
        verbose_name = 'Device Library',
        verbose_name_plural = 'Device Library'
        

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("devices:device_library", kwargs={"pk": self.pk})




#Children of DeviceLibrary records, Devices refer to through their parent.
class DeviceFeature(models.Model):
    name = models.CharField(max_length=150)
    feature_class = models.CharField(
        max_length=100,
        choices=FeatureList
        )
    system = models.CharField(
        max_length=10,
        choices=SystemType
    )
    library_device = models.ForeignKey(
        to=LibraryDevice,
        on_delete=models.PROTECT
    )
    sort_order = models.IntegerField()
    hide = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Device Feature'
    
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("devices:device_feature", kwargs={"pk": self.pk})

 # Child of a DeviceFeature, created by a feature class.  Parameter is JSON (Dict) for extra info, example 
 # would be min, max, scaled min, scaled max values for the int_value field
 # It is meant to be flexable, for features classes to use as needed. For DMX, this would a channel.   
class LibraryChannel(models.Model):
    name = models.CharField(max_length=150)
    channel_type = models.CharField(
        max_length=100,
        choices=ChannelType
    ) 
    device_feature = models.ForeignKey(
        to=DeviceFeature,
        on_delete=models.CASCADE
    )
    int_min = models.IntegerField(
        blank=True,
        null=True
    )
    int_max = models.IntegerField(
        blank=True,
        null=True
    )
    str_value = models.CharField(
        max_length=(1000),
        blank = True
    )
    parameter = models.CharField(
        max_length=(1000),
        blank = True
    )
    startup_int = models.IntegerField(
        blank=True,
        null=True
    )
    sort_order = models.IntegerField()
    hide = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("devices:channel", kwargs={"pk": self.pk})

# Child of LibraryChannel.  Can be used for selections, or other ranges in the channel.
# the max and min fields must be within the range of thoose fields in parent Channel 
class ChannelParameter(models.Model):
    name = models.CharField(max_length=150)
    allow_fading = models.BooleanField(default=False)
    library_channel = models.ForeignKey(
        to=LibraryChannel,
        on_delete=models.CASCADE
    )
    int_value = models.IntegerField(
        blank=True,
        null=True
    )
    int_min = models.IntegerField(
        blank=True,
        null=True
    )
    int_max = models.IntegerField(
        blank=True,
        null=True
    )
    str_value = models.CharField(
        max_length=(5000),
        blank = True,
        null=True
    )
    color = models.ForeignKey(
        to='Color',
        on_delete=models.PROTECT,
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("devices:channel_parameter", kwargs={"pk": self.pk})

#The actual physical or virtual device, a child of DeviceLibrary item.    
class Device(models.Model):
    name = models.CharField(max_length=150)
    device_library = models.ForeignKey(
        to=LibraryDevice,
        on_delete=models.PROTECT
    )
    interface = models.CharField(
        max_length=10, 
        choices=Interfaces,
        blank=True,
        null=True

    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
        )
    
    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("devices:device", kwargs={"pk": self.pk})

#Linked to a library channel, only stores values  
class Channel(models.Model):
    device = models.ForeignKey(
        to=Device,
        on_delete=models.CASCADE
    )
    library_channel = models.ForeignKey(
        to=LibraryChannel,
        on_delete=models.PROTECT
    )
    system_channel = models.IntegerField(
        blank=True,
        null=True
    )   
    channel_number = models.IntegerField()
    int_value = models.IntegerField(
        blank=True,
        null=True
    )
    str_value = models.CharField(
        max_length=(1000),
        blank = True,
        null=True
    )
    parameter = models.CharField(
        max_length=(1000),
        blank = True,
        null=True
    )

    def __str__(self):
        return str(self.device.name) + ' ' + str(self.channel_number)

    def get_absolute_url(self):
        return reverse("devices:channel", kwargs={"pk": self.pk})


    
class Color(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Name'
    )
    favorite = models.BooleanField(
        verbose_name='Favorite'
    )
    hex_code = models.CharField(
        max_length=7,
        verbose_name='Hex Code'
    )
    red = models.IntegerField(
        verbose_name='Red'
    )
    green = models.IntegerField(
        verbose_name='Green'
    )
    blue = models.IntegerField(
        verbose_name='Blue'
    )
    sort = models.IntegerField(
        verbose_name='Sort',
        blank=True,
        null=True
    )    


    def __str__(self):
        return self.name





#def save(self, *args, **kwargs):
    #     if not (self.device_library or self.device):
    #         raise ValidationError("A Device or Library Dev")
    #     super().save(*args, **kwargs)



