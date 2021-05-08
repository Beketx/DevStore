from django_filters import rest_framework as filters

from developer.models import DeveloperService, \
                                Developer, \
                                Stacks

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

