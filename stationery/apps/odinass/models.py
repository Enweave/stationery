import uuid

from django.db import models
from django.db.models import OuterRef, Prefetch, Subquery
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from django.urls import reverse

from django_resized import ResizedImageField

from mptt.models import MPTTModel, TreeForeignKey

from sorl.thumbnail import delete as sorl_delete_image

from odinass.utils import format_price


def generate_upload_path(instance, filename):
    filename = '{name}.{ext}'.format(name=uuid.uuid4().hex,
                                     ext=instance.image_format)
    return '{folder}/{file}'.format(folder=instance.image_folder,
                                    file=filename)


class Category(MPTTModel):
    """
    Категория товаров
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        'название',
        max_length=254, db_index=True)
    parent = TreeForeignKey(
        'self',
        verbose_name='родительская категория',
        related_name='children',
        null=True, blank=True, db_index=True)
    is_published = models.BooleanField(
        'опубликовано',
        default=True)
    image = models.ImageField(
        'изображене',
        upload_to='category/', null=True, blank=True)
    order = models.PositiveIntegerField(
        default=0, blank=False, null=False)

    class MPTTMeta:
        order_insertion_by = ['order']

    class Meta:
        default_related_name = 'categories'
        ordering = ['order']
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:category', args=[str(self.id)])

    @property
    def offers(self):
        # цены для ретейла
        price = Price.objects.filter(offer=OuterRef('pk'),
                                     price_type__sales_type=SalesType.RETAIL)

        # остатки по нужным складам
        prefetch = Prefetch(
            'rests', queryset=Rest.objects.filter(warehouse__is_selected=True)
                                          .order_by('warehouse__title'))

        return (Offer.objects
                     .select_related('product')
                     .prefetch_related('prices', 'prices__price_type',
                                       prefetch, 'rests__warehouse',
                                       'product__property_values',
                                       'product__property_values__property')
                     .filter(product__categories=self)
                     .annotate(
                        retail_price=Subquery(price.values('price')[:1])))


class Warehouse(models.Model):
    """
    Склад
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        'название',
        max_length=254, db_index=True)
    is_selected = models.BooleanField(
        'выбрано',
        default=False)

    class Meta:
        default_related_name = 'warehouses'
        ordering = ['title']
        verbose_name = 'склад'
        verbose_name_plural = 'склады'

    def __str__(self):
        return self.title


class Rest(models.Model):
    """
    Остаток
    """
    value = models.IntegerField(
        'остаток',
        default=0)
    warehouse = models.ForeignKey(
        'odinass.Warehouse',
        verbose_name='склад')
    offer = models.ForeignKey(
        'odinass.Offer',
        verbose_name='предложение')

    class Meta:
        default_related_name = 'rests'
        verbose_name = 'остаток'
        verbose_name_plural = 'остатки'

    def __str__(self):
        return str(self.value)


class Property(models.Model):
    """
    Свойство
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        'название',
        max_length=254)
    value_type = models.CharField(
        'тип значений',
        max_length=254, blank=True)

    class Meta:
        default_related_name = 'properties'
        ordering = ['title']
        verbose_name = 'свойство'
        verbose_name_plural = 'свойства'

    def __str__(self):
        return self.title


class Product(models.Model):
    """
    Товар
    """
    image_folder = 'products'
    image_format = 'jpg'

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        'название', max_length=508)
    article = models.CharField(
        'артикул', blank=True, max_length=254)
    categories = models.ManyToManyField(
        'odinass.Category',
        verbose_name='категории',
        blank=True)
    property_values = models.ManyToManyField(
        'odinass.PropertyValue',
        verbose_name='значения свойства',
        blank=True)
    image = ResizedImageField(
        'изображение',
        size=[1024, 1024], upload_to=generate_upload_path, force_format='JPEG',
        null=True, blank=True)
    created = models.DateField(
        'дата создания',
        auto_now_add=True, editable=False, null=False, blank=False)

    class Meta:
        default_related_name = 'products'
        ordering = ['title']
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.title


class PropertyValue(models.Model):
    """
    Справочник
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        'название',
        max_length=254)
    property = models.ForeignKey(
        'odinass.Property',
        verbose_name='свойство')

    class Meta:
        default_related_name = 'property_values'
        ordering = ['title']
        verbose_name = 'значение свойства'
        verbose_name_plural = 'значения свойства'

    def __str__(self):
        return self.title


