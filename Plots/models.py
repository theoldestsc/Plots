from django.db import models
from django.contrib.auth.models import User


# Create your models here.

def get_upload_path(instance,filename):
    return "Plots/{0}/{1}".format(instance.user.username, filename)

class Plot(models.Model):
    user = models.ForeignKey('auth.User',
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    image = models.ImageField(null = True, upload_to = get_upload_path)
    date = models.DateTimeField(auto_now=True)

    function = models.TextField(blank = False, null = False)
    interval = models.CharField(max_length=50,blank = False, null = False)
    step = models.CharField(max_length=20, blank = False, null = False)

    class Meta:
        ordering = ['-id']
