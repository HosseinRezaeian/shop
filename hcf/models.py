from django.db import models


# Create your models here.
class menu(models.Model):
    title = models.CharField(max_length=30)
    url_name = models.CharField(max_length=50, null=True, blank=True)
    sub_menu = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class lep(models.Model):
    email = models.EmailField(null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    logo = models.ImageField(upload_to='image', null=True, blank=True)

    def __str__(self):
        return self.email