class SalesType(object):
    """
    Тип продажи
    """
    RETAIL = 1
    WHOLESALE = 2

    CHOICES = (
        (RETAIL, 'розница'),
        (WHOLESALE, 'оптовая продажа'),
    )

    CHOICES_MACHINE_NAME = {
        RETAIL: 'retail',
        WHOLESALE: 'wholesale',
    }


class PriceType(models.Model):
    """
    Тип цены
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        'наименование',
        max_length=254)
    sales_type = models.IntegerField(
        'тип продажи',
        choices=SalesType.CHOICES, db_index=True, blank=True, null=True,
        unique=True)

    class Meta:
        default_related_name = 'price_types'
        ordering = ['title']
        verbose_name = 'тип цены'
        verbose_name_plural = 'тип цен'

    def __str__(self):
        return self.title


class Price(models.Model):
    """
    Цены
    """
    currency = models.CharField(
        'валюта',
        max_length=254)
    price = models.DecimalField(
        'цена',
        max_digits=12, decimal_places=2)
    price_type = models.ForeignKey(
        'odinass.PriceType',
        verbose_name='тип цены')
    offer = models.ForeignKey(
        'odinass.Offer',
        verbose_name='предложение')

    class Meta:
        default_related_name = 'prices'
        ordering = ['currency']
        verbose_name = 'цена'
        verbose_name_plural = 'цены'

    def __str__(self):
        price = 'нет цены'
        if self.price:
            price = '%s %s' % (self.price, self.currency)
        return price


class Offer(models.Model):
    """
    Предложение
    """
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(
        'наименование', max_length=254)
    product = models.ForeignKey(
        'odinass.Product',
        verbose_name='товар')

    class Meta:
        default_related_name = 'offers'
        ordering = ['title']
        verbose_name = 'предложение'
        verbose_name_plural = 'предложения'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages:product', args=[str(self.id)])

    @property
    def price(self):
        price = self.prices.filter(price_type__sales_type=SalesType.RETAIL)
        if len(price):
            price = price.first()
        else:
            return 'нет цены'
        return '%s %s' % (format_price(price.price), price.currency)

    @property
    def features(self):
        return (PropertyValue.objects
                             .filter(product=self.product))

    @property
    def rest_list(self):
        return (Rest.objects.filter(warehouse__is_selected=True, offer=self)
                            .order_by('warehouse__title'))


class ActionLog(object):
    """
    Список операций для логирования
    """
    IMPORT = 1
    EXPORT = 2

    CHOICES = (
        (IMPORT, 'импорт'),
        (EXPORT, 'экспорт'),
    )

    CHOICES_MACHINE_NAME = {
        IMPORT: 'import',
        EXPORT: 'export',
    }


class StatusLog(object):
    """
    Список статусов для логирования
    """
    PROGRESS = 1
    FINISHED = 2
    FAILD = 3

    CHOICES = (
        (PROGRESS, 'обрабатывается'),
        (FINISHED, 'завершено'),
        (FAILD, 'завершено с ошибкой'),
    )

    CHOICES_MACHINE_NAME = {
        PROGRESS: 'progress',
        FINISHED: 'finished',
        FAILD: 'faild',
    }


class Log(models.Model):
    """
    Логирование импорта и экспорта с 1С
    """
    action = models.IntegerField(
        'действие',
        choices=ActionLog.CHOICES, blank=True, null=True)

    status = models.IntegerField(
        'статус',
        choices=StatusLog.CHOICES, default=StatusLog.PROGRESS)

    filename = models.CharField(
        'название файла',
        max_length=254, db_index=True)

    created = models.DateTimeField(
        'время создания',
        auto_now_add=True, editable=False, null=False, blank=False)

    traceback = models.TextField(
        'traceback',
        blank=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'лог'
        verbose_name_plural = 'логи'

    def __str__(self):
        return str(self.created)


@receiver(pre_save, sender=Product, dispatch_uid='delete_old_thumb_on_save')
def delete_old_thumb_on_save(sender, instance=None, **kwargs):
    """
    Удаляем изображение и его тамбнейлы, если изображение поменялось
    """
    if instance:
        instance.full_clean()
        try:
            old_instance = sender.objects.get(pk=instance.pk)
            if old_instance.image and old_instance.image is not instance.image:
                sorl_delete_image(old_instance.image)
        except sender.DoesNotExist:
            pass


@receiver(post_delete, sender=Product,
          dispatch_uid='delete_old_thumb_on_delete')
def delete_old_thumb_on_delete(sender, instance=None, **kwargs):
    """
    Удаляем изображение и его тамбнейлы, если удаляем instance
    """
    if instance and instance.image:
        instance.full_clean()
        sorl_delete_image(instance.image)
