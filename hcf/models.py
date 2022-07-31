from django.db import models


# Create your models here.
class menu(models.Model):
    title = models.CharField(max_length=30,verbose_name='عنوان')
    url_name = models.CharField(max_length=50, null=True, blank=True,verbose_name='لینک')
    sub_menu = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,verbose_name='زیر منو')

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'منو '
        verbose_name_plural = "منو"


class lep(models.Model):
    email = models.EmailField(null=True, blank=True,verbose_name='ایمیل')
    phone = models.IntegerField(null=True, blank=True,verbose_name='تلفن')
    logo = models.ImageField(upload_to='image', null=True, blank=True,verbose_name='لوگو')

    def __str__(self):
        return self.email
    class Meta:
        verbose_name = ''
        verbose_name_plural = "لوگو ایمیل تلفن"
