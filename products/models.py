from django.db import models
from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class category(MPTTModel):
    title = models.CharField(max_length=30, verbose_name='عنوان')
    slug = models.SlugField(max_length=30, verbose_name='نمایش رد لینک')
    pic = models.ImageField(null=True, blank=True, verbose_name='تصویر')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return '{0} <<<< {1}'.format(self.title, self.parent)

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = "دسته بندی ها"


class brand(models.Model):
    title = models.CharField(max_length=50, verbose_name='برند')
    pic = models.ImageField(null=True, blank=True, verbose_name='تصویر')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برند '
        verbose_name_plural = "برندها"


# Create your models here.
class product(models.Model):
    pic = models.ImageField(upload_to='image', null=True, blank=True)
    pic1 = models.ImageField(upload_to='image', null=True, blank=True)
    pic2 = models.ImageField(upload_to='image', null=True, blank=True)
    title = models.CharField(max_length=30, verbose_name='عنوان')
    category1 = models.ForeignKey(category, default=True, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='gat', verbose_name='دسته بندی')
    number = models.IntegerField(blank=True, null=True, default=0, verbose_name='تعداد')
    brand = models.ForeignKey(brand, on_delete=models.CASCADE, null=True, blank=True, default="null",
                              verbose_name='برند')
    price = models.IntegerField(verbose_name='قیمت')
    discripion = models.CharField(max_length=300, verbose_name='توضیحات')
    slug = models.SlugField(max_length=30, verbose_name='نماش در لینک')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_discount = models.BooleanField(default=False)
    last_price = models.IntegerField(null=True, blank=True)
    cent = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = "محصولات"


class Opinion(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    title = models.CharField(max_length=50)
    text_area = models.TextField(max_length=300)
    proda = models.IntegerField(null=True)
    answer = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = "نظرات"


class report(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    text = models.TextField(max_length=300)
    id_c = models.IntegerField()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'گزارش'
        verbose_name_plural = "گزارش ها"


class discount(models.Model):
    dis = models.IntegerField(verbose_name='درصد تخفیف')

    def __str__(self):
        return str(self.dis)

    class Meta:
        verbose_name = 'درصد '
        verbose_name_plural = "تخفیف"
