# import operator
# from functools import reduce
#
# from django.db.models import Q
# from django_filters import rest_framework as filters
# from dry_rest_permissions.generics import DRYPermissionFiltersBase
#
# from developer import models
#
# class DeveloperFilterBackend(DRYPermissionFiltersBase):
#     def filter_list_queryset(self, request, queryset, view):
#         if request.user.is_joined:
#             return queryset
#
#         return queryset.filter(Q(role=request.user.role))
#
# def filter_developer(queryset, name, value):
#     lookups = ['title__icontains']
#     or_queries = []
#     search_terms = value.split()
#
#     for search_term in search_terms:
#         or_queries += [Q(**{lookup: search_term}) for lookup in lookups]
#
#     return queryset.filter(reduce(operator.or_, or_queries))
#
# class DeveloperFilter(filters.FilterSet):
#     title = filters.CharFilter(method=filter_developer)
#
#     class Meta:
#         model = models.Developer
#         fields = [
#             'stacks_id'
#         ]

from django_filters import rest_framework as filters

from developer.models import DeveloperService, Developer, Stacks


# class ArrayFilter(filters.Filterset):
#     stacks = filters.NumberFilter(field_name='dev_service__price')
class IntegerListFilter(filters.Filter):
    def filter(self, qs, value):
        if value not in (None, ''):
            str = value
            print(value)
            str1 = str.replace(']', '').replace('[', '')
            l = str1.replace('"', '').split(",")
            integers = [v for v in l]
            return qs.filter(**{'%s__%s' % (self.field_name, self.lookup_expr): integers})
        return qs

class PriceFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name='dev_service__price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='dev_service__price', lookup_expr='lte')
    stacks = IntegerListFilter(field_name='stacks_id', lookup_expr='in')
    skills = IntegerListFilter(field_name='skills_id', lookup_expr='in')
    # skills = filters.NumberFilter(field_name='dev_service__price')

    class Meta:
        model = Developer
        fields = ('dev_service__price', 'stacks_id', 'education',
                  'skills_id', 'user__city', )