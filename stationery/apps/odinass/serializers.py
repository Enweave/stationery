import operator
import re

from functools import reduce

from django.db.models import Q, Value
from django.db.models.functions import Concat

import django_filters

from rest_framework import serializers

from odinass.models import Category, Offer


def escape(s):
    return re.sub(r'[(){}\[\].*?|^$\\+-]', r'\\\g<0>', s)


class OfferTitleFilter(django_filters.Filter):
    """
    Поиск для автокомплита.
    """
    max_result = 5
    uniq_category = True

    def filter(self, qs, value):
        qs = qs.annotate(full_name=Concat(
            'product__article', Value(' '),
            'product__title', Value(' '),
            'product__search_title'))
        bits = value.split(' ')
        if len(bits) is 1 and bits[0].isdecimal():
            full_name_clauses = Q(full_name__icontains=bits[0])
        else:
            full_name_clauses = reduce(
                operator.and_,
                [Q(full_name__iregex=r'(^|\s)%s' % escape(v))
                 for v in bits])

        unpublished = Category.objects.get_queryset_descendants(
            Category.objects.filter(is_published=False),
            include_self=True)

        qs = (qs.filter(full_name_clauses)
                .exclude(product__category__in=unpublished))

        if self.uniq_category:
            products = (qs.order_by('product__category__title')
                          .distinct('product__category__title'))
            qs = (qs.filter(id__in=products)
                    .order_by('-product__category__views'))

        return qs[:self.max_result]


class CategoryTitleFilter(django_filters.Filter):
    """
    Фильтр категорий по названию.
    """
    max_result = 10

    def filter(self, qs, value):
        bits = value.split(' ')
        search_clauses = reduce(operator.and_,
                                [Q(title__icontains=v) for v in bits])
        unpublished = Category.objects.get_queryset_descendants(
            Category.objects.filter(is_published=False), include_self=True)
        qs = (qs
              .exclude(pk__in=unpublished)
              .filter(search_clauses)
              .order_by('-views'))
        return qs[:self.max_result]


class OfferQFilter(OfferTitleFilter):
    """
    Поиск для страницы поиска.
    """
    max_result = 200
    uniq_category = False


class SearchOfferFilter(django_filters.FilterSet):
    title = OfferTitleFilter()
    q = OfferQFilter()

    class Meta:
        fields = ('title', 'q')
        model = Offer


class SearchCategoryFilter(django_filters.FilterSet):
    """
    Фильтры для поиска категорий.
    """
    title = CategoryTitleFilter()

    class Meta:
        fields = ('title',)
        model = Category


class SearchOfferSerializer(serializers.ModelSerializer):
    url = serializers.CharField(source='get_absolute_url', read_only=True)
    category = serializers.CharField(source='product.category', read_only=True)
    # price_retail = serializers.CharField(source='price', read_only=True)
    price_retail = serializers.SerializerMethodField(read_only=True)
    title = serializers.CharField(source='full_title', read_only=True)

    class Meta:
        fields = '__all__'
        model = Offer

    def get_price_retail(self, obj):
        request = self.context.get('request')
        user = None
        if request and hasattr(request, 'user'):
            user = request.user
        return obj.price(user=user)


class SearchCategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для результата поиска категории.
    """
    url = serializers.CharField(
        source='get_absolute_url', read_only=True)

    class Meta:
        fields = ['id', 'url', 'title']
        model = Category
