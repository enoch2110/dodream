import django_filters
from academy.models import Student


class StudentFilter(django_filters.FilterSet):

    class Meta:
        model = Student
        fields = ['attend_method', 'use_sms']

    #
    # def __init__(self, *args, **kwargs):
    #     super(StudentFilter, self).__init__(*args, **kwargs)
    #     self.filters['manufacturer'].extra.update(
    #         {'empty_label': 'All Manufacturers'})

